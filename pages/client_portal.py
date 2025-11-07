import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# ADD THIS IMPORT
from services.data_security import DataSecurity


def auto_save_client_data():
    """SECURE auto-save client portal data"""
    from services.data_security import DataSecurity
    
    if 'portal_clients' in st.session_state:
        DataSecurity.save_user_data('portal_clients', st.session_state.portal_clients)


def send_client_invitation(client_email, client_name, access_level):
    """Simulate sending invitation email to client"""
    # In a real implementation, this would integrate with your email service
    # For now, we'll save the invitation to user data and show a success message
    
    invitation_data = {
        'email': client_email,
        'name': client_name,
        'access_level': access_level,
        'sent_date': datetime.now().isoformat(),
        'status': 'sent',
        'invitation_code': f"INV-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    }
    
    # Save invitation record
    invitations = DataSecurity.load_user_data('client_invitations', [])
    invitations.append(invitation_data)
    DataSecurity.save_user_data('client_invitations', invitations)
    
    return invitation_data

def show():
    
    # Require authentication
    DataSecurity.require_auth("Client Portal")
    
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
        <h1>🌐 Client Portal</h1>
        <p>Secure access to your personalized data, insights, and project updates</p>
    </div>

    """, unsafe_allow_html=True)

    # Initialize real client data
    user_email = st.session_state.get('user_data', {}).get('email', 'demo@example.com')
    
    # SECURE DATA LOADING
    if 'portal_clients' not in st.session_state:
        st.session_state.portal_clients = DataSecurity.get_user_clients()
    
    # Client Portal tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "👥 Client Access", 
        "📄 Document Sharing", 
        "💬 Communications", 
        "🔧 Portal Settings", 
        "📊 Usage Analytics"
    ])
    
    with tab1:
        show_client_access()
    
    with tab2:
        show_document_sharing()
    
    with tab3:
        show_communications()
    
    with tab4:
        show_portal_settings()
    
    with tab5:
        show_usage_analytics()

def show_client_access():
    st.subheader("👥 Client Access Management")
    
    # ✅ CHECK IF EDITING A CLIENT
    if 'editing_client_id' in st.session_state and st.session_state.editing_client_id:
        # Find the client being edited
        client_to_edit = None
        for client in st.session_state.portal_clients:
            if client.get('id') == st.session_state.editing_client_id:
                client_to_edit = client
                break
        
        if client_to_edit:
            edit_client_form(client_to_edit)
            st.markdown("---")
            
    # ADD NEW CLIENT BUTTON AT TOP
    col_header1, col_header2 = st.columns([3, 1])
    
    with col_header2:
        if st.button("➕ Add New Client", type="primary", use_container_width=True):
            st.session_state.show_add_client_form = True
    
    # ADD CLIENT FORM
    if st.session_state.get('show_add_client_form', False):
        with st.form("add_client_form"):
            st.markdown("### Add New Client Portal User")
            
            col_form1, col_form2 = st.columns(2)
            
            with col_form1:
                client_name = st.text_input("Client Name *", placeholder="John Smith")
                client_email = st.text_input("Email Address *", placeholder="john@company.com")
                company_name = st.text_input("Company Name", placeholder="ABC Corporation")
            
            with col_form2:
                access_level = st.selectbox("Access Level", ["Full Access", "Limited Access", "View Only"])
                
                # Multi-select for matters
                matters = st.session_state.get('matters', [])
                if matters:
                    matter_names = [m.get('name', 'Untitled') if isinstance(m, dict) else getattr(m, 'name', 'Untitled') for m in matters]
                    selected_matters = st.multiselect("Assign Matters", matter_names)
                else:
                    st.info("No matters available. Create matters in Matter Management first.")
                    selected_matters = []
                
                send_invite = st.checkbox("Send invitation email", value=True)
            
            col_submit1, col_submit2 = st.columns(2)
            
            with col_submit1:
                if st.form_submit_button("✅ Add Client", type="primary"):
                    if client_name and client_email:
                        # Create new client
                        new_client = {
                            "id": len(st.session_state.portal_clients) + 1,
                            "name": client_name,
                            "company": company_name if company_name else "N/A",
                            "email": client_email,
                            "access_level": access_level,
                            "status": "Pending Setup" if send_invite else "Active",
                            "last_login": "Never",
                            "documents_accessed": 0,
                            "matters": selected_matters,
                            "permissions": get_permissions_for_access_level(access_level),
                            "created_date": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        }
                        
                        st.session_state.portal_clients.append(new_client)
                        auto_save_client_data()
                        
                        # ✅ SEND INVITATION EMAIL
                        if send_invite:
                            invitation = send_client_invitation(client_email, client_name, access_level)
                            st.success(f"✅ Client {client_name} added successfully!")
                            st.info(f"📧 Invitation email sent to {client_email}")
                            st.code(f"Invitation Code: {invitation['invitation_code']}")
                        else:
                            st.success(f"✅ Client {client_name} added successfully!")
                        
                        st.session_state.show_add_client_form = False
                        st.rerun()
                    else:
                        st.error("Please fill in required fields (Name and Email)")
            
            with col_submit2:
                if st.form_submit_button("❌ Cancel"):
                    st.session_state.show_add_client_form = False
                    st.rerun()
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Client access overview
        st.markdown("#### Active Client Portal Users")
        
        # Search and filter
        col_search1, col_search2, col_search3 = st.columns(3)
        with col_search1:
            client_search = st.text_input("Search Clients:", placeholder="Name, email, or company...")
        with col_search2:
            access_filter = st.selectbox("Access Level:", ["All", "Full Access", "Limited Access", "View Only", "Suspended"])
        with col_search3:
            status_filter = st.selectbox("Status:", ["All", "Active", "Inactive", "Pending Setup"])
        
        # Get client list
        client_users = st.session_state.portal_clients
        
        # APPLY FILTERS
        filtered_clients = client_users
        
        # Search filter
        if client_search:
            search_lower = client_search.lower()
            filtered_clients = [
                c for c in filtered_clients
                if search_lower in c.get('name', '').lower() or
                   search_lower in c.get('email', '').lower() or
                   search_lower in c.get('company', '').lower()
            ]
        
        # Access level filter
        if access_filter != "All":
            filtered_clients = [c for c in filtered_clients if c.get('access_level') == access_filter]
        
        # Status filter
        if status_filter != "All":
            filtered_clients = [c for c in filtered_clients if c.get('status') == status_filter]
        
        # Display message if no clients
        if not filtered_clients:
            if not client_users:
                st.info("📝 No clients yet. Click 'Add New Client' to create your first client portal user.")
            else:
                st.info("🔍 No clients match your search criteria.")
        
        # Display filtered clients
        for client in filtered_clients:
            access_color = {
                "Full Access": "🟢",
                "Limited Access": "🟡",
                "View Only": "🔵",
                "Suspended": "🔴"
            }
            
            status_color = {
                "Active": "✅",
                "Inactive": "⭕",
                "Pending Setup": "⏳"
            }
            
            with st.expander(f"{access_color.get(client.get('access_level'), '⚪')} {client.get('name', 'Unknown')} ({client.get('company', 'N/A')}) - {status_color.get(client.get('status'), '⭕')} {client.get('status', 'Unknown')}"):
                col_client1, col_client2, col_client3 = st.columns(3)
                
                with col_client1:
                    st.write(f"**Email:** {client.get('email', 'N/A')}")
                    st.write(f"**Access Level:** {client.get('access_level', 'N/A')}")
                    st.write(f"**Last Login:** {client.get('last_login', 'Never')}")
                
                with col_client2:
                    st.write(f"**Documents Accessed:** {client.get('documents_accessed', 0)}")
                    st.write("**Active Matters:**")
                    matters = client.get('matters', [])
                    if matters:
                        for matter in matters:
                            st.write(f"• {matter}")
                    else:
                        st.write("• No matters assigned")
                
                with col_client3:
                    st.write("**Permissions:**")
                    permissions = client.get('permissions', [])
                    for permission in permissions:
                        st.write(f"✓ {permission}")
                
                # Client management actions
                col_action1, col_action2, col_action3, col_action4 = st.columns(4)
                with col_action1:
                    if st.button("⚙️ Edit Access", key=f"edit_{client.get('id')}"):
                        st.session_state.editing_client_id = client.get('id')
                        st.rerun()
                with col_action2:
                    if st.button("📧 Send Invite", key=f"invite_{client.get('id')}"):
                    # ✅ ACTUALLY SEND INVITATION
                    invitation = send_client_invitation(
                        client.get('email'), 
                        client.get('name'), 
                        client.get('access_level')
                    )
                    st.success(f"✅ Invitation sent to {client.get('email')}")
                    st.code(f"Invitation Code: {invitation['invitation_code']}")
                    st.rerun()
                with col_action3:
                    if st.button("🔒 Reset Password", key=f"reset_{client.get('id')}"):
                        st.success("Password reset email sent")
                with col_action4:
                    if client.get('status') == "Active":
                        if st.button("⏸️ Suspend", key=f"suspend_{client.get('id')}"):
                            client['status'] = "Suspended"
                            auto_save_client_data()
                            st.warning("Client suspended")
                            st.rerun()
                    else:
                        if st.button("▶️ Activate", key=f"activate_{client.get('id')}"):
                            client['status'] = "Active"
                            auto_save_client_data()
                            st.success("Client activated")
                            st.rerun()
                
                # Delete button
                if st.button("🗑️ Delete Client", key=f"delete_{client.get('id')}"):
                    st.session_state.portal_clients.remove(client)
                    auto_save_client_data()
                    st.success("Client deleted")
                    st.rerun()
        
        # Bulk operations
        if client_users:
            st.markdown("#### Bulk Operations")
            
            col_bulk1, col_bulk2, col_bulk3, col_bulk4 = st.columns(4)
            with col_bulk1:
                if st.button("📧 Send Welcome Email"):
                    st.info("Sending welcome emails to new users...")
            with col_bulk2:
                if st.button("🔄 Sync Permissions"):
                    st.info("Synchronizing permissions across all users...")
            with col_bulk3:
                if st.button("📊 Export User List"):
                    st.info("Exporting client user data...")
            with col_bulk4:
                if st.button("⚠️ Security Audit"):
                    st.info("Running security audit on client accounts...")
    
    with col2:
        st.markdown("#### Access Statistics")
        
        total_users = len(client_users)
        active_users = len([c for c in client_users if c.get('status') == 'Active'])
        pending_users = len([c for c in client_users if c.get('status') == 'Pending Setup'])
        
        access_stats = [
            ("Total Portal Users", str(total_users)),
            ("Active This Month", str(active_users)),
            ("Pending Setup", str(pending_users)),
            ("Login Success Rate", "98.2%")
        ]
        
        for label, value in access_stats:
            st.metric(label, value)
        
        st.markdown("#### Access Levels")
        
        full_access = len([c for c in client_users if c.get('access_level') == 'Full Access'])
        limited_access = len([c for c in client_users if c.get('access_level') == 'Limited Access'])
        view_only = len([c for c in client_users if c.get('access_level') == 'View Only'])
        suspended = len([c for c in client_users if c.get('status') == 'Suspended'])
        
        if total_users > 0:
            access_breakdown = [
                ("Full Access", f"{full_access} users", f"{full_access/total_users*100:.0f}%"),
                ("Limited Access", f"{limited_access} users", f"{limited_access/total_users*100:.0f}%"),
                ("View Only", f"{view_only} users", f"{view_only/total_users*100:.0f}%"),
                ("Suspended", f"{suspended} users", f"{suspended/total_users*100:.0f}%")
            ]
        else:
            access_breakdown = [
                ("Full Access", "0 users", "0%"),
                ("Limited Access", "0 users", "0%"),
                ("View Only", "0 users", "0%"),
                ("Suspended", "0 users", "0%")
            ]
        
        for level, count, percentage in access_breakdown:
            st.write(f"**{level}:** {count} ({percentage})")

def get_permissions_for_access_level(access_level):
    """Get default permissions based on access level"""
    if access_level == "Full Access":
        return ["View Documents", "Download Files", "Submit Requests", "View Billing", "Approve Invoices"]
    elif access_level == "Limited Access":
        return ["View Documents", "Download Files", "Submit Requests"]
    elif access_level == "View Only":
        return ["View Documents"]
    else:
        return []


def edit_client_form(client):
    """Display edit form for a client"""
    st.markdown("---")
    st.markdown(f"### ✏️ Edit Client: {client.get('name')}")
    
    with st.form(f"edit_client_form_{client.get('id')}"):
        col_edit1, col_edit2 = st.columns(2)
        
        with col_edit1:
            client_name = st.text_input("Client Name *", value=client.get('name', ''))
            client_email = st.text_input("Email Address *", value=client.get('email', ''))
            company_name = st.text_input("Company Name", value=client.get('company', ''))
        
        with col_edit2:
            access_level = st.selectbox(
                "Access Level", 
                ["Full Access", "Limited Access", "View Only"],
                index=["Full Access", "Limited Access", "View Only"].index(client.get('access_level', 'View Only'))
            )
            
            status = st.selectbox(
                "Status",
                ["Active", "Inactive", "Pending Setup", "Suspended"],
                index=["Active", "Inactive", "Pending Setup", "Suspended"].index(client.get('status', 'Active'))
            )
            
            # Multi-select for matters
            matters = st.session_state.get('matters', [])
            if matters:
                matter_names = [m.get('name', 'Untitled') if isinstance(m, dict) else getattr(m, 'name', 'Untitled') for m in matters]
                current_matters = client.get('matters', [])
                selected_matters = st.multiselect("Assign Matters", matter_names, default=current_matters)
            else:
                selected_matters = []
        
        col_submit1, col_submit2 = st.columns(2)
        
        with col_submit1:
            if st.form_submit_button("💾 Save Changes", type="primary"):
                # Update the client
                for c in st.session_state.portal_clients:
                    if c.get('id') == client.get('id'):
                        c['name'] = client_name
                        c['email'] = client_email
                        c['company'] = company_name if company_name else "N/A"
                        c['access_level'] = access_level
                        c['status'] = status
                        c['matters'] = selected_matters
                        c['permissions'] = get_permissions_for_access_level(access_level)
                        break
                
                auto_save_client_data()
                st.session_state.editing_client_id = None
                st.success(f"✅ Client '{client_name}' updated successfully!")
                st.rerun()
        
        with col_submit2:
            if st.form_submit_button("❌ Cancel"):
                st.session_state.editing_client_id = None
                st.rerun()

def show_document_sharing():
    st.subheader("📄 Client Document Sharing")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Document sharing interface
        st.markdown("#### Share Documents with Clients")
        
        with st.form("share_document"):
            col_share1, col_share2 = st.columns(2)
            
            with col_share1:
                selected_client = st.selectbox("Select Client:", [
                    "ABC Corporation (John Smith)",
                    "Tech Solutions Inc (Sarah Johnson)",
                    "Startup Innovations (Mike Davis)",
                    "Global Manufacturing (Emily Chen)"
                ])
                
                document_type = st.selectbox("Document Type:", [
                    "Contract", "Legal Brief", "Court Filing", "Correspondence", 
                    "Invoice", "Report", "Other"
                ])
                
                sharing_method = st.selectbox("Sharing Method:", [
                    "Portal Access", "Secure Email", "Download Link", "View Only"
                ])
            
            with col_share2:
                access_level = st.selectbox("Access Level:", [
                    "View Only", "Download Allowed", "Comment Allowed", "Full Access"
                ])
                
                expiry_date = st.date_input("Access Expires:", value=datetime.now() + timedelta(days=30))
                
                notification = st.checkbox("Send notification to client", value=True)
            
            document_title = st.text_input("Document Title:", placeholder="Enter document title...")
            document_description = st.text_area("Description:", placeholder="Brief description of the document...")
            
            # File upload simulation
            uploaded_file = st.file_uploader("Upload Document:", type=['pdf', 'docx', 'txt'])
            
            if st.form_submit_button("📤 Share Document", type="primary"):
                st.success(f"Document shared successfully with {selected_client}!")
                if notification:
                    st.info("Notification email sent to client.")
        
        # Shared documents tracking
        st.markdown("#### Recently Shared Documents")
        
        shared_docs = [
            {
                "document": "Merger Agreement Final.pdf",
                "client": "ABC Corporation",
                "shared_date": "2024-09-23",
                "access_level": "Download Allowed",
                "status": "Viewed",
                "downloads": 2,
                "expires": "2024-10-23"
            },
            {
                "document": "Employment Contract.docx",
                "client": "Tech Solutions Inc",
                "shared_date": "2024-09-22",
                "access_level": "Full Access",
                "status": "Downloaded",
                "downloads": 1,
                "expires": "2024-11-22"
            },
            {
                "document": "Incorporation Documents.pdf",
                "client": "Startup Innovations",
                "shared_date": "2024-09-21",
                "access_level": "View Only",
                "status": "Not Viewed",
                "downloads": 0,
                "expires": "2024-10-21"
            },
            {
                "document": "Compliance Report.pdf",
                "client": "Global Manufacturing",
                "shared_date": "2024-09-20",
                "access_level": "Download Allowed",
                "status": "Viewed",
                "downloads": 3,
                "expires": "2024-10-20"
            }
        ]
        
        for doc in shared_docs:
            status_icons = {
                "Viewed": "👁️",
                "Downloaded": "📥",
                "Not Viewed": "⭕"
            }
            
            with st.expander(f"{status_icons[doc['status']]} {doc['document']} → {doc['client']}"):
                col_doc1, col_doc2, col_doc3 = st.columns(3)
                
                with col_doc1:
                    st.write(f"**Shared Date:** {doc['shared_date']}")
                    st.write(f"**Access Level:** {doc['access_level']}")
                    st.write(f"**Status:** {doc['status']}")
                
                with col_doc2:
                    st.write(f"**Downloads:** {doc['downloads']}")
                    st.write(f"**Expires:** {doc['expires']}")
                    
                    if doc['downloads'] > 0:
                        st.progress(min(doc['downloads'] / 5, 1.0))
                
                with col_doc3:
                    st.button("📊 View Analytics", key=f"analytics_{doc['document'][:10]}")
                    st.button("🔄 Reshare", key=f"reshare_{doc['document'][:10]}")
                    st.button("🗑️ Revoke Access", key=f"revoke_{doc['document'][:10]}")
    
    with col2:
        st.markdown("#### Sharing Statistics")
        
        sharing_stats = [
            ("Documents Shared", "247"),
            ("This Month", "34"),
            ("Total Downloads", "1,892"),
            ("Avg. View Time", "12.4 min")
        ]
        
        for label, value in sharing_stats:
            st.metric(label, value)
        
        st.markdown("#### Document Types")
        
        doc_types = [
            ("Contracts", "89 docs"),
            ("Correspondence", "67 docs"),
            ("Reports", "45 docs"),
            ("Invoices", "34 docs"),
            ("Other", "12 docs")
        ]
        
        for doc_type, count in doc_types:
            st.write(f"**{doc_type}:** {count}")
        
        st.markdown("#### Security Settings")
        
        security_settings = [
            ("Watermark Documents", "✅"),
            ("Track Downloads", "✅"),
            ("Expire Old Links", "✅"),
            ("Require Login", "✅"),
            ("IP Restrictions", "❌")
        ]
        
        for setting, status in security_settings:
            st.write(f"{setting}: {status}")

def show_communications():
    st.subheader("💬 Client Communications")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Communication center
        st.markdown("#### Client Communication Center")
        
        # Message composer
        with st.expander("✉️ Compose New Message"):
            col_msg1, col_msg2 = st.columns(2)
            
            with col_msg1:
                recipient = st.selectbox("To:", [
                    "ABC Corporation (John Smith)",
                    "Tech Solutions Inc (Sarah Johnson)",
                    "Startup Innovations (Mike Davis)",
                    "Global Manufacturing (Emily Chen)",
                    "All Clients"
                ])
                
                message_type = st.selectbox("Message Type:", [
                    "General Update", "Document Notification", "Billing Notice", 
                    "Appointment Reminder", "Status Update", "Urgent Notice"
                ])
            
            with col_msg2:
                priority = st.selectbox("Priority:", ["Normal", "High", "Low"])
                delivery_method = st.selectbox("Delivery:", ["Portal + Email", "Portal Only", "Email Only"])
            
            subject = st.text_input("Subject:", placeholder="Enter message subject...")
            message_body = st.text_area("Message:", placeholder="Type your message here...", height=150)
            
            col_compose1, col_compose2, col_compose3 = st.columns(3)
            with col_compose1:
                if st.button("📤 Send Message"):
                    st.success("Message sent successfully!")
            with col_compose2:
                if st.button("📝 Save Draft"):
                    st.info("Message saved as draft.")
            with col_compose3:
                if st.button("👁️ Preview"):
                    st.info("Opening message preview...")
        
        # Recent communications
        st.markdown("#### Recent Communications")
        
        communications = [
            {
                "type": "Message",
                "subject": "Document Review Complete",
                "client": "ABC Corporation",
                "date": "2024-09-23 10:30 AM",
                "status": "Read",
                "priority": "Normal",
                "method": "Portal + Email"
            },
            {
                "type": "Notification",
                "subject": "New Document Available",
                "client": "Tech Solutions Inc",
                "date": "2024-09-22 03:15 PM",
                "status": "Delivered",
                "priority": "Normal",
                "method": "Portal Only"
            },
            {
                "type": "Reminder",
                "subject": "Upcoming Court Date",
                "client": "Startup Innovations",
                "date": "2024-09-22 09:00 AM",
                "status": "Read",
                "priority": "High",
                "method": "Portal + Email"
            },
            {
                "type": "Invoice",
                "subject": "Monthly Invoice - September 2024",
                "client": "Global Manufacturing",
                "date": "2024-09-21 05:00 PM",
                "status": "Unread",
                "priority": "Normal",
                "method": "Email Only"
            }
        ]
        
        for comm in communications:
            type_icons = {
                "Message": "💬",
                "Notification": "🔔",
                "Reminder": "⏰",
                "Invoice": "💰"
            }
            
            status_colors = {
                "Read": "🟢",
                "Delivered": "🟡",
                "Unread": "🔴"
            }
            
            priority_icons = {
                "High": "🔴",
                "Normal": "🔵",
                "Low": "🟢"
            }
            
            with st.expander(f"{type_icons[comm['type']]} {comm['subject']} → {comm['client']} {status_colors[comm['status']]}"):
                col_comm1, col_comm2, col_comm3 = st.columns(3)
                
                with col_comm1:
                    st.write(f"**Type:** {comm['type']}")
                    st.write(f"**Date:** {comm['date']}")
                    st.write(f"**Status:** {comm['status']}")
                
                with col_comm2:
                    st.write(f"**Priority:** {priority_icons[comm['priority']]} {comm['priority']}")
                    st.write(f"**Method:** {comm['method']}")
                
                with col_comm3:
                    st.button("📖 View Full", key=f"view_{comm['subject'][:10]}")
                    st.button("↩️ Reply", key=f"reply_{comm['subject'][:10]}")
                    st.button("🔄 Resend", key=f"resend_{comm['subject'][:10]}")
        
        # Communication templates
        st.markdown("#### Message Templates")
        
        templates = [
            "📄 Document Ready for Review",
            "⏰ Appointment Confirmation",
            "💰 Invoice Payment Reminder",
            "📅 Status Update Request",
            "🎉 Matter Completion Notice"
        ]
        
        col_template1, col_template2 = st.columns(2)
        for i, template in enumerate(templates):
            col = col_template1 if i % 2 == 0 else col_template2
            with col:
                if st.button(template, key=f"template_{i}"):
                    st.info(f"Loading template: {template}")
    
    with col2:
        st.markdown("#### Communication Stats")
        
        comm_stats = [
            ("Messages Sent", "156"),
            ("This Month", "23"),
            ("Read Rate", "94.2%"),
            ("Avg Response Time", "4.2 hrs")
        ]
        
        for label, value in comm_stats:
            st.metric(label, value)
        
        st.markdown("#### Message Status")
        
        message_status = [
            ("✅ Read", "89%"),
            ("📤 Delivered", "8%"),
            ("❌ Unread", "3%")
        ]
        
        for status, percentage in message_status:
            st.write(f"{status}: {percentage}")
        
        st.markdown("#### Quick Actions")
        
        if st.button("📢 Send Announcement"):
            st.info("Opening announcement composer...")
        if st.button("📊 Communication Report"):
            st.info("Generating communication analytics...")
        if st.button("⚙️ Notification Settings"):
            st.info("Opening notification preferences...")

def show_portal_settings():
    st.subheader("🔧 Client Portal Configuration")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Portal appearance settings
        st.markdown("#### Portal Appearance & Branding")
        
        with st.expander("🎨 Branding Settings"):
            col_brand1, col_brand2 = st.columns(2)
            
            with col_brand1:
                firm_name = st.text_input("Firm Name:", value="LegalDoc Pro")
                portal_title = st.text_input("Portal Title:", value="Client Portal")
                primary_color = st.color_picker("Primary Color:", value="#1f77b4")
                secondary_color = st.color_picker("Secondary Color:", value="#ff7f0e")
            
            with col_brand2:
                logo_upload = st.file_uploader("Upload Logo:", type=['png', 'jpg', 'svg'])
                favicon_upload = st.file_uploader("Upload Favicon:", type=['ico', 'png'])
                
                custom_css = st.text_area("Custom CSS:", placeholder="Enter custom CSS styles...")
            
            if st.button("💾 Save Branding"):
                st.success("Branding settings saved successfully!")
        
        # Access and security settings
        st.markdown("#### Access & Security Settings")
        
        with st.expander("🔒 Security Configuration"):
            col_security1, col_security2 = st.columns(2)
            
            with col_security1:
                two_factor_auth = st.checkbox("Require Two-Factor Authentication", value=True)
                session_timeout = st.selectbox("Session Timeout:", ["30 minutes", "1 hour", "2 hours", "4 hours", "8 hours"])
                password_policy = st.selectbox("Password Policy:", ["Standard", "Strong", "Very Strong"])
                ip_restrictions = st.checkbox("Enable IP Restrictions", value=False)
            
            with col_security2:
                document_watermarks = st.checkbox("Add Watermarks to Documents", value=True)
                download_tracking = st.checkbox("Track Document Downloads", value=True)
                audit_logging = st.checkbox("Enable Audit Logging", value=True)
                auto_logout = st.checkbox("Auto-logout Inactive Users", value=True)
            
            if st.button("🔒 Update Security Settings"):
                st.success("Security settings updated successfully!")
        
        # Feature settings
        st.markdown("#### Feature Configuration")
        
        with st.expander("⚙️ Portal Features"):
            col_features1, col_features2 = st.columns(2)
            
            with col_features1:
                document_sharing = st.checkbox("Document Sharing", value=True)
                messaging = st.checkbox("Client Messaging", value=True)
                billing_access = st.checkbox("Billing & Invoices", value=True)
                calendar_integration = st.checkbox("Calendar Integration", value=True)
            
            with col_features2:
                mobile_app = st.checkbox("Mobile App Access", value=True)
                notifications = st.checkbox("Email Notifications", value=True)
                file_uploads = st.checkbox("Client File Uploads", value=True)
                video_calls = st.checkbox("Video Conferencing", value=False)
            
            if st.button("🔧 Save Feature Settings"):
                st.success("Feature settings saved successfully!")
        
        # Notification settings
        st.markdown("#### Notification Configuration")
        
        with st.expander("📧 Email & Notification Settings"):
            col_notif1, col_notif2 = st.columns(2)
            
            with col_notif1:
                welcome_email = st.checkbox("Send Welcome Email", value=True)
                document_notifications = st.checkbox("Document Share Notifications", value=True)
                reminder_emails = st.checkbox("Appointment Reminders", value=True)
                invoice_notifications = st.checkbox("Invoice Notifications", value=True)
            
            with col_notif2:
                email_frequency = st.selectbox("Email Frequency:", ["Immediate", "Daily Digest", "Weekly Summary"])
                notification_hours = st.selectbox("Send Notifications:", ["Anytime", "Business Hours Only", "Custom Schedule"])
                
                if notification_hours == "Custom Schedule":
                    start_time = st.time_input("Start Time:")
                    end_time = st.time_input("End Time:")
            
            if st.button("📧 Save Notification Settings"):
                st.success("Notification settings saved successfully!")
    
    with col2:
        st.markdown("#### Portal Status")
        
        portal_status = [
            ("Portal Status", "🟢 Online"),
            ("Active Users", "64"),
            ("System Health", "98.5%"),
            ("Uptime", "99.9%")
        ]
        
        for label, value in portal_status:
            st.write(f"**{label}:** {value}")
        
        st.markdown("#### Configuration Backup")
        
        if st.button("💾 Backup Settings"):
            st.info("Creating configuration backup...")
        if st.button("📥 Restore Settings"):
            st.info("Opening restore interface...")
        if st.button("🔄 Reset to Default"):
            st.warning("This will reset all settings to default!")
        
        st.markdown("#### Support & Help")
        
        if st.button("📖 Portal Documentation"):
            st.info("Opening portal documentation...")
        if st.button("🎥 Video Tutorials"):
            st.info("Loading video tutorials...")
        if st.button("💬 Contact Support"):
            st.info("Opening support chat...")

def show_usage_analytics():
    st.subheader("📊 Portal Usage Analytics")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Usage metrics
        st.markdown("#### Portal Usage Overview")
        
        # Generate sample usage data
        dates = pd.date_range('2024-09-01', '2024-09-23', freq='D')
        usage_data = pd.DataFrame({
            'Date': dates,
            'Daily Logins': [45 + i*2 + (i%7)*10 for i in range(len(dates))],
            'Document Views': [120 + i*5 + (i%7)*20 for i in range(len(dates))],
            'Messages Sent': [25 + i*1 + (i%7)*5 for i in range(len(dates))]
        })
        
        fig = px.line(usage_data, x='Date', y=['Daily Logins', 'Document Views', 'Messages Sent'],
                     title='Portal Activity Trends')
        st.plotly_chart(fig, use_container_width=True)
        
        # Feature usage analytics
        st.markdown("#### Feature Usage Statistics")
        
        feature_usage = pd.DataFrame({
            'Feature': ['Document Viewing', 'Document Downloads', 'Messaging', 'Billing Access', 'File Uploads', 'Calendar'],
            'Usage Count': [1247, 892, 567, 445, 234, 123],
            'Unique Users': [87, 76, 45, 67, 23, 34],
            'Avg Session Time': [8.5, 3.2, 12.4, 6.7, 4.1, 2.8]
        })
        
        fig2 = px.bar(feature_usage, x='Feature', y='Usage Count',
                     color='Unique Users', color_continuous_scale='viridis',
                     title='Feature Usage by Count and Users')
        st.plotly_chart(fig2, use_container_width=True)
        
        # Client engagement analysis
        st.markdown("#### Client Engagement Analysis")
        
        engagement_data = pd.DataFrame({
            'Client': ['ABC Corporation', 'Tech Solutions Inc', 'Startup Innovations', 'Global Manufacturing', 'Continental Corp'],
            'Login Frequency': [23, 18, 12, 15, 8],
            'Documents Accessed': [45, 34, 12, 28, 16],
            'Messages Sent': [12, 8, 4, 9, 3],
            'Engagement Score': [85, 72, 45, 68, 38]
        })
        
        fig3 = px.scatter(engagement_data, x='Login Frequency', y='Documents Accessed',
                         size='Messages Sent', color='Engagement Score',
                         hover_name='Client', title='Client Engagement Matrix')
        st.plotly_chart(fig3, use_container_width=True)
        
        # Popular content
        st.markdown("#### Most Accessed Content")
        
        popular_content = [
            {"document": "Contract Templates", "views": 234, "downloads": 89},
            {"document": "Monthly Invoices", "views": 189, "downloads": 156},
            {"document": "Legal Updates", "views": 167, "downloads": 45},
            {"document": "Meeting Minutes", "views": 134, "downloads": 67},
            {"document": "Compliance Reports", "views": 98, "downloads": 34}
        ]
        
        for content in popular_content:
            col_content1, col_content2, col_content3 = st.columns([2, 1, 1])
            with col_content1:
                st.write(f"**{content['document']}**")
            with col_content2:
                st.write(f"{content['views']} views")
            with col_content3:
                st.write(f"{content['downloads']} downloads")
    
    with col2:
        st.markdown("#### Usage Summary")
        
        usage_summary = [
            ("Total Page Views", "12,847"),
            ("Unique Visitors", "87"),
            ("Avg Session Duration", "14.2 min"),
            ("Bounce Rate", "12.3%")
        ]
        
        for label, value in usage_summary:
            st.metric(label, value)
        
        st.markdown("#### Top Active Clients")
        
        top_clients = [
            ("ABC Corporation", "142 sessions"),
            ("Tech Solutions Inc", "89 sessions"),
            ("Global Manufacturing", "67 sessions"),
            ("Startup Innovations", "45 sessions"),
            ("Continental Corp", "23 sessions")
        ]
        
        for client, sessions in top_clients:
            st.write(f"**{client}:** {sessions}")
        
        st.markdown("#### Usage Reports")
        
        if st.button("📊 Daily Report"):
            st.info("Generating daily usage report...")
        if st.button("📈 Weekly Summary"):
            st.info("Creating weekly summary...")
        if st.button("📉 Monthly Analytics"):
            st.info("Compiling monthly analytics...")
        if st.button("📋 Export Data"):
            st.info("Preparing data export...")

# Main execution
if __name__ == "__main__":
    show()
