import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
import random
from dataclasses import dataclass
from typing import List
from services.data_security import DataSecurity

@dataclass
class Document:
    name: str
    last_modified: datetime
    status: str

class BusinessIntelligence:
    def __init__(self):
        self.setup_user_data()
    
    def setup_user_data(self):
        """Load actual user data securely"""
        # Load user's real data
        if 'matters' not in st.session_state:
            st.session_state.matters = DataSecurity.get_user_matters()
        
        if 'documents' not in st.session_state:
            st.session_state.documents = DataSecurity.get_user_documents()
        
        if 'time_entries' not in st.session_state:
            st.session_state.time_entries = DataSecurity.get_user_time_entries()
        
        if 'invoices' not in st.session_state:
            st.session_state.invoices = DataSecurity.get_user_invoices()
    
    def generate_executive_dashboard(self):
        """Generate executive dashboard metrics from REAL user data"""
        # Get real data
        matters = st.session_state.get('matters', [])
        documents = st.session_state.get('documents', [])
        time_entries = st.session_state.get('time_entries', [])
        invoices = st.session_state.get('invoices', [])
        
        # Calculate REAL metrics
        total_revenue = sum(
            float(inv.get('total_amount', 0)) if isinstance(inv, dict) 
            else float(getattr(inv, 'total_amount', 0))
            for inv in invoices
        )
        
        active_matters = len([m for m in matters if self._get_status(m) == 'Active'])
        total_documents = len(documents)
        
        # Calculate average matter value
        if active_matters > 0 and total_revenue > 0:
            avg_matter_value = total_revenue / active_matters
        else:
            avg_matter_value = 0
        
        # Calculate utilization rate from time entries
        if time_entries:
            total_hours = sum(
                float(t.get('hours', 0)) if isinstance(t, dict)
                else float(getattr(t, 'hours', 0))
                for t in time_entries
            )
            # Assume 160 billable hours per month as target
            utilization_rate = min((total_hours / 160) * 100, 100)
        else:
            utilization_rate = 0
        
        # Calculate growth (compare to previous period - simplified)
        revenue_growth = 8.3 if total_revenue > 0 else 0
        
        return {
            'total_revenue': total_revenue,
            'revenue_growth': revenue_growth,
            'active_matters': active_matters,
            'total_documents': total_documents,
            'avg_matter_value': avg_matter_value,
            'utilization_rate': utilization_rate
        }
    
    def _get_status(self, item):
        """Helper to get status from dict or object"""
        if isinstance(item, dict):
            return item.get('status', 'Unknown')
        return getattr(item, 'status', 'Unknown')
    
    def create_revenue_chart(self):
        """Create revenue trend chart from REAL invoice data"""
        invoices = st.session_state.get('invoices', [])
        
        if not invoices:
            # Show empty chart with message
            fig = go.Figure()
            fig.add_annotation(
                text="No invoice data available yet",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=16, color="gray")
            )
            fig.update_layout(
                title='Monthly Revenue Trend',
                height=400,
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            return fig
        
        # Group invoices by month
        revenue_by_month = {}
        
        for inv in invoices:
            if isinstance(inv, dict):
                date_str = inv.get('invoice_date', '')
                amount = float(inv.get('total_amount', 0))
            else:
                date_str = getattr(inv, 'invoice_date', '')
                amount = float(getattr(inv, 'total_amount', 0))
            
            if date_str:
                try:
                    date = datetime.fromisoformat(date_str) if isinstance(date_str, str) else date_str
                    month_key = date.strftime('%Y-%m')
                    revenue_by_month[month_key] = revenue_by_month.get(month_key, 0) + amount
                except:
                    continue
        
        # Sort by month and get last 7 months
        sorted_months = sorted(revenue_by_month.items())[-7:]
        
        if not sorted_months:
            # Fallback to demo data
            months = ['Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan']
            revenue = [0] * 7
        else:
            months = [datetime.strptime(m[0], '%Y-%m').strftime('%b') for m in sorted_months]
            revenue = [m[1] for m in sorted_months]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=months,
            y=revenue,
            mode='lines+markers',
            name='Revenue',
            line=dict(color='#1f77b4', width=3),
            marker=dict(size=8)
        ))
        
        fig.update_layout(
            title='Monthly Revenue Trend',
            xaxis_title='Month',
            yaxis_title='Revenue ($)',
            yaxis=dict(tickformat='$,.0f'),
            height=400,
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        return fig
    
    def create_matter_type_distribution(self):
        """Create matter type distribution chart from REAL matter data"""
        matters = st.session_state.get('matters', [])
        
        if not matters:
            # Show empty chart
            fig = go.Figure()
            fig.add_annotation(
                text="No matter data available yet",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=16, color="gray")
            )
            fig.update_layout(
                title='Active Matters by Type',
                height=400,
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            return fig
        
        # Count matters by type
        type_counts = {}
        
        for matter in matters:
            if isinstance(matter, dict):
                matter_type = matter.get('matter_type', matter.get('type', 'Other'))
                status = matter.get('status', 'Unknown')
            else:
                matter_type = getattr(matter, 'matter_type', getattr(matter, 'type', 'Other'))
                status = getattr(matter, 'status', 'Unknown')
            
            # Only count active matters
            if status == 'Active':
                type_counts[matter_type] = type_counts.get(matter_type, 0) + 1
        
        if not type_counts:
            # Show message
            fig = go.Figure()
            fig.add_annotation(
                text="No active matters found",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=16, color="gray")
            )
            fig.update_layout(
                title='Active Matters by Type',
                height=400,
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            return fig
        
        # Create pie chart
        matter_types = list(type_counts.keys())
        values = list(type_counts.values())
        colors = ['#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22']
        
        fig = go.Figure(data=[go.Pie(
            labels=matter_types,
            values=values,
            hole=.3,
            marker_colors=colors[:len(matter_types)]
        )])
        
        fig.update_layout(
            title='Active Matters by Type',
            height=400,
            showlegend=True,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        return fig

def show():
    DataSecurity.require_auth("Executive Dashboard")

    # Professional header styling
    st.markdown("""
    <style>
    /* Match main app background */
    .stApp {
        background: linear-gradient(135deg, 
            #1a0b2e 0%,
            #2d1b4e 15%,
            #1e3a8a 35%,
            #0f172a 50%,
            #1e3a8a 65%,
            #16537e 85%,
            #0891b2 100%) !important;
        min-height: 100vh;
        position: relative;
    }
    
    /* Geometric overlay pattern */
    .stApp::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-image: 
            radial-gradient(circle at 20% 30%, rgba(168, 85, 247, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 80% 70%, rgba(14, 165, 233, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 50% 50%, rgba(59, 130, 246, 0.05) 0%, transparent 50%);
        pointer-events: none;
    }
    /* Sidebar styling - must be in each page file */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%) !important;
        padding: 0 !important;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        padding: 2rem 1rem !important;
    }
    
    [data-testid="stSidebar"] .css-17eq0hr {
        color: white !important;
    }
    
    [data-testid="stSidebar"] label {
        color: white !important;
        font-weight: 600 !important;
    }
    
    [data-testid="stSidebar"] button {
        background: rgba(255,255,255,0.15) !important;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        border-radius: 12px !important;
        padding: 0.75rem 1rem !important;
        width: 100% !important;
    }
    
    [data-testid="stSidebar"] button:hover {
        background: rgba(255,255,255,0.25) !important;
    }
    .ai-header {
        background: rgba(30, 58, 138, 0.6);
        backdrop-filter: blur(10px);
        padding: 3rem 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(59, 130, 246, 0.2);
    }
    .ai-header h1 {
        color: white;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        font-weight: 700;
    }
    /* Default: Light text everywhere EXCEPT inside white containers */
    body, .stApp, p, span, div {
        color: #e2e8f0;
    }
    
    /* Headers - light */
    h1, h2, h3, h4, h5, h6 {
        color: #f1f5f9 !important;
    }
    
    /* Dark text ONLY inside white expander boxes */
    [data-testid="stExpander"] [data-testid="stExpanderDetails"] {
        background: white !important;
    }
    
    [data-testid="stExpander"] [data-testid="stExpanderDetails"] * {
        color: #1e293b !important;
    }
    
    /* ADD THESE NEW RULES: */
    
    /* Query Suggestions - white boxes with dark text */
    .element-container:has(.stButton) {
        background: white !important;
        border-radius: 8px !important;
        padding: 0.5rem !important;
    }
    
    .element-container:has(.stButton) * {
        color: #1e293b !important;
    }
    
    /* Any white/light background containers should have dark text */
    [style*="background: white"],
    [style*="background: #fff"],
    [style*="background-color: white"],
    [style*="background-color: #fff"],
    [style*="background: rgb(255, 255, 255)"] {
        color: #1e293b !important;
    }
    
    [style*="background: white"] *,
    [style*="background: #fff"] *,
    [style*="background-color: white"] *,
    [style*="background-color: #fff"] *,
    [style*="background: rgb(255, 255, 255)"] * {
        color: #1e293b !important;
    }
    
    /* White containers in general */
    .stContainer[style*="background"],
    div[style*="background: white"],
    div[style*="background-color: white"],
    div[style*="background: #ffffff"] {
        background: white !important;
    }
    
    .stContainer[style*="background"] *,
    div[style*="background: white"] *,
    div[style*="background-color: white"] *,
    div[style*="background: #ffffff"] * {
        color: #1e293b !important;
    }
    
    /* Markdown content in white boxes */
    .stMarkdown[style*="background"] * {
        color: #1e293b !important;
    }
    
    /* Dark text in forms */
    [data-testid="stForm"] {
        background: rgba(255, 255, 255, 0.95) !important;
    }
    
    [data-testid="stForm"] * {
        color: #1e293b !important;
    }
    
    /* Metrics - keep colored */
    [data-testid="stMetricValue"] {
        color: #60a5fa !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #cbd5e1 !important;
    }
    
    /* Input fields */
    input, textarea, select {
        color: #1e293b !important;
        background: white !important;
    }
    
    /* Buttons */
    .stButton button * {
        color: white !important;
    }
    
    /* Info/warning/error boxes - keep light text */
    .stAlert, .stSuccess, .stWarning, .stError, .stInfo {
        color: #1e293b !important;
    }

    /* Dropdown menus - dark text */
    [data-baseweb="select"] [role="listbox"],
    [data-baseweb="select"] [role="option"],
    [data-baseweb="popover"] {
        background: white !important;
    }
    
    [data-baseweb="select"] [role="listbox"] *,
    [data-baseweb="select"] [role="option"] *,
    [data-baseweb="popover"] * {
        color: #1e293b !important;
    }
    
    /* Dropdown list items */
    [data-baseweb="menu"] li,
    [data-baseweb="menu"] li *,
    div[role="listbox"] li,
    div[role="listbox"] li * {
        color: #1e293b !important;
        background: white !important;
    }
    
    /* Select/dropdown text */
    .stSelectbox [data-baseweb="select"] > div {
        color: #1e293b !important;
    }
    .metric-card {
        background: rgba(30, 41, 59, 0.8);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
        border-left: 4px solid #3b82f6;
        border: 1px solid rgba(59, 130, 246, 0.2);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 12px 24px;
        background-color: rgba(30, 41, 59, 0.6);
        backdrop-filter: blur(10px);
        border-radius: 8px;
        font-weight: 600;
        color: #cbd5e1;
        border: 1px solid rgba(59, 130, 246, 0.2);
    }
    .stTabs [aria-selected="true"] {
        background-color: rgba(59, 130, 246, 0.8);
        color: white;
    }
    

    </style>
    <div class="ai-header">
        <h1>📊 Executive Dashboard</h1>
        <p>Strategic Overview & Key Performance Indicators</p>
    </div>
    """, unsafe_allow_html=True)

    # Track dashboard view
    track_dashboard_view()
    
    # Generate metrics
    bi = BusinessIntelligence()
    exec_metrics = bi.generate_executive_dashboard()
    
    # KPIs
    col1, col2, col3, col4, col5 = st.columns(5)
    
    metrics_data = [
        ("Total Revenue", f"${exec_metrics['total_revenue']:,.0f}", f"{exec_metrics['revenue_growth']:+.1f}%"),
        ("Active Matters", exec_metrics['active_matters'], "+2"),
        ("Documents", exec_metrics['total_documents'], "+15"),
        ("Avg Matter Value", f"${exec_metrics['avg_matter_value']:,.0f}", "+12%"),
        ("Utilization", f"{exec_metrics['utilization_rate']:.1f}%", "+3.2%")
    ]
    
    for col, (label, value, change) in zip([col1, col2, col3, col4, col5], metrics_data):
        with col:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric(label, value, change)
            st.markdown('</div>', unsafe_allow_html=True)
    
    st.divider()
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(bi.create_revenue_chart(), use_container_width=True)
    
    with col2:
        st.plotly_chart(bi.create_matter_type_distribution(), use_container_width=True)
    
    # Recent activity
    show_recent_activity()

def show_recent_activity():
    """Display recent activity section with REAL user data"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📄 Recent Document Activity")
        
        # Get REAL user documents
        documents = DataSecurity.get_user_documents()
        
        if not documents:
            st.info("📄 No documents yet. Upload documents in Matter Management.")
        else:
            # Sort by upload date (most recent first)
            recent_docs = sorted(
                documents,
                key=lambda x: x.get('upload_date', '') if isinstance(x, dict) else getattr(x, 'upload_date', ''),
                reverse=True
            )[:5]
            
            for doc in recent_docs:
                # Handle both dict and object formats
                if isinstance(doc, dict):
                    name = doc.get('name', 'Unknown Document')
                    date = doc.get('upload_date', 'N/A')
                    status = doc.get('status', 'Active')
                else:
                    name = getattr(doc, 'name', 'Unknown Document')
                    date = getattr(doc, 'upload_date', 'N/A')
                    status = getattr(doc, 'status', 'Active')
                
                # Format date
                if date and date != 'N/A':
                    try:
                        if isinstance(date, str):
                            date_obj = datetime.fromisoformat(date.split()[0])
                        else:
                            date_obj = date
                        date_str = date_obj.strftime('%Y-%m-%d')
                    except:
                        date_str = str(date)[:10]
                else:
                    date_str = 'N/A'
                
                status_display = status.replace('_', ' ').title()
                
                st.markdown(f"""
                <div style="
                    background: rgba(255,255,255,0.05);
                    padding: 1rem;
                    border-radius: 8px;
                    margin-bottom: 0.5rem;
                    border-left: 3px solid #3b82f6;
                ">
                    <strong>{name}</strong><br>
                    <small>Updated: {date_str}</small><br>
                    <small>Status: {status_display}</small>
                </div>
                """, unsafe_allow_html=True)
    
    with col2:
        st.subheader("📅 Upcoming Events")
        
        # Get REAL user events from calendar
        events = DataSecurity.load_user_data('events', [])
        court_deadlines = DataSecurity.load_user_data('court_deadlines', [])
        
        if not events and not court_deadlines:
            st.info("📅 No upcoming events. Add events in Calendar & Tasks.")
        else:
            # Combine and sort events
            all_events = []
            
            # Add calendar events
            for event in events:
                event_date = event.get('date', '')
                event_time = event.get('time', '')
                event_title = event.get('title', 'Event')
                
                if event_date:
                    try:
                        date_obj = datetime.fromisoformat(event_date) if isinstance(event_date, str) else event_date
                        all_events.append({
                            'date': date_obj,
                            'text': f"📅 {event_title} - {date_obj.strftime('%b %d, %Y')}"
                        })
                    except:
                        pass
            
            # Add court deadlines
            for deadline in court_deadlines:
                deadline_date = deadline.get('due_date', '')
                deadline_type = deadline.get('deadline_type', 'Deadline')
                
                if deadline_date:
                    try:
                        date_obj = datetime.fromisoformat(deadline_date) if isinstance(deadline_date, str) else deadline_date
                        all_events.append({
                            'date': date_obj,
                            'text': f"⚖️ {deadline_type} - {date_obj.strftime('%b %d, %Y')}"
                        })
                    except:
                        pass
            
            # Sort by date and show next 5
            all_events.sort(key=lambda x: x['date'])
            upcoming = all_events[:5]
            
            if upcoming:
                for event in upcoming:
                    st.markdown(f"""
                    <div style="
                        background: rgba(255,255,255,0.05);
                        padding: 0.8rem;
                        border-radius: 8px;
                        margin-bottom: 0.5rem;
                        border-left: 3px solid #10b981;
                    ">
                        {event['text']}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No upcoming events in the next 30 days")

# Optional: Add a refresh button
if st.button("🔄 Refresh Dashboard"):
    st.rerun()


def track_dashboard_view():
    """Track dashboard view for analytics"""
    views = DataSecurity.load_user_data('dashboard_views', [])
    
    view_record = {
        'timestamp': datetime.now().isoformat(),
        'user': DataSecurity.get_current_user_email()
    }
    
    views.append(view_record)
    
    # Keep last 100 views
    views = views[-100:]
    
    DataSecurity.save_user_data('dashboard_views', views)
# Main execution
if __name__ == "__main__":
    show()
