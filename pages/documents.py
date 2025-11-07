import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import uuid

# ADD SECURITY IMPORT
from services.data_security import DataSecurity

def show():
    # Require authentication FIRST
    DataSecurity.require_auth("Document Management")
    
    # Initialize session state with SECURE data
    if 'documents' not in st.session_state:
        st.session_state.documents = DataSecurity.get_user_documents()
    
    if 'current_viewing_doc' not in st.session_state:
        st.session_state.current_viewing_doc = None
    
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
        <h1>📄 Document Management</h1>
        <p>Organize, store, and manage all your legal documents</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Main tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📋 Dashboard", 
        "📤 Upload", 
        "🔍 Search & Filter", 
        "📊 Analytics", 
        "⚙️ Settings"
    ])
    
    with tab1:
        show_dashboard_stats()
    
    with tab2:
        show_upload_interface()
    
    with tab3:
        show_search_and_filter()
    
    with tab4:
        show_document_analytics()
    
    with tab5:
        show_document_settings()

def show_dashboard_stats():
    """Show dashboard with REAL user data"""
    
    # Check if viewing a document
    if st.session_state.current_viewing_doc:
        display_document_viewer(st.session_state.current_viewing_doc)
        return
    
    # Get REAL user documents
    documents = DataSecurity.get_user_documents()
    
    # Dashboard metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_docs = len(documents)
        st.metric("Total Documents", total_docs)
    
    with col2:
        draft_count = len([d for d in documents if d.get('status') == 'draft'])
        st.metric("Draft Documents", draft_count)
    
    with col3:
        # Calculate total storage
        total_size_bytes = sum(d.get('size_bytes', 0) for d in documents)
        total_size_gb = total_size_bytes / (1024 * 1024 * 1024)
        st.metric("Storage Used", f"{total_size_gb:.2f} GB")
    
    with col4:
        privileged_count = len([d for d in documents if d.get('is_privileged', False)])
        st.metric("Privileged Documents", privileged_count)
    
    # Recent documents
    st.subheader("Recent Documents")
    
    if documents:
        # Sort by upload date
        recent_docs = sorted(
            documents,
            key=lambda x: x.get('upload_date', ''),
            reverse=True
        )[:10]
        
        for doc in recent_docs:
            doc_id = doc.get('id', str(uuid.uuid4()))
            doc_name = doc.get('name', 'Unknown Document')
            doc_status = doc.get('status', 'unknown')
            doc_size = doc.get('size', 'Unknown size')
            
            with st.expander(f"📄 {doc_name}"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write(f"**Status:** {doc_status.title()}")
                
                with col2:
                    st.write(f"**Size:** {doc_size}")
                
                with col3:
                    if st.button("View", key=f"view_dashboard_{doc_id}"):
                        show_document_viewer(doc)
    else:
        st.info("No documents uploaded yet. Use the Upload tab to add your first document.")

def show_document_viewer(doc):
    """View document content - sets viewing state"""
    st.session_state.current_viewing_doc = doc
    st.rerun()


def display_document_viewer(doc):
    """Display document viewer interface"""
    st.markdown("### 📄 Document Viewer")
    
    doc_name = doc.get('name', 'Unknown')
    doc_type = doc.get('type', 'Unknown')
    doc_description = doc.get('description', 'No description')
    doc_tags = doc.get('tags', [])
    doc_id = doc.get('id')
    doc_size = doc.get('size', 'Unknown')
    upload_date = doc.get('upload_date', '')
    uploaded_by = doc.get('uploaded_by', 'Unknown')
    
    # Parse upload date
    if upload_date:
        try:
            dt = datetime.fromisoformat(upload_date)
            upload_date_str = dt.strftime('%Y-%m-%d %H:%M')
        except:
            upload_date_str = str(upload_date)[:16]
    else:
        upload_date_str = 'Unknown'
    
    # Close button at top
    if st.button("❌ Close Viewer", key="close_viewer_top"):
        st.session_state.current_viewing_doc = None
        st.rerun()
    
    st.markdown("---")
    
    # Document information
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 📋 Document Info")
        st.write(f"**Name:** {doc_name}")
        st.write(f"**Type:** {doc_type}")
        st.write(f"**Size:** {doc_size}")
    
    with col2:
        st.markdown("#### 📅 Details")
        st.write(f"**Uploaded:** {upload_date_str}")
        st.write(f"**By:** {uploaded_by}")
        st.write(f"**Status:** {doc.get('status', 'Unknown').title()}")
    
    with col3:
        st.markdown("#### 🏷️ Metadata")
        st.write(f"**Privileged:** {'Yes ⚖️' if doc.get('is_privileged') else 'No'}")
        if doc_tags:
            st.write(f"**Tags:** {', '.join(doc_tags)}")
        else:
            st.write("**Tags:** None")
    
    # Description
    if doc_description and doc_description != 'No description':
        st.markdown("#### 📝 Description")
        st.write(doc_description)
    
    st.markdown("---")
    
    # Document preview and download
    col_action1, col_action2 = st.columns([2, 1])
    
    with col_action1:
        st.markdown("#### 📄 Document Content")
        
        # Get actual file content
        if doc_id and doc_name:
            file_content = DataSecurity.get_document(doc_id, doc_name)
            
            if file_content:
                # Check file type for preview
                mime_type = doc.get('mime_type', '')
                
                if 'text' in mime_type or doc_name.endswith('.txt'):
                    # Text preview
                    try:
                        text_content = file_content.decode('utf-8', errors='ignore')
                        st.text_area("Text Preview", text_content[:2000], height=300, disabled=True)
                        if len(text_content) > 2000:
                            st.info("Showing first 2000 characters. Download to see full content.")
                    except:
                        st.info("Cannot preview this file type. Please download to view.")
                
                elif 'image' in mime_type or doc_name.endswith(('.png', '.jpg', '.jpeg', '.gif')):
                    # Image preview
                    st.image(file_content, caption=doc_name, use_container_width=True)
                
                elif 'pdf' in mime_type or doc_name.endswith('.pdf'):
                    st.info("📄 PDF Preview: Download the file to view full content")
                
                else:
                    st.info(f"Preview not available for {doc_type} files. Download to view.")
                
            else:
                st.warning("File content not available")
        else:
            st.info("No content available for preview")
    
    with col_action2:
        st.markdown("#### ⚡ Quick Actions")
        
        # Download button
        if doc_id and doc_name:
            file_content = DataSecurity.get_document(doc_id, doc_name)
            
            if file_content:
                st.download_button(
                    label="📥 Download Document",
                    data=file_content,
                    file_name=doc_name,
                    mime=doc.get('mime_type', 'application/octet-stream'),
                    use_container_width=True,
                    key="download_viewer"
                )
            else:
                st.button("📥 Download (N/A)", disabled=True, use_container_width=True)
        
        # Other actions
        if st.button("✏️ Edit Metadata", use_container_width=True):
            st.info("Edit functionality coming soon")
        
        if st.button("📤 Share", use_container_width=True):
            st.info("Share functionality coming soon")
        
        if st.button("🗑️ Delete Document", use_container_width=True):
            if st.button("⚠️ Confirm Delete", use_container_width=True, type="primary"):
                delete_document(doc)
                st.session_state.current_viewing_doc = None
                st.rerun()
    
    st.markdown("---")
    
    # Close button at bottom
    if st.button("❌ Close Viewer", key="close_viewer_bottom"):
        st.session_state.current_viewing_doc = None
        st.rerun()

def show_upload_interface():
    """SECURE document upload interface"""
    
    st.subheader("📤 Upload Documents")
    
    # File upload interface
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Single file upload
        st.markdown("#### Single File Upload")
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=['pdf', 'docx', 'txt', 'png', 'jpg', 'jpeg', 'xlsx', 'pptx'],
            help="Supported formats: PDF, Word, Text, Images, Excel, PowerPoint"
        )
        
        if uploaded_file:
            file_size_mb = uploaded_file.size / (1024 * 1024)
            st.write(f"**File:** {uploaded_file.name}")
            st.write(f"**Size:** {file_size_mb:.1f} MB")
            st.write(f"**Type:** {uploaded_file.type}")
            
            # File metadata form
            with st.form("file_upload_form"):
                st.markdown("#### File Details")
                
                col_form1, col_form2 = st.columns(2)
                
                with col_form1:
                    document_title = st.text_input("Document Title", value=uploaded_file.name)
                    document_type = st.selectbox("Document Type", [
                        "Contract", "Legal Brief", "Correspondence", 
                        "Court Filing", "Research", "Template", 
                        "Invoice", "Other"
                    ])
                    
                    # Get user's matters for dropdown
                    matters = DataSecurity.get_user_matters()
                    matter_options = ["None"] + [m.get('name', f"Matter {i}") for i, m in enumerate(matters)]
                    matter_id = st.selectbox("Associated Matter", options=matter_options)
                
                with col_form2:
                    tags = st.text_input("Tags (comma-separated)", placeholder="urgent, contract, client-a")
                    is_privileged = st.checkbox("Attorney-Client Privileged")
                    description = st.text_area("Description", height=100)
                
                # Upload button
                if st.form_submit_button("📤 Upload Document", type="primary"):
                    success = process_document_upload(
                        uploaded_file, document_title, document_type, 
                        matter_id, tags, is_privileged, description
                    )
                    
                    if success:
                        st.success(f"✅ Successfully uploaded: {document_title}")
                        st.rerun()
    
    with col2:
        # Upload guidelines
        st.markdown("#### Upload Guidelines")
        
        st.markdown("**Max file size:** 100MB")
        
        st.markdown("#### Supported Formats")
        formats = [
            "📄 PDF documents",
            "📝 Word documents", 
            "📊 Excel spreadsheets",
            "🖼️ Images (JPG, PNG)",
            "📑 Text files",
            "📋 PowerPoint"
        ]
        
        for format_type in formats:
            st.write(format_type)

def process_document_upload(uploaded_file, title, doc_type, matter_id, tags, is_privileged, description):
    """Process document upload SECURELY"""
    try:
        # Read file content
        uploaded_file.seek(0)
        file_content = uploaded_file.read()
        
        # Generate document ID
        doc_id = str(uuid.uuid4())
        
        # Save actual file using DataSecurity
        file_path = DataSecurity.save_document(
            doc_id,
            file_content,
            uploaded_file.name,
            uploaded_file.type
        )
        
        if not file_path:
            st.error("Failed to save file")
            return False
        
        # Create document metadata
        user_email = DataSecurity.get_current_user_email()
        user_name = st.session_state.get('user_data', {}).get('name', 'Unknown')
        
        new_document = {
            'id': doc_id,
            'name': title,
            'original_filename': uploaded_file.name,
            'type': doc_type,
            'mime_type': uploaded_file.type,
            'matter_id': matter_id if matter_id != "None" else None,
            'tags': [tag.strip() for tag in tags.split(',') if tag.strip()],
            'is_privileged': is_privileged,
            'description': description,
            'size': f"{uploaded_file.size / (1024 * 1024):.1f} MB",
            'size_bytes': uploaded_file.size,
            'upload_date': datetime.now().isoformat(),
            'uploaded_by': user_name,
            'uploaded_by_email': user_email,
            'status': 'active',
            'path': file_path
        }
        
        # Add to session state
        if 'documents' not in st.session_state:
            st.session_state.documents = []
        
        st.session_state.documents.append(new_document)
        
        # Save to persistent storage
        DataSecurity.save_user_data('documents', st.session_state.documents)
        
        return True
        
    except Exception as e:
        st.error(f"Upload failed: {str(e)}")
        return False

def show_search_and_filter():
    """Document search with REAL user data"""
    
    # ✅ Check if viewing a document
    if st.session_state.current_viewing_doc:
        display_document_viewer(st.session_state.current_viewing_doc)
        return
    st.subheader("🔍 Search & Filter Documents")
    
    # Get REAL documents
    documents = DataSecurity.get_user_documents()
    
    # Search interface
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        search_query = st.text_input("🔍 Search documents", placeholder="Enter keywords, tags, or document names...")
    
    with col2:
        doc_type_filter = st.selectbox("Document Type", 
                                     ["All Types"] + ["Contract", "Legal Brief", "Correspondence", 
                                                     "Court Filing", "Research", "Template", "Invoice", "Other"])
    
    with col3:
        date_filter = st.selectbox("Date Range", 
                                 ["All Time", "Last 7 days", "Last 30 days", "Last 90 days", "This Year"])
    
    # Apply filters
    filtered_documents = apply_document_filters(
        documents, search_query, doc_type_filter, date_filter
    )
    
    # Results
    st.markdown(f"### Search Results ({len(filtered_documents)} documents)")
    
    if filtered_documents:
        # Display options
        col1, col2 = st.columns([1, 1])
        
        with col1:
            view_mode = st.radio("View Mode", ["List", "Table"], horizontal=True)
        
        with col2:
            sort_by = st.selectbox("Sort By", ["Upload Date", "Name", "Size", "Type"])
        
        # Sort documents
        filtered_documents = sort_documents(filtered_documents, sort_by)
        
        # Display
        if view_mode == "List":
            show_document_list(filtered_documents)
        else:
            show_document_table(filtered_documents)
    else:
        st.info("No documents match your search criteria.")

def apply_document_filters(documents, search_query, doc_type, date_filter):
    """Apply filters to document list"""
    filtered = documents.copy()
    
    # Search query
    if search_query:
        search_lower = search_query.lower()
        filtered = [doc for doc in filtered 
                   if search_lower in doc.get('name', '').lower() or 
                      search_lower in doc.get('description', '').lower() or
                      any(search_lower in tag.lower() for tag in doc.get('tags', []))]
    
    # Document type
    if doc_type != "All Types":
        filtered = [doc for doc in filtered if doc.get('type') == doc_type]
    
    # Date filter
    if date_filter != "All Time":
        cutoff_date = get_date_cutoff(date_filter)
        filtered = [doc for doc in filtered 
                   if doc.get('upload_date', '') >= cutoff_date.isoformat()]
    
    return filtered

def get_date_cutoff(date_filter):
    """Get cutoff date"""
    now = datetime.now()
    
    if date_filter == "Last 7 days":
        return now - timedelta(days=7)
    elif date_filter == "Last 30 days":
        return now - timedelta(days=30)
    elif date_filter == "Last 90 days":
        return now - timedelta(days=90)
    elif date_filter == "This Year":
        return now.replace(month=1, day=1, hour=0, minute=0, second=0)
    
    return datetime.min

def sort_documents(documents, sort_by):
    """Sort documents"""
    if sort_by == "Name":
        return sorted(documents, key=lambda x: x.get('name', '').lower())
    elif sort_by == "Upload Date":
        return sorted(documents, key=lambda x: x.get('upload_date', ''), reverse=True)
    elif sort_by == "Size":
        return sorted(documents, key=lambda x: x.get('size_bytes', 0), reverse=True)
    elif sort_by == "Type":
        return sorted(documents, key=lambda x: x.get('type', ''))
    
    return documents

def show_document_list(documents):
    """Show documents in list view"""
    for doc in documents:
        doc_id = doc.get('id')
        doc_name = doc.get('name', 'Unknown')
        
        with st.expander(f"📄 {doc_name} - {doc.get('type', 'Unknown Type')}"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write(f"**Type:** {doc.get('type', 'Unknown')}")
                st.write(f"**Size:** {doc.get('size', 'Unknown')}")
                
                upload_date = doc.get('upload_date', '')
                if upload_date:
                    try:
                        dt = datetime.fromisoformat(upload_date)
                        st.write(f"**Uploaded:** {dt.strftime('%Y-%m-%d')}")
                    except:
                        st.write(f"**Uploaded:** {upload_date}")
            
            with col2:
                st.write(f"**Status:** {doc.get('status', 'Unknown')}")
                st.write(f"**Privileged:** {'Yes' if doc.get('is_privileged') else 'No'}")
                st.write(f"**Uploaded by:** {doc.get('uploaded_by', 'Unknown')}")
            
            with col3:
                if doc.get('tags'):
                    st.write(f"**Tags:** {', '.join(doc['tags'])}")
                if doc.get('description'):
                    st.write(f"**Description:** {doc['description'][:100]}...")
            
            # Action buttons
            col_action1, col_action2, col_action3, col_action4 = st.columns(4)
            
            with col_action1:
                if st.button("👁️ View", key=f"view_list_{doc_id}"):
                    show_document_viewer(doc)
            
            with col_action2:
                # Download with actual file
                if doc_id and doc_name:
                    file_content = DataSecurity.get_document(doc_id, doc_name)
                    
                    if file_content:
                        st.download_button(
                            label="📥 Download",
                            data=file_content,
                            file_name=doc_name,
                            mime=doc.get('mime_type', 'application/octet-stream'),
                            key=f"download_list_{doc_id}"
                        )
            
            with col_action3:
                if st.button("✏️ Edit", key=f"edit_{doc_id}"):
                    st.info("Edit interface coming soon")
            
            with col_action4:
                if st.button("🗑️ Delete", key=f"delete_{doc_id}"):
                    delete_document(doc)

def show_document_table(documents):
    """Show documents in table view"""
    if documents:
        table_data = []
        for doc in documents:
            upload_date = doc.get('upload_date', '')
            if upload_date:
                try:
                    dt = datetime.fromisoformat(upload_date)
                    date_str = dt.strftime('%Y-%m-%d')
                except:
                    date_str = str(upload_date)[:10]
            else:
                date_str = 'Unknown'
            
            table_data.append({
                "Name": doc.get('name', 'Unknown'),
                "Type": doc.get('type', 'Unknown'),
                "Size": doc.get('size', 'Unknown'),
                "Upload Date": date_str,
                "Status": doc.get('status', 'Unknown'),
                "Privileged": "Yes" if doc.get('is_privileged') else "No"
            })
        
        df = pd.DataFrame(table_data)
        st.dataframe(df, use_container_width=True)

def delete_document(doc):
    """SECURELY delete a document"""
    try:
        doc_id = doc.get('id')
        doc_name = doc.get('name')
        
        # Delete actual file
        if doc_id and doc_name:
            DataSecurity.delete_document(doc_id, doc_name)
        
        # Remove from session state
        st.session_state.documents = [d for d in st.session_state.documents if d.get('id') != doc_id]
        
        # Save updated list
        DataSecurity.save_user_data('documents', st.session_state.documents)
        
        st.success(f"Document '{doc_name}' deleted successfully!")
        st.rerun()
        
    except Exception as e:
        st.error(f"Error deleting document: {str(e)}")

def show_document_analytics():
    """Show document analytics with REAL data"""
    st.subheader("📊 Document Analytics")
    
    documents = DataSecurity.get_user_documents()
    
    if documents:
        # Document type distribution
        col1, col2 = st.columns(2)
        
        with col1:
            doc_types = {}
            for doc in documents:
                doc_type = doc.get('type', 'Unknown')
                doc_types[doc_type] = doc_types.get(doc_type, 0) + 1
            
            if doc_types:
                fig1 = px.pie(values=list(doc_types.values()), names=list(doc_types.keys()),
                             title="Document Distribution by Type")
                st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # Storage by type
            storage_by_type = {}
            for doc in documents:
                doc_type = doc.get('type', 'Unknown')
                size_bytes = doc.get('size_bytes', 0)
                storage_by_type[doc_type] = storage_by_type.get(doc_type, 0) + size_bytes
            
            # Convert to MB
            storage_mb = {k: v / (1024 * 1024) for k, v in storage_by_type.items()}
            
            if storage_mb:
                fig2 = px.bar(x=list(storage_mb.keys()), y=list(storage_mb.values()),
                             title="Storage by Document Type (MB)")
                st.plotly_chart(fig2, use_container_width=True)
    
    else:
        st.info("No documents available for analytics.")

def show_document_settings():
    """Document settings"""
    st.subheader("⚙️ Document Settings")
    
    # Document preferences
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Default Settings")
        
        default_doc_type = st.selectbox(
            "Default Document Type",
            ["Contract", "Legal Brief", "Correspondence", "Court Filing", "Research", "Template", "Invoice", "Other"],
            index=0
        )
        
        auto_extract_text = st.checkbox("Auto-extract text from uploaded documents", value=True)
        auto_tag_documents = st.checkbox("Enable automatic document tagging", value=True)
    
    with col2:
        st.markdown("#### Security Settings")
        
        require_approval = st.checkbox("Require approval for document sharing", value=False)
        watermark_documents = st.checkbox("Add watermark to downloaded documents", value=False)
    
    # Save settings
    if st.button("💾 Save Settings", type="primary"):
        settings = {
            'default_doc_type': default_doc_type,
            'auto_extract_text': auto_extract_text,
            'auto_tag_documents': auto_tag_documents,
            'require_approval': require_approval,
            'watermark_documents': watermark_documents
        }
        
        DataSecurity.save_user_data('document_settings', settings)
        st.success("Settings saved successfully!")

# Main execution
if __name__ == "__main__":
    show()
