import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from types import SimpleNamespace

def dict_to_obj(d):
    """Convert dict to SimpleNamespace object"""
    return SimpleNamespace(**d)

def get_attr(item, attr, default=None):
    """Helper to get attribute from dict or object"""
    if isinstance(item, dict):
        return item.get(attr, default)
    return getattr(item, attr, default)

def show():
    """Display the Time & Billing page"""
    
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
    /* Default: Light text everywhere */
    * {
        color: #e2e8f0 !important;
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
        <h1>💰 Time & Billing</h1>
        <p>Track time, generate invoices, and manage billing</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state for time entries and invoices
    if 'time_entries' not in st.session_state:
        st.session_state.time_entries = load_sample_time_entries()
    
    if 'invoices' not in st.session_state:
        st.session_state.invoices = load_sample_invoices()
    
    # Quick stats at the top
    show_billing_metrics()
    
    # Main tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "⏱️ Time Tracking", 
        "📄 Generate Invoice", 
        "💳 Invoices", 
        "📊 Reports", 
        "⚙️ Settings"
    ])
    
    with tab1:
        show_time_tracking()
    
    with tab2:
        show_invoice_generator()
    
    with tab3:
        show_invoices_list()
    
    with tab4:
        show_billing_reports()
    
    with tab5:
        show_billing_settings()

def show_billing_metrics():
    """Display billing metrics"""
    col1, col2, col3, col4 = st.columns(4)
    
    current_month = datetime.now().month
    current_year = datetime.now().year
    
    # Convert entries to objects if needed
    time_entries = [dict_to_obj(entry) if isinstance(entry, dict) else entry 
                   for entry in st.session_state.get('time_entries', [])]
    
    # Calculate metrics using getattr() and handle datetime objects
    this_month_hours = sum(
        getattr(entry, 'hours', 0) for entry in time_entries
        if isinstance(getattr(entry, 'date', None), datetime) and 
           getattr(entry, 'date').month == current_month and
           getattr(entry, 'date').year == current_year
    )
    
    this_month_revenue = sum(
        getattr(entry, 'hours', 0) * getattr(entry, 'billable_rate', getattr(entry, 'rate', 0))
        for entry in time_entries
        if isinstance(getattr(entry, 'date', None), datetime) and 
           getattr(entry, 'date').month == current_month and
           getattr(entry, 'date').year == current_year
    )
    
    total_unbilled_hours = sum(
        getattr(entry, 'hours', 0) for entry in time_entries 
        if getattr(entry, 'status', None) == "draft" and 
           getattr(entry, 'billable', False)
    )
    
    total_unbilled_revenue = sum(
        getattr(entry, 'hours', 0) * getattr(entry, 'billable_rate', getattr(entry, 'rate', 0))
        for entry in time_entries 
        if getattr(entry, 'status', None) == "draft" and 
           getattr(entry, 'billable', False)
    )
    
    with col1:
        st.metric("📊 This Month Hours", f"{this_month_hours:.1f}h")
    
    with col2:
        st.metric("💰 This Month Revenue", f"${this_month_revenue:,.2f}")
    
    with col3:
        st.metric("⏰ Unbilled Hours", f"{total_unbilled_hours:.1f}h")
    
    with col4:
        st.metric("💵 Unbilled Revenue", f"${total_unbilled_revenue:,.2f}")

def show_time_tracking():
    """Time tracking interface"""
    
    st.markdown("### ⏱️ Time Entry")
    
    # Quick timer at the top
    col_timer1, col_timer2 = st.columns([2, 1])
    
    with col_timer1:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem;
            border-radius: 16px;
            margin-bottom: 1rem;
        ">
            <h3 style="margin: 0 0 0.5rem 0;">Quick Timer</h3>
            <h1 style="margin: 0; font-size: 3rem;">00:00:00</h1>
            <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Click Start to begin tracking time</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_timer2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("▶️ Start Timer", use_container_width=True, type="primary"):
            st.info("Timer feature coming soon!")
        if st.button("⏸️ Pause", use_container_width=True):
            st.info("Timer feature coming soon!")
        if st.button("⏹️ Stop & Save", use_container_width=True):
            st.info("Timer feature coming soon!")
    
    st.markdown("---")
    
    # Manual time entry form
    st.markdown("### 📝 Manual Time Entry")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Get matters for dropdown - use get_attr helper
        matters = st.session_state.get('matters', [])
        matter_options = ["Select a matter..."] + [get_attr(m, 'name', 'Untitled') for m in matters]
        
        with st.form("time_entry_form"):
            selected_matter = st.selectbox("Matter/Case", matter_options)
            
            col_form1, col_form2 = st.columns(2)
            
            with col_form1:
                entry_date = st.date_input("Date", datetime.now())
                hours = st.number_input("Hours", min_value=0.0, max_value=24.0, step=0.25, value=1.0)
            
            with col_form2:
                activity_type = st.selectbox("Activity Type", [
                    "Client Meeting",
                    "Court Appearance",
                    "Document Review",
                    "Research",
                    "Phone Call",
                    "Email",
                    "Drafting",
                    "Travel",
                    "Other"
                ])
                rate = st.number_input("Hourly Rate ($)", min_value=0.0, step=25.0, value=250.0)
            
            description = st.text_area("Description", placeholder="Describe the work performed...")
            
            billable = st.checkbox("Billable", value=True)
            
            submitted = st.form_submit_button("💾 Save Time Entry", use_container_width=True, type="primary")
            
            if submitted:
                if selected_matter == "Select a matter...":
                    st.error("Please select a matter")
                elif not description:
                    st.error("Please provide a description")
                else:
                    # Add time entry
                    new_entry = {
                        'id': len(st.session_state.time_entries) + 1,
                        'date': entry_date.strftime('%Y-%m-%d'),
                        'matter': selected_matter,
                        'activity': activity_type,
                        'description': description,
                        'hours': hours,
                        'rate': rate,
                        'amount': hours * rate,
                        'billable': billable,
                        'billed': False,
                        'user': st.session_state.get('user_data', {}).get('name', 'Demo User')
                    }
                    
                    st.session_state.time_entries.append(new_entry)
                    st.success(f"✅ Time entry saved: {hours} hours for {selected_matter}")
                    st.rerun()
    
    with col2:
        st.markdown("### 💡 Quick Tips")
        st.info("""
        **Best Practices:**
        - Log time daily for accuracy
        - Be specific in descriptions
        - Use activity types consistently
        - Review unbilled time weekly
        """)
        
        # Quick stats
        st.markdown("### 📊 Today's Time")
        today = datetime.now().strftime('%Y-%m-%d')
        today_entries = [e for e in st.session_state.time_entries if get_attr(e, 'date', '') == today]
        today_hours = sum(get_attr(e, 'hours', 0) for e in today_entries)
        today_amount = sum(get_attr(e, 'amount', 0) for e in today_entries)
        
        st.metric("Hours Logged", f"{today_hours:.1f}")
        st.metric("Amount", f"${today_amount:,.2f}")
    
    # Recent time entries table
    st.markdown("---")
    st.markdown("### 📋 Recent Time Entries")
    
    # Filter options
    col_filter1, col_filter2, col_filter3 = st.columns(3)
    
    with col_filter1:
        filter_matter = st.selectbox("Filter by Matter", ["All"] + [get_attr(m, 'name', 'Untitled') for m in matters])
    
    with col_filter2:
        filter_status = st.selectbox("Status", ["All", "Unbilled", "Billed"])
    
    with col_filter3:
        filter_date = st.selectbox("Period", ["Last 7 days", "Last 30 days", "This Month", "All Time"])
    
    # Apply filters
    filtered_entries = st.session_state.time_entries.copy()
    
    if filter_matter != "All":
        filtered_entries = [e for e in filtered_entries if get_attr(e, 'matter', '') == filter_matter]
    
    if filter_status == "Unbilled":
        filtered_entries = [e for e in filtered_entries if not get_attr(e, 'billed', False)]
    elif filter_status == "Billed":
        filtered_entries = [e for e in filtered_entries if get_attr(e, 'billed', False)]
    
    # Display entries
    if filtered_entries:
        # Convert to regular dicts for DataFrame
        entries_data = []
        for e in filtered_entries:
            entries_data.append({
                'date': get_attr(e, 'date', ''),
                'matter': get_attr(e, 'matter', ''),
                'activity': get_attr(e, 'activity', ''),
                'description': get_attr(e, 'description', ''),
                'hours': get_attr(e, 'hours', 0),
                'rate': get_attr(e, 'rate', 0),
                'amount': get_attr(e, 'amount', 0),
                'billed': get_attr(e, 'billed', False)
            })
        
        df = pd.DataFrame(entries_data)
        df = df.sort_values('date', ascending=False)
        
        # Style the dataframe
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "date": st.column_config.DateColumn("Date", format="MMM DD, YYYY"),
                "matter": "Matter",
                "activity": "Activity",
                "description": st.column_config.TextColumn("Description", width="large"),
                "hours": st.column_config.NumberColumn("Hours", format="%.2f"),
                "rate": st.column_config.NumberColumn("Rate", format="$%.2f"),
                "amount": st.column_config.NumberColumn("Amount", format="$%.2f"),
                "billed": st.column_config.CheckboxColumn("Billed")
            }
        )
        
        # Summary
        total_hours = df['hours'].sum()
        total_amount = df['amount'].sum()
        
        st.markdown(f"""
        **Summary:** {len(df)} entries | {total_hours:.1f} hours | ${total_amount:,.2f}
        """)
    else:
        st.info("No time entries found matching your filters.")

def show_invoice_generator():
    """Invoice generation interface"""
    
    st.markdown("### 📄 Generate New Invoice")
    st.info("Invoice generation feature - Select client to see unbilled time entries")

def show_invoices_list():
    """Display list of invoices"""
    
    st.markdown("### 💳 Invoices")
    
    invoices = st.session_state.invoices
    
    if not invoices:
        st.info("No invoices yet. Generate your first invoice in the 'Generate Invoice' tab!")
        return
    
    # Display invoices
    for invoice in sorted(invoices, key=lambda x: get_attr(x, 'date', ''), reverse=True):
        status_colors = {
            'draft': '#6c757d',
            'sent': '#ffc107',
            'paid': '#28a745',
            'overdue': '#dc3545'
        }
        
        status = get_attr(invoice, 'status', 'draft')
        status_color = status_colors.get(status, '#6c757d')
        
        col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
        
        with col1:
            st.markdown(f"**{get_attr(invoice, 'invoice_number', 'N/A')}**")
            st.caption(get_attr(invoice, 'client', 'Unknown'))
        
        with col2:
            st.write(f"Date: {get_attr(invoice, 'date', 'N/A')}")
            st.caption(f"Due: {get_attr(invoice, 'due_date', 'N/A')}")
        
        with col3:
            st.markdown(f"""
            <span style="
                background: {status_color};
                color: white;
                padding: 0.25rem 0.75rem;
                border-radius: 12px;
                font-size: 0.85rem;
                font-weight: 600;
            ">{status.upper()}</span>
            """, unsafe_allow_html=True)
        
        with col4:
            st.metric("Total", f"${get_attr(invoice, 'total', 0):,.2f}")
        
        st.markdown("---")

def show_billing_reports():
    """Display billing reports and analytics"""
    
    st.markdown("### 📊 Billing Reports & Analytics")
    st.info("Comprehensive billing analytics and reports coming soon!")

def show_billing_settings():
    """Billing settings and configuration"""
    
    st.markdown("### ⚙️ Billing Settings")
    st.info("Configure billing rates, invoice templates, and payment methods")

def load_sample_time_entries():
    """Load sample time entries for demo"""
    
    sample_entries = [
        {
            'id': 1,
            'date': (datetime.now() - timedelta(days=5)).strftime('%Y-%m-%d'),
            'matter': 'Johnson Custody Case',
            'activity': 'Client Meeting',
            'description': 'Initial consultation regarding custody arrangements',
            'hours': 2.0,
            'rate': 250.0,
            'amount': 500.0,
            'billable': True,
            'billed': False,
            'user': 'John Smith'
        },
        {
            'id': 2,
            'date': (datetime.now() - timedelta(days=4)).strftime('%Y-%m-%d'),
            'matter': 'Smith Contract Dispute',
            'activity': 'Document Review',
            'description': 'Reviewed employment contracts and supporting documentation',
            'hours': 3.5,
            'rate': 250.0,
            'amount': 875.0,
            'billable': True,
            'billed': False,
            'user': 'John Smith'
        },
        {
            'id': 3,
            'date': (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d'),
            'matter': 'TechCorp Merger',
            'activity': 'Research',
            'description': 'Legal research on merger compliance requirements',
            'hours': 4.0,
            'rate': 300.0,
            'amount': 1200.0,
            'billable': True,
            'billed': True,
            'user': 'Sarah Johnson'
        },
        {
            'id': 4,
            'date': (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d'),
            'matter': 'Johnson Custody Case',
            'activity': 'Phone Call',
            'description': 'Phone conference with opposing counsel',
            'hours': 0.5,
            'rate': 150.0,
            'amount': 75.0,
            'billable': True,
            'billed': False,
            'user': 'John Smith'
        },
        {
            'id': 5,
            'date': (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'),
            'matter': 'Smith Contract Dispute',
            'activity': 'Drafting',
            'description': 'Drafted response to opposing counsel demands',
            'hours': 2.5,
            'rate': 250.0,
            'amount': 625.0,
            'billable': True,
            'billed': False,
            'user': 'John Smith'
        },
        {
            'id': 6,
            'date': datetime.now().strftime('%Y-%m-%d'),
            'matter': 'TechCorp Merger',
            'activity': 'Email',
            'description': 'Email correspondence with client regarding due diligence',
            'hours': 0.25,
            'rate': 150.0,
            'amount': 37.5,
            'billable': True,
            'billed': False,
            'user': 'Sarah Johnson'
        },
        {
            'id': 7,
            'date': (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d'),
            'matter': 'Anderson Real Estate',
            'activity': 'Court Appearance',
            'description': 'Hearing on motion for summary judgment',
            'hours': 3.0,
            'rate': 350.0,
            'amount': 1050.0,
            'billable': True,
            'billed': True,
            'user': 'Michael Davis'
        },
        {
            'id': 8,
            'date': (datetime.now() - timedelta(days=6)).strftime('%Y-%m-%d'),
            'matter': 'Johnson Custody Case',
            'activity': 'Document Review',
            'description': 'Reviewed financial disclosures and custody evaluation',
            'hours': 1.5,
            'rate': 250.0,
            'amount': 375.0,
            'billable': True,
            'billed': False,
            'user': 'John Smith'
        }
    ]
    
    return sample_entries

def load_sample_invoices():
    """Load sample invoices for demo"""
    
    sample_invoices = [
        {
            'id': 1,
            'invoice_number': 'INV-20251001-001',
            'client': 'TechCorp Industries',
            'date': '2025-10-01',
            'due_date': '2025-10-31',
            'subtotal': 2400.0,
            'tax': 0.0,
            'discount': 0.0,
            'total': 2400.0,
            'status': 'paid',
            'payment_terms': 'Net 30',
            'notes': 'Thank you for your business.',
            'entries': []
        },
        {
            'id': 2,
            'invoice_number': 'INV-20251005-002',
            'client': 'Anderson Real Estate LLC',
            'date': '2025-10-05',
            'due_date': '2025-11-04',
            'subtotal': 1575.0,
            'tax': 0.0,
            'discount': 0.0,
            'total': 1575.0,
            'status': 'sent',
            'payment_terms': 'Net 30',
            'notes': 'Payment due within 30 days.',
            'entries': []
        },
        {
            'id': 3,
            'invoice_number': 'INV-20251010-003',
            'client': 'Smith & Associates',
            'date': '2025-10-10',
            'due_date': '2025-11-09',
            'subtotal': 3250.0,
            'tax': 0.0,
            'discount': 100.0,
            'total': 3150.0,
            'status': 'sent',
            'payment_terms': 'Net 30',
            'notes': 'Volume discount applied.',
            'entries': []
        },
        {
            'id': 4,
            'invoice_number': 'INV-20251012-004',
            'client': 'Johnson Family Trust',
            'date': '2025-10-12',
            'due_date': '2025-11-11',
            'subtotal': 950.0,
            'tax': 0.0,
            'discount': 0.0,
            'total': 950.0,
            'status': 'draft',
            'payment_terms': 'Net 30',
            'notes': '',
            'entries': []
        }
    ]
    
    return sample_invoices

if __name__ == "__main__":
    show()
