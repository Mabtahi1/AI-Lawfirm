import streamlit as st
from services.email_service import EmailService, AuthTokenManager

def show():
    """Display forgot password page"""
    
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
        <h1>🤖 AI Legal Insights</h1>
        <p>AI-powered document analysis, contract review, and legal intelligence</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("forgot_password_form"):
            email = st.text_input("Email Address", placeholder="your@email.com")
            
            submitted = st.form_submit_button("Send Reset Link", use_container_width=True, type="primary")
            
            if submitted:
                if not email or '@' not in email:
                    st.error("Please enter a valid email address")
                else:
                    # Check if user exists
                    users = st.session_state.get('users', {})
                    
                    if email in users:
                        # Generate reset token
                        reset_token = AuthTokenManager.create_reset_token(email)
                        
                        # Send reset email
                        email_service = EmailService()
                        email_sent = email_service.send_password_reset_email(email, reset_token)
                        
                        if email_sent:
                            st.success(f"""
                            ✅ Password reset link sent!
                            
                            If an account exists for **{email}**, you'll receive a password reset email shortly.
                            
                            The link expires in 1 hour.
                            """)
                        else:
                            st.warning("Unable to send email. Please try again later.")
                    else:
                        # Don't reveal if email exists (security)
                        st.success(f"""
                        ✅ Password reset link sent!
                        
                        If an account exists for **{email}**, you'll receive a password reset email shortly.
                        
                        The link expires in 1 hour.
                        """)
        
        st.markdown("---")
        
        if st.button("← Back to Login"):
            st.query_params.clear()
            st.rerun()

if __name__ == "__main__":
    show()
