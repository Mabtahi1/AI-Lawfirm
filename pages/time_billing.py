import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from types import SimpleNamespace
import json
import os

# ADD THIS:
from services.data_security import DataSecurity

# DELETE these old functions:
# - DATA_DIR = "user_data"
# - ensure_data_dir()
# - get_user_file()
# - save_user_data()
# - load_user_data()

# REPLACE auto_save_user_data with:
def auto_save_user_data():
    """SECURE auto-save billing data"""
    if 'time_entries' in st.session_state:
        DataSecurity.save_user_data('time_entries', st.session_state.time_entries)
    
    if 'invoices' in st.session_state:
        DataSecurity.save_user_data('invoices', st.session_state.invoices)
    
    if 'matters' in st.session_state:
        DataSecurity.save_user_data('matters', st.session_state.matters)
    
    if 'billing_settings' in st.session_state:
        DataSecurity.save_user_data('billing_settings', st.session_state.billing_settings)

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
    
    # Require authentication
    DataSecurity.require_auth("Time & Billing")
    
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
        <h1>💰 Time & Billing</h1>
        <p>Track time, generate invoices, and manage billing</p>
    </div>
    """, unsafe_allow_html=True)
    
    # GET USER EMAIL FOR DATA PERSISTENCE
    user_email = st.session_state.get('user_data', {}).get('email', 'demo@example.com')
    
    # LOAD REAL USER DATA (NO MOCK DATA)
    if 'time_entries' not in st.session_state:
        st.session_state.time_entries = DataSecurity.get_user_time_entries()
    
    if 'invoices' not in st.session_state:
        st.session_state.invoices = DataSecurity.get_user_invoices()
    
    if 'matters' not in st.session_state:
        st.session_state.matters = DataSecurity.get_user_matters()
    
    if 'billing_settings' not in st.session_state:
        st.session_state.billing_settings = DataSecurity.load_user_data('billing_settings', {
            'default_rate': 250.0,
            'paralegal_rate': 150.0,
            'associate_rate': 300.0,
            'partner_rate': 450.0,
            'senior_partner_rate': 600.0,
            'court_appearance_rate': 500.0,
            'firm_name': '',
            'firm_address': '',
            'firm_phone': '',
            'firm_email': '',
            'invoice_prefix': 'INV',
            'payment_terms': 'Net 30',
            'include_tax': False,
            'tax_rate': 0.0,
            'invoice_footer': 'Thank you for your business.',
            'accept_check': True,
            'accept_wire': True,
            'accept_credit': True,
            'accept_ach': True,
            'charge_late_fees': False,
            'late_fee_percent': 1.5,
            'grace_period': 5
        })
    
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
    
    # ✅ FIX: Handle both datetime objects and strings
    def get_entry_date(entry):
        """Safely get datetime from entry"""
        date_val = getattr(entry, 'date', None)
        if isinstance(date_val, str):
            try:
                return datetime.strptime(date_val, '%Y-%m-%d')
            except:
                return None
        elif isinstance(date_val, datetime):
            return date_val
        return None
    
    # Calculate metrics using safe date comparison
    this_month_hours = sum(
        getattr(entry, 'hours', 0) for entry in time_entries
        if (entry_date := get_entry_date(entry)) and 
           entry_date.month == current_month and
           entry_date.year == current_year
    )
    
    this_month_revenue = sum(
        getattr(entry, 'hours', 0) * getattr(entry, 'rate', 0)
        for entry in time_entries
        if (entry_date := get_entry_date(entry)) and 
           entry_date.month == current_month and
           entry_date.year == current_year
    )
    
    total_unbilled_hours = sum(
        getattr(entry, 'hours', 0) for entry in time_entries 
        if not getattr(entry, 'billed', False) and 
           getattr(entry, 'billable', False)
    )
    
    total_unbilled_revenue = sum(
        getattr(entry, 'hours', 0) * getattr(entry, 'rate', 0)
        for entry in time_entries 
        if not getattr(entry, 'billed', False) and 
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
    
    # Check if user has matters
    if not st.session_state.matters:
        st.warning("⚠️ You don't have any matters yet. Please create a matter in the Matter Management page first.")
        if st.button("Go to Matter Management"):
            st.switch_page("pages/matters.py")
        return
    
    # Quick timer at the top
    col_timer1, col_timer2 = st.columns([2, 1])
    
    # Initialize timer state
    if 'timer_running' not in st.session_state:
        st.session_state.timer_running = False
    if 'timer_start' not in st.session_state:
        st.session_state.timer_start = None
    if 'timer_elapsed' not in st.session_state:
        st.session_state.timer_elapsed = 0
    if 'timer_paused_time' not in st.session_state:
        st.session_state.timer_paused_time = 0
    
    # Calculate elapsed time
    if st.session_state.timer_running and st.session_state.timer_start:
        elapsed_seconds = int((datetime.now() - st.session_state.timer_start).total_seconds()) + st.session_state.timer_paused_time
    else:
        elapsed_seconds = st.session_state.timer_paused_time
    
    hours = elapsed_seconds // 3600
    minutes = (elapsed_seconds % 3600) // 60
    seconds = elapsed_seconds % 60
    timer_display = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    with col_timer1:
        timer_color = "#10b981" if st.session_state.timer_running else "#667eea"
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, {timer_color} 0%, #764ba2 100%);
            color: white;
            padding: 2rem;
            border-radius: 16px;
            margin-bottom: 1rem;
        ">
            <h3 style="margin: 0 0 0.5rem 0;">Quick Timer {'🟢 RUNNING' if st.session_state.timer_running else '⏸️ STOPPED'}</h3>
            <h1 style="margin: 0; font-size: 3rem;">{timer_display}</h1>
            <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">
                {'Timer is running - click Pause or Stop' if st.session_state.timer_running else 'Click Start to begin tracking time'}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_timer2:
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Start button
        if not st.session_state.timer_running:
            if st.button("▶️ Start Timer", use_container_width=True, type="primary"):
                st.session_state.timer_running = True
                st.session_state.timer_start = datetime.now()
                st.success("✓ Timer started!")
                st.rerun()
        
        # Pause button
        if st.session_state.timer_running:
            if st.button("⏸️ Pause", use_container_width=True):
                st.session_state.timer_running = False
                if st.session_state.timer_start:
                    st.session_state.timer_paused_time += int((datetime.now() - st.session_state.timer_start).total_seconds())
                st.session_state.timer_start = None
                st.warning("Timer paused")
                st.rerun()
        
        # Stop & Save button
        if st.button("⏹️ Stop & Save", use_container_width=True):
            # Calculate final time
            if st.session_state.timer_running and st.session_state.timer_start:
                final_seconds = int((datetime.now() - st.session_state.timer_start).total_seconds()) + st.session_state.timer_paused_time
            else:
                final_seconds = st.session_state.timer_paused_time
            
            final_hours = round(final_seconds / 3600, 2)
            
            # Get current timer data
            timer_matter = st.session_state.get('timer_matter_select', 'Select matter...')
            timer_activity = st.session_state.get('timer_activity_select', 'Other')
            timer_desc = st.session_state.get('timer_desc', '')
            
            # Validate data
            if timer_matter != "Select matter..." and final_hours > 0:
                # Get default rate from settings
                default_rate = st.session_state.billing_settings.get('default_rate', 250.0)
                
                # ✅ FIX: Use string format for date consistently
                new_entry = {
                    'id': len(st.session_state.time_entries) + 1,
                    'date': datetime.now().strftime('%Y-%m-%d'),  # ✅ String format
                    'matter': timer_matter,
                    'activity': timer_activity,
                    'description': timer_desc if timer_desc else f"Timer entry - {timer_activity}",
                    'hours': final_hours,
                    'rate': default_rate,
                    'amount': final_hours * default_rate,
                    'billable': True,
                    'billed': False,
                    'user': st.session_state.get('user_data', {}).get('name', 'User')
                }
                
                st.session_state.time_entries.append(new_entry)
                auto_save_user_data()
                
                # Reset timer
                st.session_state.timer_running = False
                st.session_state.timer_start = None
                st.session_state.timer_paused_time = 0
                
                st.success(f"✅ Timer saved! {final_hours} hours added to {timer_matter}")
                st.rerun()
            else:
                st.error("⚠️ Please select a matter before saving timer")
                # Reset timer anyway
                st.session_state.timer_running = False
                st.session_state.timer_start = None
                st.session_state.timer_paused_time = 0
                st.rerun()
    
    # Auto-refresh timer display when running
    if st.session_state.timer_running:
        import time
        time.sleep(0.1)
        st.rerun()
    
    st.markdown("---")
    st.markdown("#### What are you working on?")
    col_matter, col_activity = st.columns(2)
    
    with col_matter:
        matters = st.session_state.get('matters', [])
        matter_options = ["Select matter..."] + [get_attr(m, 'name', 'Untitled') for m in matters]
        timer_matter = st.selectbox("Matter", matter_options, key="timer_matter_select")
    
    with col_activity:
        timer_activity = st.selectbox("Activity", [
            "Client Meeting",
            "Court Appearance", 
            "Document Review",
            "Research",
            "Phone Call",
            "Email",
            "Drafting",
            "Travel",
            "Other"
        ], key="timer_activity_select")
    
    timer_description = st.text_input("Quick description (optional)", key="timer_desc", placeholder="What are you working on?")
    
    # Manual time entry form
    st.markdown("### 📝 Manual Time Entry")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Get matters for dropdown
        matters = st.session_state.get('matters', [])
        matter_options = ["Select a matter..."] + [get_attr(m, 'name', 'Untitled') for m in matters]
        
        with st.form("time_entry_form"):
            selected_matter = st.selectbox("Matter/Case", matter_options)
            
            col_form1, col_form2 = st.columns(2)
            
            with col_form1:
                entry_date = st.date_input("Date", datetime.now())
                
                # Get default rate from settings
                default_rate = st.session_state.billing_settings.get('default_rate', 250.0)
                
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
                rate = st.number_input("Hourly Rate ($)", min_value=0.0, step=25.0, value=default_rate)
            
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
                        'user': st.session_state.get('user_data', {}).get('name', 'User')
                    }
                    
                    st.session_state.time_entries.append(new_entry)
                    auto_save_user_data()
                    
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
                'Date': get_attr(e, 'date', ''),
                'Matter': get_attr(e, 'matter', ''),
                'Activity': get_attr(e, 'activity', ''),
                'Description': get_attr(e, 'description', ''),
                'Hours': get_attr(e, 'hours', 0),
                'Rate': get_attr(e, 'rate', 0),
                'Amount': get_attr(e, 'amount', 0),
                'Billed': '✓' if get_attr(e, 'billed', False) else '✗'
            })
        
        df = pd.DataFrame(entries_data)
        df = df.sort_values('Date', ascending=False)
        
        # Style the dataframe
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )
        
        # Summary
        total_hours = sum(get_attr(e, 'hours', 0) for e in filtered_entries)
        total_amount = sum(get_attr(e, 'amount', 0) for e in filtered_entries)
        
        st.markdown(f"""
        **Summary:** {len(df)} entries | {total_hours:.1f} hours | ${total_amount:,.2f}
        """)
    else:
        st.info("No time entries found. Start tracking your time above!")

def show_invoice_generator():
    """Invoice generation interface"""
    
    st.markdown("### 📄 Generate New Invoice")
    
    # Get unbilled time entries
    unbilled_entries = [e for e in st.session_state.time_entries 
                       if get_attr(e, 'billable', False) and not get_attr(e, 'billed', False)]
    
    if not unbilled_entries:
        st.info("💡 No unbilled time entries available. Log billable time in the Time Tracking tab first.")
        return
    
    # Group by matter
    matters_with_unbilled = {}
    for entry in unbilled_entries:
        matter = get_attr(entry, 'matter', 'Unknown')
        if matter not in matters_with_unbilled:
            matters_with_unbilled[matter] = []
        matters_with_unbilled[matter].append(entry)
    
    # Invoice form
    with st.form("invoice_generator_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            selected_client = st.selectbox("Select Client/Matter", list(matters_with_unbilled.keys()))
            invoice_date = st.date_input("Invoice Date", datetime.now())
            due_date = st.date_input("Due Date", datetime.now() + timedelta(days=30))
        
        with col2:
            payment_terms = st.selectbox("Payment Terms", 
                ["Net 30", "Net 15", "Due on Receipt", "Net 60"],
                index=0 if st.session_state.billing_settings.get('payment_terms') == 'Net 30' else 0)
            invoice_notes = st.text_area("Invoice Notes", 
                value=st.session_state.billing_settings.get('invoice_footer', 'Thank you for your business.'),
                placeholder="Thank you for your business...")
            discount_percent = st.number_input("Discount (%)", min_value=0.0, max_value=100.0, step=5.0, value=0.0)
        
        # Show unbilled entries for selected client
        st.markdown("#### Unbilled Time Entries")
        
        selected_entries = matters_with_unbilled.get(selected_client, [])
        
        if selected_entries:
            # Create selection checkboxes
            st.markdown("Select entries to include:")
            selected_entry_ids = []
            
            for entry in selected_entries:
                entry_id = get_attr(entry, 'id', 0)
                entry_date = get_attr(entry, 'date', '')
                entry_activity = get_attr(entry, 'activity', '')
                entry_hours = get_attr(entry, 'hours', 0)
                entry_amount = get_attr(entry, 'amount', 0)
                entry_desc = get_attr(entry, 'description', '')
                
                include = st.checkbox(
                    f"{entry_date} - {entry_activity} ({entry_hours}h) - ${entry_amount:.2f}",
                    value=True,
                    key=f"entry_{entry_id}"
                )
                
                if include:
                    selected_entry_ids.append(entry_id)
                    st.caption(entry_desc)
            
            # Calculate totals
            subtotal = sum(get_attr(e, 'amount', 0) for e in selected_entries if get_attr(e, 'id', 0) in selected_entry_ids)
            discount_amount = subtotal * (discount_percent / 100)
            total = subtotal - discount_amount
            
            st.markdown("---")
            col_total1, col_total2 = st.columns([3, 1])
            
            with col_total2:
                st.metric("Subtotal", f"${subtotal:.2f}")
                if discount_amount > 0:
                    st.metric("Discount", f"-${discount_amount:.2f}")
                st.metric("**Total**", f"**${total:.2f}**")
        
        # Generate button
        if st.form_submit_button("📄 Generate Invoice", type="primary", use_container_width=True):
            if not selected_entry_ids:
                st.error("Please select at least one time entry")
            else:
                # Create invoice
                invoice_prefix = st.session_state.billing_settings.get('invoice_prefix', 'INV')
                invoice_number = f"{invoice_prefix}-{datetime.now().strftime('%Y%m%d')}-{len(st.session_state.invoices) + 1:03d}"
                
                new_invoice = {
                    'id': len(st.session_state.invoices) + 1,
                    'invoice_number': invoice_number,
                    'client': selected_client,
                    'date': invoice_date.strftime('%Y-%m-%d'),
                    'due_date': due_date.strftime('%Y-%m-%d'),
                    'subtotal': subtotal,
                    'discount': discount_amount,
                    'total': total,
                    'status': 'draft',
                    'payment_terms': payment_terms,
                    'notes': invoice_notes,
                    'entries': selected_entry_ids
                }
                
                st.session_state.invoices.append(new_invoice)
                
                # Mark entries as billed
                for entry in st.session_state.time_entries:
                    if get_attr(entry, 'id', 0) in selected_entry_ids:
                        if isinstance(entry, dict):
                            entry['billed'] = True
                        else:
                            entry.billed = True
                
                auto_save_user_data()
                
                st.success(f"✅ Invoice {invoice_number} created successfully!")
                st.balloons()
                
                # Show download option
                st.info("💡 View your invoice in the 'Invoices' tab")
                st.rerun()

def show_invoices_list():
    """Display list of invoices"""
    
    st.markdown("### 💳 Invoices")
    
    invoices = st.session_state.invoices
    
    if not invoices:
        st.info("📄 No invoices yet. Generate your first invoice in the 'Generate Invoice' tab!")
        return
    
    # Invoice actions
    col_action1, col_action2 = st.columns([3, 1])
    with col_action2:
        if st.button("➕ New Invoice"):
            st.info("Go to 'Generate Invoice' tab to create a new invoice")
    
    st.markdown("---")
    
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
        
        with st.expander(f"📄 {get_attr(invoice, 'invoice_number', 'N/A')} - {get_attr(invoice, 'client', 'Unknown')} - ${get_attr(invoice, 'total', 0):,.2f}"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"**Invoice:** {get_attr(invoice, 'invoice_number', 'N/A')}")
                st.markdown(f"**Client:** {get_attr(invoice, 'client', 'Unknown')}")
                st.markdown(f"**Date:** {get_attr(invoice, 'date', 'N/A')}")
            
            with col2:
                st.markdown(f"**Due Date:** {get_attr(invoice, 'due_date', 'N/A')}")
                st.markdown(f"**Terms:** {get_attr(invoice, 'payment_terms', 'N/A')}")
                st.markdown(f"""**Status:** <span style="background: {status_color}; color: white; padding: 0.25rem 0.75rem; border-radius: 12px; font-size: 0.85rem;">{status.upper()}</span>""", unsafe_allow_html=True)
            
            with col3:
                st.metric("Subtotal", f"${get_attr(invoice, 'subtotal', 0):,.2f}")
                if get_attr(invoice, 'discount', 0) > 0:
                    st.metric("Discount", f"-${get_attr(invoice, 'discount', 0):,.2f}")
                st.metric("**Total**", f"**${get_attr(invoice, 'total', 0):,.2f}**")
            
            # Invoice actions
            col_btn1, col_btn2, col_btn3, col_btn4 = st.columns(4)
            
            with col_btn1:
                if st.button("📧 Send", key=f"send_{get_attr(invoice, 'id')}"):
                    if isinstance(invoice, dict):
                        invoice['status'] = 'sent'
                    else:
                        invoice.status = 'sent'
                    auto_save_user_data()
                    st.success("Invoice marked as sent!")
                    st.rerun()
            
            with col_btn2:
                if st.button("✅ Mark Paid", key=f"paid_{get_attr(invoice, 'id')}"):
                    if isinstance(invoice, dict):
                        invoice['status'] = 'paid'
                    else:
                        invoice.status = 'paid'
                    auto_save_user_data()
                    st.success("Invoice marked as paid!")
                    st.rerun()
            
            with col_btn3:
                if st.button("📥 Download PDF", key=f"download_{get_attr(invoice, 'id')}"):
                    st.info("PDF download feature coming soon!")
            
            with col_btn4:
                if st.button("🗑️ Delete", key=f"delete_{get_attr(invoice, 'id')}"):
                    st.session_state.invoices.remove(invoice)
                    auto_save_user_data()
                    st.success("Invoice deleted!")
                    st.rerun()

def show_billing_reports():
    """Display billing reports and analytics"""
    
    st.markdown("### 📊 Billing Reports & Analytics")
    
    if not st.session_state.time_entries:
        st.info("📈 No data yet. Start logging time to see reports!")
        return
    
    # Date range selector
    col1, col2 = st.columns(2)
    
    with col1:
        report_period = st.selectbox("Report Period", [
            "This Month",
            "Last Month", 
            "Last 3 Months",
            "Last 6 Months",
            "This Year",
            "All Time"
        ])
    
    with col2:
        report_type = st.selectbox("Report Type", [
            "Revenue Summary",
            "Time by Matter",
            "Time by Attorney",
            "Billable vs Non-Billable"
        ])
    
    # Summary metrics
    col_met1, col_met2, col_met3, col_met4 = st.columns(4)
    
    time_entries = [dict_to_obj(e) if isinstance(e, dict) else e for e in st.session_state.time_entries]
    
    total_hours = sum(getattr(e, 'hours', 0) for e in time_entries)
    total_revenue = sum(getattr(e, 'amount', 0) for e in time_entries)
    billable_hours = sum(getattr(e, 'hours', 0) for e in time_entries if getattr(e, 'billable', False))
    avg_rate = total_revenue / total_hours if total_hours > 0 else 0
    
    with col_met1:
        st.metric("Total Hours", f"{total_hours:.1f}h")
    
    with col_met2:
        st.metric("Total Revenue", f"${total_revenue:,.2f}")
    
    with col_met3:
        st.metric("Billable Hours", f"{billable_hours:.1f}h")
    
    with col_met4:
        st.metric("Avg Rate", f"${avg_rate:.2f}/h")
    
    st.markdown("---")
    
    # Show report based on selection
    if report_type == "Revenue Summary":
        st.markdown("#### 💰 Revenue Summary")
        
        # Group by month
        revenue_by_month = {}
        for entry in time_entries:
            entry_date = getattr(entry, 'date', '')
            if entry_date:
                month = entry_date[:7]  # YYYY-MM
                revenue_by_month[month] = revenue_by_month.get(month, 0) + getattr(entry, 'amount', 0)
        
        if revenue_by_month:
            df = pd.DataFrame(list(revenue_by_month.items()), columns=['Month', 'Revenue'])
            df = df.sort_values('Month')
            
            fig = px.bar(df, x='Month', y='Revenue', title='Revenue by Month')
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            st.plotly_chart(fig, use_container_width=True)
            
            st.dataframe(df, use_container_width=True, hide_index=True)
    
    elif report_type == "Time by Matter":
        st.markdown("#### ⚖️ Time by Matter")
        
        # Group by matter
        time_by_matter = {}
        for entry in time_entries:
            matter = getattr(entry, 'matter', 'Unknown')
            time_by_matter[matter] = time_by_matter.get(matter, 0) + getattr(entry, 'hours', 0)
        
        if time_by_matter:
            df = pd.DataFrame(list(time_by_matter.items()), columns=['Matter', 'Hours'])
            df = df.sort_values('Hours', ascending=False)
            
            fig = px.pie(df, values='Hours', names='Matter', title='Time Distribution by Matter')
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            st.plotly_chart(fig, use_container_width=True)
            
            st.dataframe(df, use_container_width=True, hide_index=True)
    
    elif report_type == "Time by Attorney":
        st.markdown("#### 👨‍⚖️ Time by Attorney")
        
        # Group by user
        time_by_user = {}
        for entry in time_entries:
            user = getattr(entry, 'user', 'Unknown')
            time_by_user[user] = time_by_user.get(user, 0) + getattr(entry, 'hours', 0)
        
        if time_by_user:
            df = pd.DataFrame(list(time_by_user.items()), columns=['Attorney', 'Hours'])
            df = df.sort_values('Hours', ascending=False)
            
            fig = px.bar(df, x='Attorney', y='Hours', title='Time by Attorney')
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            st.plotly_chart(fig, use_container_width=True)
            
            st.dataframe(df, use_container_width=True, hide_index=True)
    
    elif report_type == "Billable vs Non-Billable":
        st.markdown("#### 💼 Billable vs Non-Billable")
        
        billable = sum(getattr(e, 'hours', 0) for e in time_entries if getattr(e, 'billable', False))
        non_billable = sum(getattr(e, 'hours', 0) for e in time_entries if not getattr(e, 'billable', False))
        
        df = pd.DataFrame({
            'Type': ['Billable', 'Non-Billable'],
            'Hours': [billable, non_billable]
        })
        
        fig = px.pie(df, values='Hours', names='Type', title='Billable vs Non-Billable Hours')
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        st.plotly_chart(fig, use_container_width=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Billable Hours", f"{billable:.1f}h")
        with col2:
            st.metric("Non-Billable Hours", f"{non_billable:.1f}h")

def show_billing_settings():
    """Billing settings and configuration"""
    
    st.markdown("### ⚙️ Billing Settings")
    
    tab1, tab2, tab3 = st.tabs(["💰 Rates", "📄 Invoice Templates", "💳 Payment"])
    
    with tab1:
        st.markdown("#### Default Billing Rates")
        
        col1, col2 = st.columns(2)
        
        with col1:
            default_rate = st.number_input("Default Hourly Rate ($)", 
                min_value=0.0, step=25.0, 
                value=st.session_state.billing_settings.get('default_rate', 250.0))
            
            paralegal_rate = st.number_input("Paralegal Rate ($)", 
                min_value=0.0, step=25.0, 
                value=st.session_state.billing_settings.get('paralegal_rate', 150.0))
            
            associate_rate = st.number_input("Associate Rate ($)", 
                min_value=0.0, step=25.0, 
                value=st.session_state.billing_settings.get('associate_rate', 300.0))
        
        with col2:
            partner_rate = st.number_input("Partner Rate ($)", 
                min_value=0.0, step=25.0, 
                value=st.session_state.billing_settings.get('partner_rate', 450.0))
            
            senior_partner_rate = st.number_input("Senior Partner Rate ($)", 
                min_value=0.0, step=25.0, 
                value=st.session_state.billing_settings.get('senior_partner_rate', 600.0))
            
            court_appearance_rate = st.number_input("Court Appearance Rate ($)", 
                min_value=0.0, step=25.0, 
                value=st.session_state.billing_settings.get('court_appearance_rate', 500.0))
        
        if st.button("💾 Save Rates", type="primary"):
            st.session_state.billing_settings.update({
                'default_rate': default_rate,
                'paralegal_rate': paralegal_rate,
                'associate_rate': associate_rate,
                'partner_rate': partner_rate,
                'senior_partner_rate': senior_partner_rate,
                'court_appearance_rate': court_appearance_rate
            })
            auto_save_user_data()
            st.success("✅ Billing rates saved successfully!")
            st.rerun()
    
    with tab2:
        st.markdown("#### Invoice Template Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            firm_name = st.text_input("Firm Name", 
                value=st.session_state.billing_settings.get('firm_name', ''))
            
            firm_address = st.text_area("Firm Address", 
                value=st.session_state.billing_settings.get('firm_address', ''))
            
            firm_phone = st.text_input("Phone", 
                value=st.session_state.billing_settings.get('firm_phone', ''))
            
            firm_email = st.text_input("Email", 
                value=st.session_state.billing_settings.get('firm_email', ''))
        
        with col2:
            invoice_prefix = st.text_input("Invoice Number Prefix", 
                value=st.session_state.billing_settings.get('invoice_prefix', 'INV'))
            
            default_payment_terms = st.selectbox("Default Payment Terms", 
                ["Net 30", "Net 15", "Due on Receipt", "Net 60"],
                index=["Net 30", "Net 15", "Due on Receipt", "Net 60"].index(
                    st.session_state.billing_settings.get('payment_terms', 'Net 30')))
            
            include_tax = st.checkbox("Include Tax on Invoices", 
                value=st.session_state.billing_settings.get('include_tax', False))
            
            if include_tax:
                tax_rate = st.number_input("Tax Rate (%)", 
                    min_value=0.0, max_value=100.0, 
                    value=st.session_state.billing_settings.get('tax_rate', 8.5))
        
        st.markdown("#### Invoice Footer")
        invoice_footer = st.text_area("Footer Text", 
            value=st.session_state.billing_settings.get('invoice_footer', 
                'Thank you for your business.\nPayment is due within the terms specified above.'))
        
        if st.button("💾 Save Template Settings", type="primary"):
            st.session_state.billing_settings.update({
                'firm_name': firm_name,
                'firm_address': firm_address,
                'firm_phone': firm_phone,
                'firm_email': firm_email,
                'invoice_prefix': invoice_prefix,
                'payment_terms': default_payment_terms,
                'include_tax': include_tax,
                'invoice_footer': invoice_footer
            })
            if include_tax:
                st.session_state.billing_settings['tax_rate'] = tax_rate
            auto_save_user_data()
            st.success("✅ Invoice template settings saved!")
            st.rerun()
    
    with tab3:
        st.markdown("#### Payment Methods")
        
        st.info("💡 Configure accepted payment methods for invoices")
        
        accept_check = st.checkbox("Accept Checks", 
            value=st.session_state.billing_settings.get('accept_check', True))
        accept_wire = st.checkbox("Accept Wire Transfer", 
            value=st.session_state.billing_settings.get('accept_wire', True))
        accept_credit = st.checkbox("Accept Credit Cards", 
            value=st.session_state.billing_settings.get('accept_credit', True))
        accept_ach = st.checkbox("Accept ACH/Direct Deposit", 
            value=st.session_state.billing_settings.get('accept_ach', True))
        
        if accept_wire:
            st.markdown("**Wire Transfer Information**")
            bank_name = st.text_input("Bank Name", 
                value=st.session_state.billing_settings.get('bank_name', ''))
            routing_number = st.text_input("Routing Number", 
                value=st.session_state.billing_settings.get('routing_number', ''))
            account_number = st.text_input("Account Number", 
                value=st.session_state.billing_settings.get('account_number', ''), 
                type="password")
        
        st.markdown("#### Late Payment Settings")
        charge_late_fees = st.checkbox("Charge Late Fees", 
            value=st.session_state.billing_settings.get('charge_late_fees', False))
        
        if charge_late_fees:
            late_fee_percent = st.number_input("Late Fee Percentage", 
                min_value=0.0, max_value=25.0, 
                value=st.session_state.billing_settings.get('late_fee_percent', 1.5))
            grace_period = st.number_input("Grace Period (days)", 
                min_value=0, 
                value=st.session_state.billing_settings.get('grace_period', 5))
        
        if st.button("💾 Save Payment Settings", type="primary"):
            st.session_state.billing_settings.update({
                'accept_check': accept_check,
                'accept_wire': accept_wire,
                'accept_credit': accept_credit,
                'accept_ach': accept_ach,
                'charge_late_fees': charge_late_fees
            })
            if accept_wire:
                st.session_state.billing_settings.update({
                    'bank_name': bank_name,
                    'routing_number': routing_number,
                    'account_number': account_number
                })
            if charge_late_fees:
                st.session_state.billing_settings.update({
                    'late_fee_percent': late_fee_percent,
                    'grace_period': grace_period
                })
            auto_save_user_data()
            st.success("✅ Payment settings saved!")
            st.rerun()

if __name__ == "__main__":
    show()
