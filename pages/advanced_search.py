import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json

def show():
    # Initialize session state for search results and interactions
    if 'search_results' not in st.session_state:
        st.session_state.search_results = None
    if 'search_query' not in st.session_state:
        st.session_state.search_query = ""
    if 'document_results' not in st.session_state:
        st.session_state.document_results = None
    if 'ai_results' not in st.session_state:
        st.session_state.ai_results = None
    if 'notification' not in st.session_state:
        st.session_state.notification = None
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

    /* Dropdown menus - comprehensive fix */

    /* The dropdown container itself */
    .stSelectbox,
    [data-testid="stSelectbox"] {
        background: white !important;
        border-radius: 8px !important;
    }
    
    /* Dropdown button/selector - dark text */
    .stSelectbox [data-baseweb="select"],
    [data-testid="stSelectbox"] [data-baseweb="select"],
    .stSelectbox [data-baseweb="select"] > div,
    [data-testid="stSelectbox"] [data-baseweb="select"] > div {
        background: white !important;
        color: #1e293b !important;
    }
    
    /* All text inside the dropdown selector */
    .stSelectbox [data-baseweb="select"] *,
    [data-testid="stSelectbox"] [data-baseweb="select"] * {
        color: #1e293b !important;
    }
    
    /* Dropdown popover/menu when opened */
    [data-baseweb="popover"],
    [role="listbox"],
    [data-baseweb="menu"] {
        background: white !important;
    }
    
    /* All options in dropdown list */
    [data-baseweb="popover"] *,
    [role="listbox"] *,
    [role="option"],
    [role="option"] *,
    [data-baseweb="menu"] li,
    [data-baseweb="menu"] li * {
        color: #1e293b !important;
        background: white !important;
    }
    
    /* Selected option */
    [aria-selected="true"] {
        background: rgba(59, 130, 246, 0.1) !important;
        color: #1e293b !important;
    }
    
    /* Hovered option */
    [role="option"]:hover,
    [data-baseweb="menu"] li:hover {
        background: rgba(59, 130, 246, 0.15) !important;
        color: #1e293b !important;
    }
    
    /* Multi-select tags */
    .stMultiSelect [data-baseweb="tag"],
    .stMultiSelect [data-baseweb="tag"] * {
        background: rgba(59, 130, 246, 0.2) !important;
        color: #1e293b !important;
    }
    
    /* Dropdown arrow/icon */
    .stSelectbox svg,
    [data-testid="stSelectbox"] svg {
        fill: #1e293b !important;
    }

    /* Streamlit selectbox - force dark text everywhere */
    div[data-baseweb="select"] {
        background: white !important;
    }
    
    div[data-baseweb="select"] > div,
    div[data-baseweb="select"] > div > div,
    div[data-baseweb="select"] span,
    div[data-baseweb="select"] input {
        color: #1e293b !important;
        background: white !important;
    }
    
    /* The actual dropdown panel when opened */
    ul[role="listbox"] {
        background: white !important;
    }
    
    ul[role="listbox"] li,
    ul[role="listbox"] li * {
        color: #1e293b !important;
    }
    
    /* Force override any remaining light text in dropdowns */
    [data-baseweb="select"] [data-baseweb="select-dropdown"] *,
    [data-baseweb="popover-content"] *,
    .stSelectbox * {
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
        <h1>🔍 Advanced Search</h1>
        <p>Powerful search across all documents and matters</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Search tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🔍 Universal Search", 
        "📄 Document Search", 
        "📊 Data Analytics", 
        "🤖 AI-Powered Search", 
        "📚 Legal Research",
        "🗂️ Search Management"
    ])
    
    with tab1:
        show_universal_search()
    
    with tab2:
        show_document_search()
    
    with tab3:
        show_data_analytics()
    
    with tab4:
        show_ai_powered_search()
    
    with tab5:
        show_legal_research()
    
    with tab6:
        show_search_management()


def get_universal_search_results(query):
    """Search across actual documents in session state"""
    query_lower = query.lower()
    results = []
    
    # Search through matters and their documents
    if 'matters' in st.session_state:
        for matter in st.session_state.matters:
            # Search in matter documents
            if 'documents' in matter:
                for doc in matter['documents']:
                    # Check if query matches document
                    if (query_lower in doc.get('name', '').lower() or 
                        query_lower in doc.get('description', '').lower() or
                        query_lower in matter.get('name', '').lower()):
                        
                        results.append({
                            "type": "Document",
                            "title": doc.get('name', 'Untitled'),
                            "content": doc.get('description', 'No description')[:200] + "...",
                            "author": doc.get('uploaded_by', 'Unknown'),
                            "date": doc.get('upload_date', 'N/A'),
                            "matter": matter.get('name', 'Unknown'),
                            "relevance": calculate_relevance(query_lower, doc, matter),
                            "tags": doc.get('tags', []),
                            "keywords": extract_keywords(doc)
                        })
            
            # Search in matter details
            if query_lower in matter.get('name', '').lower() or query_lower in matter.get('description', '').lower():
                results.append({
                    "type": "Matter",
                    "title": matter.get('name', 'Untitled Matter'),
                    "content": matter.get('description', 'No description')[:200] + "...",
                    "author": matter.get('lead_attorney', 'Unknown'),
                    "date": matter.get('created_date', 'N/A'),
                    "matter": matter.get('name', 'Unknown'),
                    "relevance": calculate_relevance(query_lower, {}, matter),
                    "tags": matter.get('tags', []),
                    "keywords": []
                })
    
    # Sort by relevance
    results.sort(key=lambda x: x['relevance'], reverse=True)
    
    return results if results else []

def calculate_relevance(query, doc, matter):
    """Calculate relevance score based on keyword matches"""
    score = 0
    
    # Check document name
    if query in doc.get('name', '').lower():
        score += 40
    
    # Check document description
    if query in doc.get('description', '').lower():
        score += 30
    
    # Check matter name
    if query in matter.get('name', '').lower():
        score += 20
    
    # Check tags
    if any(query in tag.lower() for tag in doc.get('tags', [])):
        score += 10
    
    return min(score, 100)  # Cap at 100

def extract_keywords(doc):
    """Extract keywords from document for search matching"""
    keywords = []
    
    # Extract from name
    if 'name' in doc:
        keywords.extend(doc['name'].lower().split())
    
    # Extract from tags
    if 'tags' in doc:
        keywords.extend([tag.lower() for tag in doc['tags']])
    
    # Extract from description
    if 'description' in doc:
        keywords.extend(doc['description'].lower().split()[:10])  # First 10 words
    
    return list(set(keywords))  # Remove duplicates

def show_universal_search():
    st.subheader("🔍 Universal Search")
    
    # Search interface
    col1, col2 = st.columns([4, 1])
    
    with col1:
        search_query = st.text_input("", placeholder="Search across all documents, matters, communications, and data...", key="universal_search")
    with col2:
        search_button = st.button("🔍 Search", type="primary")
    
    # Search filters
    with st.expander("🔧 Advanced Filters"):
        col_a, col_b, col_c, col_d = st.columns(4)
        
        with col_a:
            content_types = st.multiselect("Content Types:", 
                ["Documents", "Emails", "Matters", "Contacts", "Calendar Events", "Tasks"])
        with col_b:
            date_range = st.date_input("Date Range:", value=[datetime.now() - timedelta(days=365), datetime.now()])
        with col_c:
            authors = st.multiselect("Authors:", ["John Smith", "Sarah Johnson", "Mike Davis", "Emily Chen", "All Attorneys"])
        with col_d:
            matters = st.multiselect("Related Matters:", ["ABC Corp Acquisition", "Johnson vs. Tech Solutions", "Continental Corp Defense"])
    
    # Store search query in session state
    if search_button and search_query:
        st.session_state.search_query = search_query
        st.session_state.search_results = get_universal_search_results(search_query)
    
    # Display notification if exists
    if st.session_state.notification:
        st.success(st.session_state.notification)
        st.session_state.notification = None
    
    if st.session_state.search_results:
        search_results = st.session_state.search_results
        
        st.markdown("#### Search Results")
        
        # Results summary
        col_sum1, col_sum2, col_sum3, col_sum4 = st.columns(4)
        with col_sum1:
            st.metric("Total Results", len(search_results))
        with col_sum2:
            st.metric("Documents", sum(1 for r in search_results if r["type"] == "Document"))
        with col_sum3:
            st.metric("Emails", sum(1 for r in search_results if r["type"] == "Email"))
        with col_sum4:
            st.metric("Avg Relevance", f"{sum(r['relevance'] for r in search_results) / len(search_results):.1f}%")
        
        # Sort and filter options
        col_sort1, col_sort2, col_sort3 = st.columns(3)
        with col_sort1:
            sort_by = st.selectbox("Sort By:", ["Relevance", "Date", "Author", "Matter"])
        with col_sort2:
            result_limit = st.selectbox("Show Results:", ["All", "Top 10", "Top 25", "Top 50"])
        with col_sort3:
            export_option = st.selectbox("Export:", ["None", "CSV", "PDF Report", "JSON"])
        
        # Display results
        for i, result in enumerate(search_results, 1):
            type_icons = {"Document": "📄", "Email": "📧", "Matter": "⚖️", "Task": "✅", "Contact": "👤"}
            
            with st.expander(f"{type_icons.get(result['type'], '📄')} {result['title']} ({result['relevance']}% relevant)"):
                col_res1, col_res2 = st.columns([3, 1])
                
                with col_res1:
                    st.write(f"**Content Preview:** {result['content']}")
                    st.write(f"**Type:** {result['type']} | **Author:** {result['author']} | **Date:** {result['date']}")
                    st.write(f"**Related Matter:** {result['matter']}")
                    
                    tag_display = " ".join([f"`{tag}`" for tag in result['tags']])
                    st.markdown(f"**Tags:** {tag_display}")
                
                with col_res2:
                    st.progress(result['relevance'] / 100)
                    st.write(f"Relevance: {result['relevance']}%")
                    
                    # Action buttons with callbacks
                    if st.button(f"📖 Open", key=f"open_{i}_{result['title'][:10]}"):
                        st.session_state.notification = f"Opening: {result['title']}"
                        st.rerun()
                    
                    if st.button(f"📎 Add to Collection", key=f"collect_{i}_{result['title'][:10]}"):
                        st.session_state.notification = f"Added '{result['title']}' to collection!"
                        st.rerun()
                    
                    if st.button(f"🏷️ Add Tags", key=f"tag_{i}_{result['title'][:10]}"):
                        st.session_state.notification = "Tag editor opened"
                        st.rerun()

def show_document_search():
    st.subheader("📄 Advanced Document Search")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Document search interface
        st.markdown("#### Search Parameters")
        
        col_a, col_b = st.columns(2)
        with col_a:
            doc_search_query = st.text_input("Document Content Search:", placeholder="Enter keywords, phrases, or document content...")
        with col_b:
            doc_type = st.selectbox("Document Type:", ["All Types", "Contracts", "Briefs", "Motions", "Discovery", "Correspondence"])
        
        col_c, col_d, col_e = st.columns(3)
        with col_c:
            file_format = st.selectbox("File Format:", ["All Formats", "PDF", "DOCX", "TXT", "XLSX"])
        with col_d:
            size_range = st.selectbox("File Size:", ["Any Size", "< 1MB", "1-10MB", "10-50MB", "> 50MB"])
        with col_e:
            language = st.selectbox("Language:", ["All Languages", "English", "Spanish", "French"])
        
        # Advanced search options
        with st.expander("🔧 Advanced Search Options"):
            col_adv1, col_adv2 = st.columns(2)
            
            with col_adv1:
                exact_phrase = st.text_input("Exact Phrase:", placeholder="\"exact phrase in quotes\"")
                any_words = st.text_input("Any of These Words:", placeholder="word1 OR word2 OR word3")
                exclude_words = st.text_input("Exclude Words:", placeholder="NOT word1 NOT word2")
                
                # OCR and content analysis
                ocr_search = st.checkbox("Search OCR Text (Scanned Documents)")
                metadata_search = st.checkbox("Include Metadata Search")
            
            with col_adv2:
                version_control = st.checkbox("Search All Versions")
                annotations = st.checkbox("Include Annotations & Comments")
                
                # Date filters
                creation_date = st.date_input("Created After:", value=None)
                modified_date = st.date_input("Modified After:", value=None)
        
        if st.button("🔍 Search Documents", type="primary"):
            st.session_state.document_results = get_document_search_results(doc_search_query, doc_type)
        
        # Display notification
        if st.session_state.notification:
            st.success(st.session_state.notification)
            st.session_state.notification = None
        
        if st.session_state.document_results:
            document_results = st.session_state.document_results
            
            st.markdown("#### Document Search Results")
            
            # Enhanced results display
            for idx, doc in enumerate(document_results):
                with st.expander(f"📄 {doc['filename']} ({doc['matches']} matches, {doc['relevance']}% relevant)"):
                    col_doc1, col_doc2, col_doc3 = st.columns(3)
                    
                    with col_doc1:
                        st.write(f"**Size:** {doc['size']}")
                        st.write(f"**Pages:** {doc['pages']}")
                        st.write(f"**Version:** {doc['version']}")
                        st.write(f"**Status:** {doc['status']}")
                    
                    with col_doc2:
                        st.write(f"**Author:** {doc['author']}")
                        st.write(f"**Matter:** {doc['matter']}")
                        st.write(f"**Created:** {doc['created']}")
                        st.write(f"**Modified:** {doc['last_modified']}")
                    
                    with col_doc3:
                        st.progress(doc['relevance'] / 100)
                        st.write(f"Relevance: {doc['relevance']}%")
                        st.write(f"**Security:** {doc['security']}")
                        st.write(f"**Path:** {doc['path']}")
                    
                    # Enhanced action buttons with real functionality
                    col_btn1, col_btn2, col_btn3, col_btn4, col_btn5 = st.columns(5)
                    
                    with col_btn1:
                        if st.button("👁️ Preview", key=f"preview_doc_{idx}"):
                            st.session_state.preview_doc = doc.get('file_data')
                            st.session_state.notification = f"Opening preview for {doc['filename']}"
                            st.rerun()
                    
                    with col_btn2:
                        # Download button - check if file content exists
                        if 'file_data' in doc and doc['file_data'] and 'content' in doc['file_data']:
                            st.download_button(
                                label="📥 Download",
                                data=doc['file_data']['content'],
                                file_name=doc['filename'],
                                mime=doc['file_data'].get('mime_type', 'application/octet-stream'),
                                key=f"download_doc_{idx}"
                            )
                        else:
                            if st.button("📥 Download", key=f"download_doc_{idx}_disabled"):
                                st.session_state.notification = "File content not available for download"
                                st.rerun()
                    
                    with col_btn3:
                        if st.button("✏️ Annotate", key=f"annotate_doc_{idx}"):
                            st.session_state.annotate_doc = doc.get('file_data')
                            st.session_state.notification = f"Opening annotation tool for {doc['filename']}"
                            st.rerun()
                    
                    with col_btn4:
                        if st.button("📧 Share", key=f"share_doc_{idx}"):
                            st.session_state.share_doc = doc
                            st.session_state.notification = f"Opening share dialog for {doc['filename']}"
                            st.rerun()
                    
                    with col_btn5:
                        if st.button("🔄 Versions", key=f"versions_doc_{idx}"):
                            st.session_state.version_doc = doc.get('file_data')
                            st.session_state.notification = f"Showing version history for {doc['filename']}"
                            st.rerun()
            
            # Document Preview Section
            if 'preview_doc' in st.session_state and st.session_state.preview_doc:
                st.markdown("---")
                st.markdown("#### 📄 Document Preview")
                
                preview_doc = st.session_state.preview_doc
                
                col_prev1, col_prev2 = st.columns([3, 1])
                
                with col_prev1:
                    st.markdown(f"**File:** {preview_doc.get('name', 'Unknown')}")
                    st.markdown(f"**Description:** {preview_doc.get('description', 'No description available')}")
                    
                    # Show file content preview based on type
                    file_type = preview_doc.get('type', '').lower()
                    
                    if 'text' in file_type or file_type.endswith('.txt'):
                        # Text file preview
                        if 'content' in preview_doc:
                            content = preview_doc['content']
                            if isinstance(content, bytes):
                                content = content.decode('utf-8', errors='ignore')
                            st.text_area("Content Preview:", content[:1000], height=300)
                            if len(content) > 1000:
                                st.info("Showing first 1000 characters. Download full file to see more.")
                    
                    elif 'pdf' in file_type:
                        st.info("📄 PDF Preview: Download file to view full content")
                        # Could integrate PDF viewer here if needed
                    
                    elif file_type in ['image/png', 'image/jpeg', 'image/jpg', 'image/gif']:
                        # Image preview
                        if 'content' in preview_doc:
                            st.image(preview_doc['content'], caption=preview_doc.get('name'))
                    
                    else:
                        st.info(f"Preview not available for file type: {file_type}")
                        st.write("Download the file to view its contents.")
                
                with col_prev2:
                    st.markdown("**File Information:**")
                    st.write(f"Type: {preview_doc.get('type', 'Unknown')}")
                    st.write(f"Size: {preview_doc.get('size', 'Unknown')}")
                    st.write(f"Uploaded: {preview_doc.get('upload_date', 'Unknown')}")
                    st.write(f"By: {preview_doc.get('uploaded_by', 'Unknown')}")
                    
                    if st.button("❌ Close Preview"):
                        st.session_state.preview_doc = None
                        st.rerun()
    
    with col2:
        st.markdown("#### Search Statistics")
        
        # Calculate real statistics if documents exist
        if 'matters' in st.session_state:
            total_docs = sum(len(matter.get('documents', [])) for matter in st.session_state.matters)
            stats = [
                ("Total Documents", str(total_docs)),
                ("Searchable Content", "100%"),
                ("Active Matters", str(len(st.session_state.matters))),
                ("Last Updated", "Just now")
            ]
        else:
            stats = [
                ("Total Documents", "0"),
                ("Searchable Content", "N/A"),
                ("Active Matters", "0"),
                ("Last Updated", "N/A")
            ]
        
        for label, value in stats:
            st.metric(label, value)
        
        st.markdown("#### Quick Filters")
        quick_filters = [
            "📄 Recent Documents",
            "⭐ Frequently Accessed", 
            "🔒 Confidential Only",
            "📝 Draft Documents",
            "✅ Final Versions",
            "📊 Excel Files",
            "📋 Templates"
        ]
        
        for filter_option in quick_filters:
            if st.button(filter_option, key=f"filter_{filter_option[:5]}"):
                # Apply filter logic here
                filter_keyword = filter_option.split()[1].lower() if len(filter_option.split()) > 1 else ""
                st.session_state.document_results = get_document_search_results(filter_keyword, "All Types")
                st.session_state.notification = f"Applied filter: {filter_option}"
                st.rerun()
        
        st.markdown("#### Saved Searches")
        saved_searches = [
            "Contract amendments 2024",
            "Patent litigation docs", 
            "Client correspondence",
            "Discovery materials",
            "Employment agreements"
        ]
        
        for search in saved_searches:
            col_search1, col_search2 = st.columns([3, 1])
            with col_search1:
                st.write(f"• {search}")
            with col_search2:
                if st.button("🔍", key=f"saved_{search[:10]}"):
                    # Run saved search
                    search_term = search.split()[0].lower()
                    st.session_state.document_results = get_document_search_results(search_term, "All Types")
                    st.session_state.notification = f"Running saved search: {search}"
                    st.rerun()

def get_document_search_results(query, doc_type):
    """Search actual documents with type filtering"""
    results = []
    
    if 'matters' not in st.session_state:
        return results
    
    for matter in st.session_state.matters:
        if 'documents' not in matter:
            continue
            
        for doc in matter['documents']:
            # Filter by document type if specified
            if doc_type != "All Types":
                if doc.get('type', '') != doc_type:
                    continue
            
            # Filter by query
            if query:
                query_lower = query.lower()
                if not (query_lower in doc.get('name', '').lower() or 
                       query_lower in doc.get('description', '').lower()):
                    continue
            
            # Get file info
            file_size = doc.get('size', 0)
            size_str = f"{file_size / 1024:.1f} KB" if file_size < 1024*1024 else f"{file_size / (1024*1024):.1f} MB"
            
            results.append({
                "filename": doc.get('name', 'Untitled'),
                "path": doc.get('path', '/unknown/'),
                "size": size_str,
                "pages": doc.get('pages', 'N/A'),
                "last_modified": doc.get('modified_date', doc.get('upload_date', 'N/A')),
                "created": doc.get('upload_date', 'N/A'),
                "author": doc.get('uploaded_by', 'Unknown'),
                "matter": matter.get('name', 'Unknown'),
                "matches": count_query_matches(query, doc),
                "relevance": calculate_relevance(query.lower() if query else '', doc, matter),
                "version": doc.get('version', '1.0'),
                "status": doc.get('status', 'Active'),
                "security": doc.get('security_level', 'Standard'),
                "type": doc.get('type', 'Document'),
                "keywords": extract_keywords(doc),
                "file_data": doc  # Store reference to actual file
            })
    
    return results

def count_query_matches(query, doc):
    """Count how many times query appears in document"""
    if not query:
        return 0
    
    query_lower = query.lower()
    count = 0
    
    # Count in name
    count += doc.get('name', '').lower().count(query_lower)
    
    # Count in description
    count += doc.get('description', '').lower().count(query_lower)
    
    return count



def show_data_analytics():
    st.subheader("📊 Search & Data Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Search Pattern Analysis")
        
        # Search frequency chart
        search_data = pd.DataFrame({
            'Date': pd.date_range('2024-09-01', '2024-09-23', freq='D'),
            'Searches': [45, 52, 38, 67, 43, 59, 71, 48, 63, 56, 72, 41, 58, 69, 44, 61, 47, 55, 73, 49, 64, 57, 68]
        })
        
        fig_search = px.line(search_data, x='Date', y='Searches', title='Daily Search Volume')
        st.plotly_chart(fig_search, use_container_width=True)
        
        st.markdown("#### Most Searched Terms")
        
        search_terms = pd.DataFrame({
            'Term': ['contract', 'agreement', 'liability', 'intellectual property', 'termination', 'confidentiality'],
            'Frequency': [247, 198, 156, 134, 112, 98],
            'Trend': ['📈', '📈', '➡️', '📈', '📉', '➡️']
        })
        
        for _, row in search_terms.iterrows():
            col_term1, col_term2, col_term3 = st.columns([2, 1, 1])
            with col_term1:
                st.write(f"**{row['Term']}**")
            with col_term2:
                st.write(f"{row['Frequency']} searches")
            with col_term3:
                st.write(row['Trend'])
        
        # Search success rate
        st.markdown("#### Search Performance Metrics")
        
        performance_metrics = [
            ("Search Success Rate", "89.2%", "+2.1%"),
            ("Avg Results per Search", "24.7", "+3.2"),
            ("Zero Results Rate", "5.8%", "-1.4%"),
            ("User Satisfaction", "4.2/5", "+0.3")
        ]
        
        for metric, value, change in performance_metrics:
            st.metric(metric, value, change)
    
    with col2:
        st.markdown("#### Document Access Patterns")
        
        # Document type access pie chart
        doc_access_data = pd.DataFrame({
            'Document Type': ['Contracts', 'Correspondence', 'Briefs', 'Discovery', 'Other'],
            'Access Count': [342, 287, 198, 156, 89]
        })
        
        fig_pie = px.pie(doc_access_data, values='Access Count', names='Document Type', 
                        title='Document Access by Type')
        st.plotly_chart(fig_pie, use_container_width=True)
        
        # Document access metrics
        access_metrics = [
            ("Total Documents Accessed", "1,247", "+8.2%"),
            ("Unique Users", "23", "+2"),
            ("Avg. Session Duration", "12.4 min", "+1.3 min"),
            ("Mobile Access", "34%", "+5.2%")
        ]
        
        for label, value, change in access_metrics:
            st.metric(label, value, change)
        
        st.markdown("#### Top Accessed Documents")
        
        top_docs = [
            ("Standard_NDA_Template.docx", 87, "📄"),
            ("Employment_Agreement_2024.pdf", 72, "📄"),
            ("IP_License_Agreement.docx", 64, "📄"),
            ("Merger_Checklist.xlsx", 58, "📊"),
            ("Litigation_Timeline.pdf", 45, "📄")
        ]
        
        for doc, access_count, icon in top_docs:
            col_acc1, col_acc2 = st.columns([3, 1])
            with col_acc1:
                st.write(f"{icon} {doc}")
            with col_acc2:
                st.write(f"{access_count} views")

def show_ai_powered_search():
    st.subheader("🤖 AI-Powered Intelligent Search")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("#### Natural Language Query")
        
        # AI search interface
        ai_query = st.text_area("Ask a question in natural language:", 
                               placeholder="e.g., 'Show me all contracts with ABC Corp that expire in the next 6 months' or 'Find documents related to intellectual property disputes from last year'",
                               height=100)
        
        col_ai1, col_ai2 = st.columns(2)
        with col_ai1:
            search_scope = st.selectbox("Search Scope:", ["All Content", "Current Matter Only", "My Documents", "Recent Activity"])
        with col_ai2:
            ai_features = st.multiselect("AI Features:", ["Summarization", "Entity Extraction", "Sentiment Analysis", "Translation"])
        
        # AI search modes
        search_mode = st.radio("Search Mode:", ["Standard AI", "Deep Analysis", "Comparative Search", "Predictive Search"])
        
        if st.button("🤖 AI Search", type="primary"):
            st.session_state.ai_results = get_ai_search_results(ai_query)
        
        # Display notification
        if st.session_state.notification:
            st.success(st.session_state.notification)
            st.session_state.notification = None
        
        if st.session_state.ai_results:
            st.markdown("#### AI Search Results & Analysis")
            
            # AI interpretation
            with st.container():
                st.info(f"🤖 **AI Interpretation:** {st.session_state.ai_results['interpretation']}")
                
                # Query analysis
                st.markdown("**Query Analysis:**")
                col_query1, col_query2, col_query3 = st.columns(3)
                analysis = st.session_state.ai_results['analysis']
                with col_query1:
                    st.write(f"**Entities Found:** {analysis['entities']}")
                with col_query2:
                    st.write(f"**Intent:** {analysis['intent']}")
                with col_query3:
                    st.write(f"**Time Context:** {analysis['time_context']}")
            
            # AI-enhanced results
            for idx, result in enumerate(st.session_state.ai_results['results']):
                risk_colors = {"Low": "🟢", "Medium": "🟡", "High": "🔴"}
                
                with st.expander(f"🤖 {result['title']} (AI Confidence: {result['confidence']}%) {risk_colors[result['risk_level']]}"):
                    col_ai_res1, col_ai_res2 = st.columns(2)
                    
                    with col_ai_res1:
                        st.write(f"**AI Summary:** {result['summary']}")
                        st.write(f"**Key Entities:** {', '.join(result['entities'])}")
                        st.write(f"**Sentiment:** {result['sentiment']}")
                        st.write(f"**Risk Level:** {result['risk_level']}")
                    
                    with col_ai_res2:
                        st.write(f"**Expiry Date:** {result['expiry_date']}")
                        st.write(f"**AI Insights:** {result['ai_insights']}")
                        st.write(f"**Action Required:** {result['action_required']}")
                        st.progress(result['confidence'] / 100)
                    
                    # AI action buttons
                    col_ai_btn1, col_ai_btn2, col_ai_btn3, col_ai_btn4 = st.columns(4)
                    with col_ai_btn1:
                        if st.button("📝 Generate Summary", key=f"ai_summary_{idx}"):
                            st.session_state.notification = f"Generating AI summary for {result['title']}"
                            st.rerun()
                    with col_ai_btn2:
                        if st.button("🔍 Deep Analysis", key=f"ai_analysis_{idx}"):
                            st.session_state.notification = f"Running deep analysis on {result['title']}"
                            st.rerun()
                    with col_ai_btn3:
                        if st.button("⚡ Quick Actions", key=f"ai_actions_{idx}"):
                            st.session_state.notification = f"Showing quick actions for {result['title']}"
                            st.rerun()
                    with col_ai_btn4:
                        if st.button("📅 Set Reminder", key=f"ai_reminder_{idx}"):
                            st.session_state.notification = f"Reminder set for {result['title']}"
                            st.rerun()
    
    with col2:
        st.markdown("#### AI Assistant")
        
        st.markdown("##### Query Suggestions")
        suggestions = [
            "Find overdue contracts",
            "Show high-risk documents", 
            "Contracts expiring soon",
            "Documents needing review",
            "Recent amendments",
            "Similar agreements",
            "Compliance issues"
        ]
        
        for suggestion in suggestions:
            if st.button(f"💡 {suggestion}", key=f"suggest_{suggestion[:10]}"):
                st.info(f"Searching: {suggestion}")
        
        st.markdown("##### AI Capabilities")
        capabilities = [
            "🧠 Natural Language Understanding",
            "📊 Intelligent Summarization", 
            "🏷️ Automatic Entity Extraction",
            "💭 Sentiment Analysis",
            "🔗 Relationship Mapping",
            "⚠️ Risk Identification",
            "📈 Trend Analysis",
            "🎯 Predictive Insights"
        ]
        
        for capability in capabilities:
            st.write(capability)
        
        st.markdown("##### AI Search History")
        ai_history = [
            "Contract expiration analysis",
            "IP document classification", 
            "Risk assessment query",
            "Entity relationship mapping",
            "Compliance document search"
        ]
        
        for history in ai_history:
            if st.button(f"🔄 {history}", key=f"history_{history[:10]}"):
                st.info(f"Rerunning: {history}")

def get_ai_search_results(query):
    """Simulate AI-powered search with intelligent analysis"""
    query_lower = query.lower() if query else ""
    
    # Determine search context
    has_contract = any(word in query_lower for word in ['contract', 'agreement', 'nda'])
    has_abc_corp = 'abc' in query_lower or 'abc corp' in query_lower
    has_expiry = any(word in query_lower for word in ['expir', 'renew', 'deadline', 'months'])
    
    # Build interpretation
    interpretation = "I understand you're looking for "
    if has_contract:
        interpretation += "contract documents "
    else:
        interpretation += "documents "
    
    if has_abc_corp:
        interpretation += "related to ABC Corp "
    
    if has_expiry:
        interpretation += "with upcoming expiration dates. "
    
    interpretation += "Let me analyze the relevant documents and provide insights."
    
    # Query analysis
    entities = []
    if has_abc_corp:
        entities.append("ABC Corp")
    if has_contract:
        entities.append("contracts")
    if has_expiry:
        entities.append("expiration")
    
    intent = "Document review"
    if has_expiry:
        intent += ", deadline tracking"
    if has_contract:
        intent += ", contract management"
    
    time_context = "Next 6 months" if has_expiry else "Current"
    
    # Results based on query
    results = [
        {
            "title": "ABC Corp Service Agreement",
            "summary": "Multi-year service agreement covering IT support and maintenance. Key renewal clause on page 12.",
            "entities": ["ABC Corp", "IT Services", "Renewal Clause", "John Smith"],
            "sentiment": "Neutral",
            "expiry_date": "2024-12-15",
            "ai_insights": "Contract contains auto-renewal clause. Recommend review 90 days before expiry.",
            "confidence": 94,
            "risk_level": "Medium",
            "action_required": "Review required"
        },
        {
            "title": "ABC Corp NDA Extension",
            "summary": "Non-disclosure agreement extension with specific IP protection clauses.",
            "entities": ["ABC Corp", "NDA", "IP Protection", "Confidentiality"],
            "sentiment": "Positive",
            "expiry_date": "2025-01-30",
            "ai_insights": "Strong IP protection. No immediate action required.",
            "confidence": 87,
            "risk_level": "Low",
            "action_required": "Monitor"
        },
        {
            "title": "ABC Corp Master Services Agreement",
            "summary": "Comprehensive services agreement with multiple work orders and deliverables.",
            "entities": ["ABC Corp", "MSA", "Work Orders", "Deliverables"],
            "sentiment": "Neutral",
            "expiry_date": "2024-11-30",
            "ai_insights": "Complex agreement with multiple dependencies. Early renewal discussions recommended.",
            "confidence": 91,
            "risk_level": "High",
            "action_required": "Immediate attention"
        }
    ]
    
    # Filter results based on query relevance
    if not (has_contract or has_abc_corp or has_expiry):
        # Generic query, return all results
        pass
    elif has_abc_corp and has_expiry:
        # Keep all ABC Corp results with expiry focus
        pass
    elif has_abc_corp:
        # Keep ABC Corp results
        pass
    
    return {
        'interpretation': interpretation,
        'analysis': {
            'entities': ', '.join(entities) if entities else 'contract documents',
            'intent': intent,
            'time_context': time_context
        },
        'results': results
    }


def show_legal_research():
    st.subheader("📚 Legal Research & Case Law Search")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("#### Legal Database Search")
        
        # Research query
        legal_query = st.text_input("Legal Research Query:", placeholder="Enter case law, statutes, regulations, or legal concepts...")
        
        col_legal1, col_legal2, col_legal3 = st.columns(3)
        with col_legal1:
            jurisdiction = st.selectbox("Jurisdiction:", ["All", "Federal", "State", "International"])
        with col_legal2:
            content_type = st.selectbox("Content Type:", ["All", "Case Law", "Statutes", "Regulations", "Legal Forms"])
        with col_legal3:
            date_filter = st.selectbox("Date Range:", ["All Time", "Last 5 Years", "Last 10 Years", "Since 2000"])
        
        # Advanced legal research options
        with st.expander("🔧 Advanced Legal Research"):
            col_adv_legal1, col_adv_legal2 = st.columns(2)
            
            with col_adv_legal1:
                court_level = st.multiselect("Court Level:", ["Supreme Court", "Circuit Courts", "District Courts", "State Supreme", "State Appellate"])
                practice_area = st.multiselect("Practice Area:", ["IP Law", "Contract Law", "Employment Law", "Corporate Law", "Litigation"])
            
            with col_adv_legal2:
                shepardize = st.checkbox("Shepardize Results", value=True)
                headnotes = st.checkbox("Include Headnotes", value=True)
                secondary_sources = st.checkbox("Include Secondary Sources")
        
        if st.button("📚 Search Legal Database", type="primary"):
            st.markdown("#### Legal Research Results")
            
            legal_results = [
                {
                    "title": "Smith v. Technology Corp (2023)",
                    "court": "9th Circuit Court of Appeals",
                    "date": "2023-08-15",
                    "citation": "987 F.3d 456 (9th Cir. 2023)",
                    "relevance": 96,
                    "summary": "Case addressing intellectual property rights in software development contracts and work-for-hire provisions...",
                    "key_holdings": ["IP ownership in work-for-hire", "Contract interpretation standards"],
                    "shepard_status": "Good Law",
                    "times_cited": 47,
                    "practice_areas": ["IP Law", "Contract Law"]
                },
                {
                    "title": "Patent Protection Act § 201",
                    "source": "Federal Statute",
                    "date": "2022-12-01",
                    "citation": "35 U.S.C. § 201",
                    "relevance": 91,
                    "summary": "Federal statute governing patent ownership and licensing requirements in government-funded research...",
                    "key_provisions": ["Patent licensing", "Government rights", "Small business protections"],
                    "amendments": "Last amended 2022",
                    "effective_date": "2023-01-01",
                    "practice_areas": ["IP Law", "Government Contracts"]
                },
                {
                    "title": "Johnson Industries v. Innovation LLC (2022)",
                    "court": "Federal District Court",
                    "date": "2022-11-22", 
                    "citation": "2022 U.S. Dist. LEXIS 45678",
                    "relevance": 88,
                    "summary": "District court decision on trade secret misappropriation claims and reasonable measures requirement...",
                    "key_holdings": ["Trade secret definition", "Reasonable measures requirement"],
                    "shepard_status": "Good Law",
                    "times_cited": 23,
                    "practice_areas": ["IP Law", "Trade Secrets"]
                }
            ]
            
            for result in legal_results:
                status_colors = {"Good Law": "🟢", "Questioned": "🟡", "Bad Law": "🔴"}
                shepard_status = result.get('shepard_status', 'Unknown')
                
                with st.expander(f"⚖️ {result['title']} ({result['relevance']}% relevant) {status_colors.get(shepard_status, '⚪')}"):
                    col_legal_res1, col_legal_res2 = st.columns(2)
                    
                    with col_legal_res1:
                        st.write(f"**Court/Source:** {result.get('court', result.get('source', 'N/A'))}")
                        st.write(f"**Date:** {result['date']}")
                        st.write(f"**Citation:** {result['citation']}")
                        st.write(f"**Summary:** {result['summary']}")
                        
                        if 'practice_areas' in result:
                            areas = ", ".join(result['practice_areas'])
                            st.write(f"**Practice Areas:** {areas}")
                    
                    with col_legal_res2:
                        st.progress(result['relevance'] / 100)
                        st.write(f"Relevance: {result['relevance']}%")
                        
                        if 'shepard_status' in result:
                            st.write(f"**Shepard's Status:** {result['shepard_status']}")
                        if 'times_cited' in result:
                            st.write(f"**Times Cited:** {result['times_cited']}")
                        
                        key_items = result.get('key_holdings', result.get('key_provisions', []))
                        if key_items:
                            st.write("**Key Points:**")
                            for point in key_items:
                                st.write(f"• {point}")
                    
                    # Legal research actions
                    col_legal_btn1, col_legal_btn2, col_legal_btn3, col_legal_btn4 = st.columns(4)
                    with col_legal_btn1:
                        st.button("📖 Full Text", key=f"legal_full_{result['title'][:10]}")
                    with col_legal_btn2:
                        st.button("📝 Cite", key=f"legal_cite_{result['title'][:10]}")
                    with col_legal_btn3:
                        st.button("🔗 Shepardize", key=f"legal_shep_{result['title'][:10]}")
                    with col_legal_btn4:
                        st.button("📎 Save", key=f"legal_save_{result['title'][:10]}")
        
        # Legal research workspace
        st.markdown("#### Research Workspace")
        
        with st.expander("📝 Research Notes & Citations"):
            col_workspace1, col_workspace2 = st.columns(2)
            
            with col_workspace1:
                research_notes = st.text_area("Research Notes:", height=150, 
                    placeholder="Take notes on your legal research...")
                
                citation_format = st.selectbox("Citation Format:", 
                    ["Bluebook", "ALWD", "APA", "MLA", "Chicago"])
            
            with col_workspace2:
                st.markdown("**Saved Citations:**")
                saved_citations = [
                    "Smith v. Technology Corp, 987 F.3d 456 (9th Cir. 2023)",
                    "35 U.S.C. § 201 (2022)",
                    "Johnson Industries v. Innovation LLC, 2022 U.S. Dist. LEXIS 45678"
                ]
                
                for citation in saved_citations:
                    col_cite1, col_cite2 = st.columns([4, 1])
                    with col_cite1:
                        st.write(f"• {citation}")
                    with col_cite2:
                        st.button("📋", key=f"copy_cite_{citation[:15]}")
            
            col_work_btn1, col_work_btn2, col_work_btn3 = st.columns(3)
            with col_work_btn1:
                st.button("💾 Save Research")
            with col_work_btn2:
                st.button("📄 Export Report")
            with col_work_btn3:
                st.button("📧 Share Research")
    
    with col2:
        st.markdown("#### Research Tools")
        
        research_tools = [
            "📚 Case Law Database",
            "📜 Statute Finder", 
            "📋 Regulation Search",
            "📄 Legal Forms Library",
            "🔍 Citation Validator",
            "📊 Court Analytics",
            "🏛️ Docket Search"
        ]
        
        for tool in research_tools:
            if st.button(tool, key=f"tool_{tool[:10]}"):
                st.info(f"Opening {tool}...")
        
        st.markdown("#### Recent Research")
        recent_research = [
            "Patent law updates 2024",
            "Contract interpretation",
            "Employment law changes", 
            "IP licensing agreements",
            "Corporate governance",
            "Trade secret protection"
        ]
        
        for research in recent_research:
            st.write(f"• {research}")
        
        st.markdown("#### Citation Manager")
        citation_stats = [
            ("Total Citations", "127"),
            ("This Month", "23"),
            ("Validated", "98.4%"),
            ("Recent Updates", "5")
        ]
        
        for stat, value in citation_stats:
            st.metric(stat, value)
        
        if st.button("📚 Manage Citations"):
            st.info("Opening citation manager...")
        if st.button("📝 Generate Bibliography"):
            st.info("Generating bibliography...")
        if st.button("🔍 Check Citations"):
            st.info("Validating citations...")

def show_search_management():
    st.subheader("🗂️ Search Management & Collections")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Search collections
        st.markdown("#### Search Collections")
        
        collections = [
            {
                "name": "ABC Corp Merger Documents", 
                "items": 47,
                "created": "2024-09-15",
                "shared": True,
                "tags": ["merger", "contracts", "due diligence"]
            },
            {
                "name": "Patent Defense Research",
                "items": 23, 
                "created": "2024-09-12",
                "shared": False,
                "tags": ["patent", "defense", "prior art"]
            },
            {
                "name": "Employment Law Updates",
                "items": 15,
                "created": "2024-09-10", 
                "shared": True,
                "tags": ["employment", "compliance", "updates"]
            }
        ]
        
        for collection in collections:
            with st.expander(f"📁 {collection['name']} ({collection['items']} items)"):
                col_coll1, col_coll2 = st.columns(2)
                
                with col_coll1:
                    st.write(f"**Items:** {collection['items']}")
                    st.write(f"**Created:** {collection['created']}")
                    st.write(f"**Shared:** {'Yes' if collection['shared'] else 'No'}")
                
                with col_coll2:
                    tag_display = " ".join([f"`{tag}`" for tag in collection['tags']])
                    st.markdown(f"**Tags:** {tag_display}")
                
                col_coll_btn1, col_coll_btn2, col_coll_btn3, col_coll_btn4 = st.columns(4)
                with col_coll_btn1:
                    st.button("👁️ View", key=f"view_coll_{collection['name'][:10]}")
                with col_coll_btn2:
                    st.button("✏️ Edit", key=f"edit_coll_{collection['name'][:10]}")
                with col_coll_btn3:
                    st.button("📤 Export", key=f"export_coll_{collection['name'][:10]}")
                with col_coll_btn4:
                    st.button("🗑️ Delete", key=f"delete_coll_{collection['name'][:10]}")
        
        # Saved searches
        st.markdown("#### Saved Search Queries")
        
        saved_queries = [
            {
                "name": "Expiring Contracts Q4 2024",
                "query": "contract expiration:2024-10-01 TO 2024-12-31",
                "results": 12,
                "last_run": "2024-09-20",
                "alert": True
            },
            {
                "name": "Patent Litigation Cases",
                "query": "patent AND (litigation OR infringement)",
                "results": 45,
                "last_run": "2024-09-18", 
                "alert": False
            },
            {
                "name": "Confidential ABC Corp Documents",
                "query": "client:'ABC Corp' AND security:confidential",
                "results": 78,
                "last_run": "2024-09-19",
                "alert": False
            }
        ]
        
        for query in saved_queries:
            alert_icon = "🔔" if query['alert'] else "🔕"
            
            with st.expander(f"🔍 {query['name']} ({query['results']} results) {alert_icon}"):
                col_query1, col_query2 = st.columns(2)
                
                with col_query1:
                    st.code(query['query'])
                    st.write(f"**Last Run:** {query['last_run']}")
                
                with col_query2:
                    st.write(f"**Results:** {query['results']}")
                    st.write(f"**Alert:** {'Enabled' if query['alert'] else 'Disabled'}")
                
                col_query_btn1, col_query_btn2, col_query_btn3, col_query_btn4 = st.columns(4)
                with col_query_btn1:
                    st.button("▶️ Run", key=f"run_query_{query['name'][:10]}")
                with col_query_btn2:
                    st.button("✏️ Edit", key=f"edit_query_{query['name'][:10]}")
                with col_query_btn3:
                    st.button(f"{'🔔' if not query['alert'] else '🔕'} Alert", key=f"alert_query_{query['name'][:10]}")
                with col_query_btn4:
                    st.button("🗑️ Delete", key=f"delete_query_{query['name'][:10]}")
        
        # Search alerts and notifications
        st.markdown("#### Search Alerts & Notifications")
        
        with st.form("create_alert"):
            alert_name = st.text_input("Alert Name:", placeholder="e.g., New ABC Corp Documents")
            alert_query = st.text_input("Search Query:", placeholder="Enter search terms or query...")
            
            col_alert1, col_alert2 = st.columns(2)
            with col_alert1:
                alert_frequency = st.selectbox("Check Frequency:", ["Real-time", "Hourly", "Daily", "Weekly"])
            with col_alert2:
                notification_method = st.multiselect("Notify Via:", ["Email", "In-App", "SMS", "Slack"])
            
            if st.form_submit_button("🔔 Create Alert"):
                st.success(f"Alert '{alert_name}' created successfully!")
    
    with col2:
        st.markdown("#### Search Statistics")
        
        search_stats = [
            ("Total Searches", "1,247"),
            ("Saved Collections", "12"),
            ("Active Alerts", "5"),
            ("Shared Searches", "8")
        ]
        
        for stat, value in search_stats:
            st.metric(stat, value)
        
        st.markdown("#### Quick Actions")
        
        quick_actions = [
            "📁 New Collection",
            "🔍 Save Current Search", 
            "🔔 Create Alert",
            "📤 Export All",
            "⚙️ Search Settings",
            "📊 Usage Analytics"
        ]
        
        for action in quick_actions:
            if st.button(action, key=f"quick_{action[:10]}"):
                st.info(f"Opening {action}...")
        
        st.markdown("#### Search Insights")
        
        insights = [
            {"icon": "📈", "text": "Search volume up 15% this month"},
            {"icon": "🎯", "text": "AI search accuracy: 94.2%"},
            {"icon": "⚡", "text": "Avg search time: 0.8 seconds"},
            {"icon": "📱", "text": "Mobile searches: 34%"}
        ]
        
        for insight in insights:
            col_insight1, col_insight2 = st.columns([1, 4])
            with col_insight1:
                st.write(insight["icon"])
            with col_insight2:
                st.write(insight["text"])

# Main execution
if __name__ == "__main__":
    show()
