import streamlit as st
import sys
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configure Streamlit
st.set_page_config(
    page_title="LegalDoc Pro - Enterprise Legal Management",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Hide toolbar with refresh button */
    [data-testid="stToolbar"] {
        display: none !important;
    }
    
    [data-testid="stDecoration"] {
        display: none !important;
    }
    
    /* Hide top padding */
    .block-container {
        padding-top: 1rem !important;
    }

    
    .main {
        font-family: 'Inter', sans-serif;
        padding: 0 !important;
    }
    
    .block-container {
        padding: 2rem 3rem !important;
        max-width: 100% !important;
    }
</style>
""", unsafe_allow_html=True)

# Import services with error handling
try:
    from services.email_service import AuthTokenManager, EmailService
    from services.subscription_config import SUBSCRIPTION_PLANS
except ImportError as e:
    st.error(f"Import error: {e}")
    st.stop()

try:
    from services.subscription_manager import EnhancedAuthService as AuthService
except ImportError:
    st.error("Authentication service not found.")
    st.stop()

try:
    from session_manager import initialize_session_state, load_sample_data
except ImportError:
    # If session_manager doesn't exist, create minimal initialization
    def initialize_session_state():
        if 'logged_in' not in st.session_state:
            st.session_state.logged_in = False
        if 'user_data' not in st.session_state:
            st.session_state.user_data = None
        if 'current_page' not in st.session_state:
            st.session_state.current_page = 'Executive Dashboard'
        if 'documents' not in st.session_state:
            st.session_state.documents = []
        if 'matters' not in st.session_state:
            st.session_state.matters = []
    
    def load_sample_data():
        pass

# Import pages with fallbacks
def safe_import_page(page_name, module_path):
    """Safely import a page module with fallback"""
    try:
        module = __import__(module_path, fromlist=[page_name])
        return getattr(module, 'show', lambda: st.error(f"Page {page_name} show function not found"))
    except ImportError:
        return lambda: st.info(f"{page_name} page is under development")
    except Exception as e:
        return lambda: st.error(f"Error loading {page_name}: {str(e)}")

# Page modules - ONLY pages that should be accessible after login
page_modules = {
    "Executive Dashboard": safe_import_page("dashboard", "pages.dashboard"),
    "Document Management": safe_import_page("documents", "pages.documents"), 
    "Matter Management": safe_import_page("matters", "pages.matters"),
    "Case Comparison": safe_import_page("case_comparison", "pages.case_comparison"),
    "Time & Billing": safe_import_page("time_billing", "pages.time_billing"),
    "AI Insights": safe_import_page("ai_insights", "pages.ai_insights"),
    "Calendar & Tasks": safe_import_page("calendar_tasks", "pages.calendar_tasks"),
    "Advanced Search": safe_import_page("advanced_search", "pages.advanced_search"),
    "Integrations": safe_import_page("integrations", "pages.integrations"),
    "Business Intelligence": safe_import_page("business_intel", "pages.business_intelligence"),
    "Billing Management": safe_import_page("billing_management", "pages.billing_management"),
}

def main():
    """Main application function"""
    
    # Initialize session state ONCE at the very beginning
    if 'initialized' not in st.session_state:
        initialize_session_state()
        load_sample_data()
        st.session_state.initialized = True
    
    # Initialize authentication service
    auth_service = AuthService()
    
    # Check URL parameters for special pages
    query_params = st.query_params
    
    # Handle email verification (no login required)
    if 'verify' in query_params:
        handle_email_verification_static()
        return
    
    # Handle password reset (no login required)
    if 'reset' in query_params:
        handle_password_reset_static()
        return
    
    # ========== AUTHENTICATION GATE ==========
    # If user is NOT logged in, show ONLY login page (no sidebar, no other pages)
    if not st.session_state.get('logged_in', False):
        # Apply professional clean login page styling
        st.markdown("""
        <style>
        /* Professional dark blue gradient background */
        .stApp {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 25%, #334155 50%, #1e3a8a 75%, #1e40af 100%);
        }
        
        /* Hide sidebar */
        [data-testid="stSidebar"] {
            display: none;
        }
        
        /* All white text */
        label, p, span, div, .stMarkdown, h1, h2, h3 {
            color: white !important;
        }
        
        /* Professional input fields - clean white/gray */
        input {
            background: rgba(255, 255, 255, 0.95) !important;
            border: 2px solid #e2e8f0 !important;
            border-radius: 10px !important;
            padding: 0.875rem 1rem !important;
            color: #1e293b !important;
            font-size: 1rem !important;
            transition: all 0.2s ease !important;
        }
        
        input::placeholder {
            color: #94a3b8 !important;
        }
        
        input:focus {
            background: white !important;
            border-color: #3b82f6 !important;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
            outline: none !important;
        }
        
        /* Professional blue button */
        .stButton button {
            background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 0.875rem 2rem !important;
            font-weight: 600 !important;
            width: 100% !important;
            font-size: 1rem !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 14px rgba(59, 130, 246, 0.4) !important;
        }
        
        .stButton button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 20px rgba(59, 130, 246, 0.5) !important;
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
        }
        
        /* Secondary button (outlined) */
        .stButton button[kind="secondary"] {
            background: transparent !important;
            border: 2px solid rgba(255, 255, 255, 0.3) !important;
            color: white !important;
            box-shadow: none !important;
        }
        
        .stButton button[kind="secondary"]:hover {
            background: rgba(255, 255, 255, 0.1) !important;
            border-color: rgba(255, 255, 255, 0.5) !important;
        }
        
        /* Clean selectbox */
        [data-baseweb="select"] {
            background: rgba(255, 255, 255, 0.95) !important;
            border: 2px solid #e2e8f0 !important;
            border-radius: 10px !important;
        }
        
        [data-baseweb="select"] > div {
            color: #1e293b !important;
        }
        
        /* Checkbox */
        [data-testid="stCheckbox"] {
            color: white !important;
        }
        
        /* Info/Success/Error messages */
        .stSuccess {
            background: rgba(16, 185, 129, 0.15) !important;
            border: 1px solid rgba(16, 185, 129, 0.3) !important;
            border-radius: 10px !important;
            color: white !important;
        }
        
        .stError {
            background: rgba(239, 68, 68, 0.15) !important;
            border: 1px solid rgba(239, 68, 68, 0.3) !important;
            border-radius: 10px !important;
            color: white !important;
        }
        
        .stInfo {
            background: rgba(59, 130, 246, 0.15) !important;
            border: 1px solid rgba(59, 130, 246, 0.3) !important;
            border-radius: 10px !important;
            color: white !important;
        }
        
        /* Expander */
        [data-testid="stExpander"] {
            background: rgba(255, 255, 255, 0.08) !important;
            border: 1px solid rgba(255, 255, 255, 0.15) !important;
            border-radius: 10px !important;
        }
        
        [data-testid="stExpander"] summary {
            color: white !important;
        }
        
        /* Forms - glass effect cards */
        [data-testid="stForm"] {
            background: rgba(30, 41, 59, 0.7) !important;
            backdrop-filter: blur(20px) !important;
            -webkit-backdrop-filter: blur(20px) !important;
            padding: 2.5rem 2rem !important;
            border-radius: 20px !important;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3) !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
        }
        
        /* Form labels and text should be white */
        [data-testid="stForm"] label,
        [data-testid="stForm"] p,
        [data-testid="stForm"] span,
        [data-testid="stForm"] div {
            color: white !important;
        }
        
        /* Form headings white */
        [data-testid="stForm"] h1,
        [data-testid="stForm"] h2,
        [data-testid="stForm"] h3,
        [data-testid="stForm"] h4 {
            color: white !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Show the login page
        auth_service.show_login()
        
        # ADD FORGOT PASSWORD SECTION HERE - This goes AFTER show_login()
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Center the forgot password button
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            # Use expander - automatically scrolls when opened
            with st.expander("🔑 Forgot Password? Click here to reset"):
                st.markdown("### 🔐 Reset Your Password")
                st.write("Enter your email address and we'll send you a reset link.")
                
                with st.form("main_forgot_password_form", clear_on_submit=True):
                    reset_email = st.text_input(
                        "Email Address", 
                        placeholder="your@email.com",
                        key="reset_email_input"
                    )
                    
                    col_submit, col_cancel = st.columns(2)
                    
                    with col_submit:
                        submit_reset = st.form_submit_button(
                            "📧 Send Reset Link", 
                            use_container_width=True, 
                            type="primary"
                        )
                    
                    with col_cancel:
                        cancel_reset = st.form_submit_button(
                            "✖️ Cancel", 
                            use_container_width=True
                        )
                    
                    if cancel_reset:
                        st.rerun()
                    
                    if submit_reset:
                        if not reset_email or '@' not in reset_email:
                            st.error("❌ Please enter a valid email address")
                        else:
                            from services.email_service import EmailService, AuthTokenManager
                            try:
                                users = st.session_state.get('users', {})
                                if reset_email in users:
                                    reset_token = AuthTokenManager.create_reset_token(reset_email)
                                    email_service = EmailService()
                                    email_sent = email_service.send_password_reset_email(reset_email, reset_token)
                                    if email_sent:
                                        st.success(f"✅ **Password reset link sent!** Check your email at **{reset_email}**")
                                        st.balloons()
                                    else:
                                        st.warning("⚠️ Unable to send email. Please try again later.")
                                else:
                                    st.success("✅ If an account exists, you'll receive a reset email.")
                            except Exception as e:
                                st.error(f"❌ Error: {str(e)}")
                                
                                # Show debug info in expander
                                with st.expander("🔧 Debug Information"):
                                    st.code(str(e))
        
        return  # Stop here - don't render anything else
    
    # ========== USER IS LOGGED IN - SHOW FULL APP ==========
    
    # Apply logged-in app styling
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #1a0b2e 0%, #2d1b4e 15%, #1e3a8a 35%, #0f172a 50%, #1e3a8a 65%, #16537e 85%, #0891b2 100%) !important;
    }
    .main .block-container {
        background: #1e293b !important;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3) !important;
        border: 1px solid #334155 !important;
    }
    .main .block-container > div:not(.stPlotlyChart) * {
        color: #e2e8f0 !important;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #f1f5f9 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Render sidebar (only shown when logged in)
    auth_service.render_sidebar()
    
    # Get current page
    current_page = st.session_state.get('current_page', 'Executive Dashboard')
    
    # Route to page
    if current_page in page_modules:
        try:
            page_modules[current_page]()
        except Exception as e:
            st.error(f"Error loading {current_page}: {str(e)}")
            
            with st.expander("🔧 Error Details"):
                import traceback
                st.code(traceback.format_exc())
            
            if st.button("🏠 Return to Dashboard"):
                st.session_state['current_page'] = 'Executive Dashboard'
                st.rerun()
    else:
        st.error(f"Page '{current_page}' not found")
        
        if st.button("🏠 Go to Dashboard"):
            st.session_state['current_page'] = 'Executive Dashboard'
            st.rerun()

def handle_email_verification_static():
    """Handle email verification - STATIC VERSION (no rerun)"""
    query_params = st.query_params
    token = query_params.get('verify')
    
    st.markdown("""
    <div style="text-align: center; padding: 3rem;">
        <h1>📧 Email Verification</h1>
    </div>
    """, unsafe_allow_html=True)
    
    if not token:
        st.error("No verification token provided")
        return
    
    try:
        email, error = AuthTokenManager.verify_token(token, 'verification')
        
        if error:
            st.error(f"❌ Verification failed: {error}")
            
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                if st.button("🏠 Go to Login", use_container_width=True):
                    st.query_params.clear()
                    st.rerun()
            return
        
        # Mark email as verified
        if 'users' in st.session_state and email in st.session_state.users:
            st.session_state.users[email]['data']['email_verified'] = True
            
            # Remove token
            if 'verification_tokens' in st.session_state:
                st.session_state.verification_tokens.pop(token, None)
            
            st.success(f"✅ Email verified successfully!")
            st.balloons()
            
            # Auto-login
            user_data = st.session_state.users[email]['data']
            st.session_state.logged_in = True
            st.session_state.user_data = user_data
            st.session_state.current_page = 'Executive Dashboard'
            
            st.info("Redirecting to dashboard...")
            
            # Clear query params and redirect
            st.query_params.clear()
            
            import time
            time.sleep(2)
            
            # Only rerun once
            if 'verification_done' not in st.session_state:
                st.session_state.verification_done = True
                st.rerun()
        else:
            st.error("❌ User not found")
    
    except Exception as e:
        st.error(f"Verification error: {str(e)}")

def handle_password_reset_static():
    """Handle password reset - STATIC VERSION"""
    query_params = st.query_params
    token = query_params.get('reset')
    
    st.markdown("""
    <div style="text-align: center; padding: 2rem;">
        <h1>🔐 Reset Your Password</h1>
    </div>
    """, unsafe_allow_html=True)
    
    if not token:
        st.error("No reset token provided")
        return
    
    try:
        email, error = AuthTokenManager.verify_token(token, 'reset')
        
        if error:
            st.error(f"❌ Reset link invalid: {error}")
            
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                if st.button("🏠 Go to Login", use_container_width=True):
                    st.query_params.clear()
                    st.rerun()
            return
        
        # Show password reset form
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            with st.form("reset_password_form"):
                st.write(f"**Email:** {email}")
                
                new_password = st.text_input("New Password", type="password", placeholder="Minimum 8 characters")
                confirm_password = st.text_input("Confirm Password", type="password")
                
                submitted = st.form_submit_button("Reset Password", use_container_width=True, type="primary")
                
                if submitted:
                    if len(new_password) < 8:
                        st.error("Password must be at least 8 characters")
                    elif new_password != confirm_password:
                        st.error("Passwords do not match")
                    else:
                        # Update password
                        hashed_password = AuthTokenManager.hash_password(new_password)
                        
                        if 'users' in st.session_state and email in st.session_state.users:
                            st.session_state.users[email]['password'] = hashed_password
                            
                            # Remove token
                            if 'reset_tokens' in st.session_state:
                                st.session_state.reset_tokens.pop(token, None)
                            
                            st.success("✅ Password reset successfully!")
                            st.info("You can now log in with your new password")
                            
                            # Clear query params
                            st.query_params.clear()
                            
                            import time
                            time.sleep(2)
                            
                            # Only rerun once
                            if 'reset_done' not in st.session_state:
                                st.session_state.reset_done = True
                                st.rerun()
                        else:
                            st.error("User not found")
    
    except Exception as e:
        st.error(f"Reset error: {str(e)}")

# Run the app
try:
    main()
except Exception as e:
    st.error(f"Application Error: {str(e)}")
    
    with st.expander("🔧 Debug Info"):
        import traceback
        st.code(traceback.format_exc())
    
    if st.button("🔄 Reload"):
        st.rerun()
