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

# ========== RECURSION PROTECTION ==========
# Prevent infinite reloads
if 'reload_count' not in st.session_state:
    st.session_state.reload_count = 0

st.session_state.reload_count += 1

# If reloaded more than 5 times, stop
if st.session_state.reload_count > 5:
    st.error("⚠️ Too many reloads detected. Resetting application...")
    
    if st.button("🔄 Reset Application"):
        # Clear everything
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
    
    st.stop()  # Stop execution

# Reset counter after successful load
if st.session_state.reload_count == 2:
    st.session_state.reload_count = 0

# Load CSS (keep your existing CSS)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
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
    st.error("Session manager not found.")
    st.stop()

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

# Page modules
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
    "Mobile App": safe_import_page("mobile_app", "pages.mobile_app"),
    "Business Intelligence": safe_import_page("business_intel", "pages.business_intelligence"),
    "Billing Management": safe_import_page("billing_management", "pages.billing_management"),
}

def main():
    """Main application function"""
    
    # Check URL parameters ONCE at start
    query_params = st.query_params
    
    # Handle special pages that don't need login
    if 'verify' in query_params:
        handle_email_verification_static()
        return
    
    if 'reset' in query_params:
        handle_password_reset_static()
        return
    
    if query_params.get('page') == 'forgot_password':
        try:
            from pages.forgot_password import show
            show()
        except:
            st.error("Forgot password page not found")
        return
    
    # Initialize session state ONCE
    if 'initialized' not in st.session_state:
        initialize_session_state()
        load_sample_data()
        st.session_state.initialized = True
    
    # Initialize authentication service
    auth_service = AuthService()
    
    # Check authentication
    if not st.session_state.get('logged_in', False):
        auth_service.show_login()
        return
    
    # Main app styling
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
    
    # Render sidebar
    auth_service.render_sidebar()
    
    # Get current page
    current_page = st.session_state.get('current_page', 'Executive Dashboard')
    
    # Route to page
    if current_page in page_modules:
        try:
            page_modules[current_page]()
        except Exception as e:
            st.error(f"Error loading {current_page}: {str(e)}")
            
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

if __name__ == "__main__":
    try:
        main()
    except RecursionError:
        st.error("⚠️ FATAL: Recursion detected")
        st.write("The app is stuck in a reload loop.")
        
        if st.button("🔄 Force Reset"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    except Exception as e:
        st.error(f"Application Error: {str(e)}")
        
        with st.expander("🔧 Debug Info"):
            import traceback
            st.code(traceback.format_exc())
        
        if st.button("🔄 Reload"):
            st.rerun()
