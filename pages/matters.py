# pages/matters.py - Enhanced Matter Management Interface
import streamlit as st
import uuid
import time
from datetime import datetime, timedelta
import pandas as pd
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from enum import Enum
from types import SimpleNamespace

def dict_to_obj(d):
    return SimpleNamespace(**d)

def get_attr(item, attr, default=None):
    """Helper to get attribute from dict or object"""
    if isinstance(item, dict):
        return item.get(attr, default)
    return getattr(item, attr, default)

def set_attr(item, attr, value):
    """Helper to set attribute on dict or object"""
    if isinstance(item, dict):
        item[attr] = value
    else:
        setattr(item, attr, value)

class MatterType(Enum):
    LITIGATION = "litigation"
    CORPORATE = "corporate"
    REAL_ESTATE = "real_estate"
    INTELLECTUAL_PROPERTY = "intellectual_property"
    EMPLOYMENT = "employment"
    TAX = "tax"
    FAMILY = "family"
    CRIMINAL = "criminal"
    IMMIGRATION = "immigration"
    BANKRUPTCY = "bankruptcy"
    CONTRACT = "contract"
    MERGERS_ACQUISITIONS = "mergers_acquisitions"

class MatterStatus(Enum):
    ACTIVE = "active"
    ON_HOLD = "on_hold"
    CLOSED = "closed"
    ARCHIVED = "archived"
    CANCELLED = "cancelled"

class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class Task:
    id: str = ""
    matter_id: str = ""
    title: str = ""
    description: str = ""
    assigned_to: str = ""
    due_date: datetime = field(default_factory=datetime.now)
    status: str = "pending"
    priority: str = "medium"
    created_date: datetime = field(default_factory=datetime.now)
    completed_date: Optional[datetime] = None
    estimated_hours: float = 0.0
    actual_hours: float = 0.0

@dataclass
class TimeEntry:
    id: str = ""
    matter_id: str = ""
    attorney_email: str = ""
    date: datetime = field(default_factory=datetime.now)
    hours: float = 0.0
    description: str = ""
    billable_rate: float = 250.0
    task_id: Optional[str] = None

@dataclass
class MatterExpense:
    id: str = ""
    matter_id: str = ""
    date: datetime = field(default_factory=datetime.now)
    amount: float = 0.0
    description: str = ""
    category: str = "general"
    is_billable: bool = True
    receipt_attached: bool = False

@dataclass
class Matter:
    id: str = ""
    name: str = ""
    client_id: str = ""
    client_name: str = ""
    matter_type: str = ""
    status: str = ""
    created_date: datetime = field(default_factory=datetime.now)
    assigned_attorneys: List[str] = field(default_factory=list)
    description: str = ""
    budget: float = 0.0
    estimated_hours: float = 0.0
    actual_hours: float = 0.0
    hourly_rate: float = 250.0
    priority: str = "medium"
    deadline: Optional[datetime] = None
    closed_date: Optional[datetime] = None
    billing_contact: str = ""
    tags: List[str] = field(default_factory=list)
    custom_fields: Dict[str, Any] = field(default_factory=dict)

# Import auth service
try:
    from services.auth import AuthService
except ImportError:
    class AuthService:
        def has_permission(self, perm):
            return True


def create_new_user():
    from services.subscription_manager import EnhancedAuthService
    auth_service = EnhancedAuthService()
    
    if not auth_service.check_user_limit_before_invite():
        st.error("User limit reached for your current plan.")
        current_plan = st.session_state.user_data.get('organization_code')
        subscription = auth_service.subscription_manager.get_organization_subscription(current_plan)
        limits = auth_service.subscription_manager.get_plan_limits(subscription['plan'])
        
        st.info(f"Your {subscription['plan'].title()} plan allows {limits['max_users']} users.")
        
        if st.button("Upgrade Plan"):
            st.session_state['show_upgrade_modal'] = True
            st.rerun()
        return


def initialize_matter_session_state():
    """Initialize matter-related session state"""
    if 'matters' not in st.session_state:
        st.session_state.matters = []
    
    if 'tasks' not in st.session_state:
        st.session_state.tasks = []
    
    if 'time_entries' not in st.session_state:
        st.session_state.time_entries = []
    
    if 'matter_expenses' not in st.session_state:
        st.session_state.matter_expenses = []
    
    # Sample data for demo
    if not st.session_state.matters:
        sample_matters = [
            Matter(
                id=str(uuid.uuid4()),
                name="Software License Agreement",
                client_id=str(uuid.uuid4()),
                client_name="TechCorp Inc",
                matter_type="contract",
                status="active",
                created_date=datetime.now() - timedelta(days=30),
                assigned_attorneys=["john.doe@lawfirm.com", "jane.smith@lawfirm.com"],
                description="Negotiation and drafting of enterprise software licensing agreement",
                budget=50000.0,
                estimated_hours=100.0,
                actual_hours=45.5,
                priority="high",
                deadline=datetime.now() + timedelta(days=15),
                billing_contact="finance@techcorp.com",
                tags=["contract", "technology", "urgent"]
            ),
            Matter(
                id=str(uuid.uuid4()),
                name="Employment Dispute Resolution",
                client_id=str(uuid.uuid4()),
                client_name="StartupXYZ",
                matter_type="employment",
                status="active",
                created_date=datetime.now() - timedelta(days=45),
                assigned_attorneys=["alice.johnson@lawfirm.com"],
                description="Wrongful termination claim defense",
                budget=30000.0,
                estimated_hours=80.0,
                actual_hours=32.0,
                priority="medium",
                billing_contact="hr@startupxyz.com",
                tags=["employment", "litigation"]
            ),
            Matter(
                id=str(uuid.uuid4()),
                name="Corporate Acquisition",
                client_id=str(uuid.uuid4()),
                client_name="GlobalCorp",
                matter_type="mergers_acquisitions",
                status="on_hold",
                created_date=datetime.now() - timedelta(days=60),
                assigned_attorneys=["partner@lawfirm.com", "senior@lawfirm.com"],
                description="Asset purchase agreement for subsidiary acquisition",
                budget=150000.0,
                estimated_hours=300.0,
                actual_hours=125.0,
                priority="critical",
                billing_contact="legal@globalcorp.com",
                tags=["M&A", "corporate", "high-value"]
            )
        ]
        st.session_state.matters.extend(sample_matters)

def show():
    # Convert all time entries to objects once at the START
    if 'time_entries' in st.session_state:
        time_entries = [dict_to_obj(entry) if isinstance(entry, dict) else entry 
                       for entry in st.session_state.time_entries]
    else:
        time_entries = []
    
    # Now use time_entries with getattr() since they're SimpleNamespace objects
    total_unbilled_hours = sum(
        getattr(entry, 'hours', 0) for entry in time_entries 
        if getattr(entry, 'status', None) == "draft" and getattr(entry, 'billable', False)
    )
    
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
        <h1>⚖️ Matter Management</h1>
        <p>Track cases, matters, and client engagements</p>
    </div>
    """, unsafe_allow_html=True)
    
    initialize_matter_session_state()
    auth_service = AuthService()
    
    # Navigation tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📋 Matters", "📊 Analytics", "✅ Tasks", "⏰ Time Tracking", "💰 Expenses"])
    
    with tab1:
        _show_matter_dashboard(auth_service)
    
    with tab2:
        _show_matter_analytics()
    
    with tab3:
        _show_task_management(auth_service)
    
    with tab4:
        _show_time_tracking(auth_service)
    
    with tab5:
        _show_expense_tracking(auth_service)

def _show_matter_dashboard(auth_service):
    """Enhanced matter dashboard"""
    # Statistics
    _show_matter_statistics()
    
    st.divider()
    
    # Create new matter
    if auth_service.has_permission('write'):
        _show_create_matter_form(auth_service)
        st.divider()
    
    # Matter filters and search
    _show_matter_filters()
    
    # Matter list
    _show_matter_list(auth_service)

def _show_matter_statistics():
    """Display comprehensive matter statistics"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        active_matters = len([m for m in st.session_state.matters if get_attr(m, 'status') == 'active'])
        st.metric("🟢 Active Matters", active_matters)
    
    with col2:
        total_budget = sum(get_attr(m, 'budget', 0) for m in st.session_state.matters if get_attr(m, 'status') == 'active')
        st.metric("💰 Active Budget", f"${total_budget:,.0f}")
    
    with col3:
        total_hours = sum(get_attr(m, 'actual_hours', 0) for m in st.session_state.matters if get_attr(m, 'status') == 'active')
        st.metric("⏰ Hours Logged", f"{total_hours:.1f}")
    
    with col4:
        avg_utilization = 0
        if st.session_state.matters:
            total_est = sum(get_attr(m, 'estimated_hours', 0) for m in st.session_state.matters if get_attr(m, 'estimated_hours', 0) > 0)
            total_actual = sum(get_attr(m, 'actual_hours', 0) for m in st.session_state.matters if get_attr(m, 'estimated_hours', 0) > 0)
            avg_utilization = (total_actual / total_est * 100) if total_est > 0 else 0
        st.metric("📈 Utilization", f"{avg_utilization:.1f}%")
    
    # Additional statistics row
    col5, col6, col7, col8 = st.columns(4)
    
    with col5:
        overdue_matters = len([m for m in st.session_state.matters 
                             if get_attr(m, 'deadline') and get_attr(m, 'deadline') < datetime.now() and get_attr(m, 'status') == 'active'])
        st.metric("⚠️ Overdue", overdue_matters, delta=None, delta_color="inverse")
    
    with col6:
        high_priority = len([m for m in st.session_state.matters 
                           if get_attr(m, 'priority') in ['high', 'critical'] and get_attr(m, 'status') == 'active'])
        st.metric("🔴 High Priority", high_priority)
    
    with col7:
        on_hold = len([m for m in st.session_state.matters if get_attr(m, 'status') == 'on_hold'])
        st.metric("⏸️ On Hold", on_hold)
    
    with col8:
        closed_this_month = len([m for m in st.session_state.matters 
                               if get_attr(m, 'closed_date') and (datetime.now() - get_attr(m, 'closed_date')).days <= 30])
        st.metric("✅ Closed (30d)", closed_this_month)

def _show_create_matter_form(auth_service):
    """Enhanced matter creation form"""
    st.subheader("➕ Create New Matter")
    
    with st.form("new_matter_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            matter_name = st.text_input("Matter Name *", placeholder="e.g., Software License Agreement")
            client_name = st.text_input("Client Name *", placeholder="e.g., TechCorp Inc")
            matter_type = st.selectbox("Matter Type *", 
                                     [mt.value.replace('_', ' ').title() for mt in MatterType])
            priority = st.selectbox("Priority", [p.value.title() for p in Priority], index=1)
        
        with col2:
            description = st.text_area("Description", height=100)
            estimated_budget = st.number_input("Estimated Budget ($)", min_value=0.0, step=1000.0)
            estimated_hours = st.number_input("Estimated Hours", min_value=0.0, step=10.0, value=40.0)
            hourly_rate = st.number_input("Hourly Rate ($)", min_value=0.0, step=25.0, value=250.0)
        
        # Additional fields
        col3, col4 = st.columns(2)
        
        with col3:
            deadline = st.date_input("Deadline (optional)", value=None)
            billing_contact = st.text_input("Billing Contact Email", placeholder="billing@client.com")
        
        with col4:
            assigned_attorneys = st.text_input("Assigned Attorneys (comma-separated)", 
                                             placeholder="john@firm.com, jane@firm.com")
            tags = st.text_input("Tags (comma-separated)", placeholder="contract, urgent, technology")
        
        if st.form_submit_button("🚀 Create Matter", type="primary"):
            if matter_name and client_name:
                new_matter = Matter(
                    id=str(uuid.uuid4()),
                    name=matter_name,
                    client_id=str(uuid.uuid4()),
                    client_name=client_name,
                    matter_type=matter_type.lower().replace(' ', '_'),
                    status='active',
                    created_date=datetime.now(),
                    assigned_attorneys=[email.strip() for email in assigned_attorneys.split(',') if email.strip()],
                    description=description,
                    budget=estimated_budget,
                    estimated_hours=estimated_hours,
                    actual_hours=0.0,
                    hourly_rate=hourly_rate,
                    priority=priority.lower(),
                    deadline=datetime.combine(deadline, datetime.min.time()) if deadline else None,
                    billing_contact=billing_contact,
                    tags=[tag.strip() for tag in tags.split(',') if tag.strip()]
                )
                
                st.session_state.matters.append(new_matter)
                st.success(f"✅ Matter '{matter_name}' created successfully!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("❌ Please fill in all required fields.")

def _show_matter_filters():
    """Matter filtering interface"""
    st.subheader("🔍 Filter & Search")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        status_filter = st.selectbox("Status", 
                                   ["All"] + [s.value.title() for s in MatterStatus])
    
    with col2:
        type_filter = st.selectbox("Type", 
                                 ["All"] + [mt.value.replace('_', ' ').title() for mt in MatterType])
    
    with col3:
        priority_filter = st.selectbox("Priority", 
                                     ["All"] + [p.value.title() for p in Priority])
    
    with col4:
        attorney_filter = st.selectbox("Assigned Attorney", 
                                     ["All"] + list(set([attorney for matter in st.session_state.matters 
                                                        for attorney in get_attr(matter, 'assigned_attorneys', [])])))
    
    # Search functionality
    search_term = st.text_input("🔍 Search matters", placeholder="Search by name, client, or description...")
    
    # Apply filters to session state for use in matter list
    st.session_state['matter_filters'] = {
        'status': status_filter,
        'type': type_filter,
        'priority': priority_filter,
        'attorney': attorney_filter,
        'search': search_term
    }

def _show_matter_list(auth_service):
    """Enhanced matter list with filtering"""
    st.subheader("📋 Matter List")
    
    # Apply filters
    filtered_matters = _apply_matter_filters(st.session_state.matters)
    
    if not filtered_matters:
        st.info("No matters found matching your filters.")
        return
    
    st.markdown(f"**Showing {len(filtered_matters)} matters**")
    
    # Sort options
    sort_by = st.selectbox("Sort by:", 
                          ["Created Date", "Deadline", "Priority", "Name", "Budget", "Hours"])
    
    filtered_matters = _sort_matters(filtered_matters, sort_by)
    
    # Display matters
    for matter in filtered_matters:
        _show_matter_card(matter, auth_service)

def _apply_matter_filters(matters):
    """Apply filters to matter list"""
    if 'matter_filters' not in st.session_state:
        return matters
    
    filters = st.session_state['matter_filters']
    filtered = matters.copy()
    
    # Status filter
    if filters['status'] != "All":
        status_value = filters['status'].lower()
        filtered = [m for m in filtered if get_attr(m, 'status') == status_value]
    
    # Type filter
    if filters['type'] != "All":
        type_value = filters['type'].lower().replace(' ', '_')
        filtered = [m for m in filtered if get_attr(m, 'matter_type') == type_value]
    
    # Priority filter
    if filters['priority'] != "All":
        priority_value = filters['priority'].lower()
        filtered = [m for m in filtered if get_attr(m, 'priority') == priority_value]
    
    # Attorney filter
    if filters['attorney'] != "All":
        filtered = [m for m in filtered if filters['attorney'] in get_attr(m, 'assigned_attorneys', [])]
    
    # Search filter
    if filters['search']:
        search_term = filters['search'].lower()
        filtered = [m for m in filtered if 
                   search_term in get_attr(m, 'name', '').lower() or 
                   search_term in get_attr(m, 'client_name', '').lower() or 
                   search_term in get_attr(m, 'description', '').lower()]
    
    return filtered

def _sort_matters(matters, sort_by):
    """Sort matters based on selected criteria"""
    if sort_by == "Created Date":
        return sorted(matters, key=lambda x: get_attr(x, 'created_date', datetime.min), reverse=True)
    elif sort_by == "Deadline":
        return sorted(matters, key=lambda x: get_attr(x, 'deadline') or datetime.max)
    elif sort_by == "Priority":
        priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        return sorted(matters, key=lambda x: priority_order.get(get_attr(x, 'priority', 'low'), 4))
    elif sort_by == "Name":
        return sorted(matters, key=lambda x: get_attr(x, 'name', '').lower())
    elif sort_by == "Budget":
        return sorted(matters, key=lambda x: get_attr(x, 'budget', 0), reverse=True)
    elif sort_by == "Hours":
        return sorted(matters, key=lambda x: get_attr(x, 'actual_hours', 0), reverse=True)
    else:
        return matters

def _show_matter_card(matter, auth_service):
    """Enhanced matter card display"""
    # Priority and status indicators
    priority_colors = {"low": "🟢", "medium": "🟡", "high": "🟠", "critical": "🔴"}
    status_colors = {"active": "🟢", "on_hold": "🟡", "closed": "✅", "archived": "📦", "cancelled": "❌"}
    
    matter_id = get_attr(matter, 'id')
    matter_name = get_attr(matter, 'name', 'Unknown')
    matter_client = get_attr(matter, 'client_name', 'Unknown')
    matter_status = get_attr(matter, 'status', 'active')
    matter_priority = get_attr(matter, 'priority', 'medium')
    matter_deadline = get_attr(matter, 'deadline')
    matter_type = get_attr(matter, 'matter_type', 'unknown')
    matter_budget = get_attr(matter, 'budget', 0)
    matter_estimated_hours = get_attr(matter, 'estimated_hours', 0)
    matter_actual_hours = get_attr(matter, 'actual_hours', 0)
    matter_hourly_rate = get_attr(matter, 'hourly_rate', 250)
    matter_created_date = get_attr(matter, 'created_date', datetime.now())
    matter_billing_contact = get_attr(matter, 'billing_contact', '')
    matter_description = get_attr(matter, 'description', '')
    matter_tags = get_attr(matter, 'tags', [])
    matter_assigned_attorneys = get_attr(matter, 'assigned_attorneys', [])
    
    matter_docs = [doc for doc in st.session_state.get('documents', []) 
                   if hasattr(doc, 'matter_id') and doc.matter_id == matter_id]
    
    # Check if overdue
    is_overdue = matter_deadline and matter_deadline < datetime.now() and matter_status == 'active'
    overdue_indicator = "⚠️ OVERDUE" if is_overdue else ""
    
    with st.expander(f"{priority_colors.get(matter_priority, '⚪')} {matter_name} - {matter_client} {overdue_indicator}"):
        # Main information
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"**👤 Client:** {matter_client}")
            st.markdown(f"**📋 Type:** {matter_type.replace('_', ' ').title()}")
            st.markdown(f"**🎯 Status:** {status_colors.get(matter_status, '❓')} {matter_status.title()}")
            st.markdown(f"**🔥 Priority:** {priority_colors.get(matter_priority, '⚪')} {matter_priority.title()}")
        
        with col2:
            st.markdown(f"**📄 Documents:** {len(matter_docs)}")
            st.markdown(f"**💰 Budget:** ${matter_budget:,.2f}")
            st.markdown(f"**⏰ Est. Hours:** {matter_estimated_hours}")
            st.markdown(f"**📊 Actual Hours:** {matter_actual_hours}")
        
        with col3:
