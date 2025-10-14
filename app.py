import streamlit as st
import sys
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import auth token manager for password reset and verification
from services.email_service import AuthTokenManager, EmailService
from services.subscription_config import SUBSCRIPTION_PLANS

# Temporarily disable scheduler to avoid issues
# from services.email_scheduler import EmailScheduler

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
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* ... rest of your CSS stays the same ... */
</style>
""", unsafe_allow_html=True)

# Import services with error handling
try:
    from services.subscription_manager import EnhancedAuthService as AuthService
except ImportError:
    st.error("Authentication service not found. Please check the services/auth.py file.")
    st.stop()

try:
    from session_manager import initialize_session_state, load_sample_data
except ImportError:
    st.error("Session manager not found. Please check the session_manager.py file.")
    st.stop()

# Import pages with fallbacks
def safe_import_page(page_name, module_path):
    """Safely import a page module with fallback"""
    try:
        module = __import__(module_path, fromlist=[page_name])
        return getattr(module, 'show', lambda: st.error(f"Page {page_name} show function not found"))
    except ImportError:
        return lambda: show_placeholder_page(page_name)
    except Exception as e:
        return lambda: st.error(f"Error loading {page_name}: {str(e)}")

def show_placeholder_page(page_name):
    """Show a placeholder page when the actual page is not available"""
    st.markdown(f"""
    <div class="main-header">
        <h1>{page_name}</h1>
        <p>This page is under development</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.info(f"The {page_name} page is being developed. Please check back later.")
    
    if page_name == "Executive Dashboard":
        show_basic_dashboard()

def show_basic_dashboard():
    """Basic dashboard fallback"""
    st.subheader("📊 Basic Dashboard")
    
    # Basic metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Active Matters", len(st.session_state.get('matters', [])))
    with col2:
        st.metric("Total Documents", len(st.session_state.get('documents', [])))
    with col3:
        st.metric("Active Clients", len(st.session_state.get('clients', [])))
    with col4:
        st.metric("Pending Tasks", len(st.session_state.get('tasks', [])))
    
    # Recent activity
    st.subheader("Recent Activity")
    recent_items = [
        "Document uploaded: Merger Agreement v2.1",
        "Matter created: Johnson Custody Case",
        "Invoice generated: INV-2024-001",
        "Client portal access granted",
        "Calendar event scheduled"
    ]
    
    for item in recent_items:
        st.write(f"• {item}")

# Try to import pages, with fallbacks
page_modules = {
    "Signup": safe_import_page("signup", "pages.signup"),
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
    "Client Portal Management": safe_import_page("client_portal", "pages.client_portal"),
    "System Settings": safe_import_page("settings", "pages.system_settings"),
    "Client Dashboard": safe_import_page("client_dashboard", "pages.client_dashboard"),
    "My Documents": safe_import_page("my_documents", "pages.my_documents"),
    "Billing Management": safe_import_page("billing_management", "pages.billing_management"),
    "Messages": safe_import_page("messages", "pages.messages"),
    "Forgot Password": safe_import_page("forgot_password", "pages.forgot_password"),
}

# ========== KEEP ONLY ONE OF EACH FUNCTION ==========

def handle_email_verification():
    """Handle email verification from URL"""
    query_params = st.query_params
    
    if 'verify' in query_params:
        token = query_params['verify']
        
        email, error = AuthTokenManager.verify_token(token, 'verification')
        
        if error:
            st.error(f"❌ Verification failed: {error}")
            
            if st.button("🏠 Go to Login"):
                st.query_params.clear()
                st.rerun()
            return False
        
        # Mark email as verified
        if 'users' in st.session_state and email in st.session_state.users:
            st.session_state.users[email]['data']['email_verified'] = True
            
            # Send welcome email
            user_data = st.session_state.users[email]['data']
            org_code = user_data['organization_code']
            subscription = st.session_state.subscriptions.get(org_code, {})
            plan_name = SUBSCRIPTION_PLANS[subscription.get('plan', 'basic')]['name']
            
            email_service = EmailService()
            email_service.send_welcome_email(email, user_data['first_name'], plan_name)
            
            # Remove token
            if 'verification_tokens' in st.session_state:
                st.session_state.verification_tokens.pop(token, None)
            
            st.success(f"✅ Email verified successfully! Welcome to LegalDoc Pro, {user_data['first_name']}!")
            st.balloons()
            
            # Auto-login
            st.session_state.logged_in = True
            st.session_state.user_data = user_data
            st.session_state.current_page = 'Executive Dashboard'
            
            # Clear query params
            st.query_params.clear()
            
            import time
            time.sleep(2)
            st.rerun()
            
            return True
        else:
            st.error("❌ User not found")
            return False
    
    return None

def handle_password_reset():
    """Handle password reset from URL"""
    query_params = st.query_params
    
    if 'reset' in query_params:
        token = query_params['reset']
        
        email, error = AuthTokenManager.verify_token(token, 'reset')
        
        if error:
            st.error(f"❌ Reset link invalid: {error}")
            st.write("The link may have expired or been used already.")
            
            if st.button("🔐 Request New Reset Link"):
                st.query_params.clear()
                st.query_params.update({"page": "forgot_password"})
                st.rerun()
            
            if st.button("🏠 Go to Login"):
                st.query_params.clear()
                st.rerun()
            return False
        
        # Show password reset form
        st.markdown("""
        <div class="main-header">
            <h1>🔐 Reset Your Password</h1>
            <p>Enter your new password below</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            with st.form("reset_password_form"):
                st.write(f"**Email:** {email}")
                
                new_password = st.text_input("New Password", type="password", placeholder="Minimum 8 characters")
                
                # Password strength indicator
                if new_password:
                    strength = calculate_password_strength(new_password)
                    strength_colors = {
                        'weak': '#dc3545',
                        'medium': '#ffc107',
                        'strong': '#28a745'
                    }
                    st.markdown(f"""
                    <div style="
                        background: {strength_colors[strength]};
                        color: white;
                        padding: 0.5rem;
                        border-radius: 5px;
                        text-align: center;
                        margin: 0.5rem 0;
                    ">
                        Password Strength: {strength.upper()}
                    </div>
                    """, unsafe_allow_html=True)
                
                confirm_password = st.text_input("Confirm New Password", type="password")
                
                st.markdown("**Password Requirements:**")
                st.write("• At least 8 characters")
                st.write("• Mix of uppercase and lowercase letters")
                st.write("• At least one number")
                
                submitted = st.form_submit_button("Reset Password", use_container_width=True, type="primary")
                
                if submitted:
                    errors = []
                    
                    if len(new_password) < 8:
                        errors.append("Password must be at least 8 characters")
                    
                    if new_password != confirm_password:
                        errors.append("Passwords do not match")
                    
                    if errors:
                        for error in errors:
                            st.error(error)
                    else:
                        # Update password
                        hashed_password = AuthTokenManager.hash_password(new_password)
                        
                        if 'users' in st.session_state and email in st.session_state.users:
                            st.session_state.users[email]['password'] = hashed_password
                            
                            # Remove token
                            if 'reset_tokens' in st.session_state:
                                st.session_state.reset_tokens.pop(token, None)
                            
                            st.success("✅ Password reset successfully! You can now log in with your new password.")
                            st.balloons()
                            
                            # Clear query params
                            st.query_params.clear()
                            
                            import time
                            time.sleep(2)
                            st.rerun()
                        else:
                            st.error("User not found")
        
        return True
    
    return None

def calculate_password_strength(password):
    """Calculate password strength"""
    score = 0
    
    if len(password) >= 8:
        score += 1
    if len(password) >= 12:
        score += 1
    if any(c.isupper() for c in password):
        score += 1
    if any(c.islower() for c in password):
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    if any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password):
        score += 1
    
    if score <= 2:
        return 'weak'
    elif score <= 4:
        return 'medium'
    else:
        return 'strong'

def show_email_verification_warning():
    """Show warning when email is not verified"""
    user_data = st.session_state.get('user_data', {})
    email = user_data.get('email')
    
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #ffc107 0%, #ff9800 100%);
        color: white;
        padding: 3rem;
        border-radius: 20px;
        text-align: center;
        margin: 2rem;
    ">
        <h1>📧 Verify Your Email</h1>
        <p style="font-size: 1.2rem;">
            Please verify your email address to access your account
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.info(f"""
        We sent a verification email to **{email}**.
        
        Please check your inbox and click the verification link.
        """)
        
        st.markdown("### Didn't receive the email?")
        
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            if st.button("📨 Resend Verification Email", use_container_width=True, type="primary"):
                email_service = EmailService()
                verification_token = AuthTokenManager.create_verification_token(email)
                email_sent = email_service.send_verification_email(email, verification_token)
                
                if email_sent:
                    st.success("✅ Verification email sent! Check your inbox.")
                else:
                    st.warning("📧 In development mode, check the console for the verification link.")
        
        with col_btn2:
            if st.button("🚪 Logout", use_container_width=True):
                st.session_state.logged_in = False
                st.session_state.user_data = None
                st.rerun()
        
        st.markdown("---")
        
        with st.expander("💡 Troubleshooting"):
            st.write("""
            **Email not arriving?**
            
            1. ✉️ Check your spam/junk folder
            2. ✅ Make sure you entered the correct email
            3. ⏰ Wait a few minutes for delivery
            4. 📞 Contact support: support@legaldocpro.com
            
            **In development mode?**
            
            If `SENDGRID_API_KEY` is not set in your `.env` file, the verification link 
            will be displayed in the application instead of being emailed.
            """)

def handle_forgot_password():
    """Handle forgot password page"""
    query_params = st.query_params
    
    if query_params.get('page') == 'forgot_password':
        from pages.forgot_password import show
        show()
        return True
    
    return False

def main():
    """Main application function"""
    
    try:
        # Skip scheduler for now to avoid issues
        # email_scheduler = EmailScheduler()
        # email_scheduler.run_scheduled_tasks()
        
        # Handle email verification and password reset FIRST
        verification_result = handle_email_verification()
        if verification_result is not None:
            return
        
        reset_result = handle_password_reset()
        if reset_result is not None:
            return
        
        forgot_result = handle_forgot_password()
        if forgot_result:
            return
        
        # Initialize session state and load data
        initialize_session_state()
        load_sample_data()
        
        # Initialize authentication service
        auth_service = AuthService()
        
        # Check authentication
        if not auth_service.is_logged_in():
            auth_service.show_login()
            return
        
        # Check if email is verified (default True for demo users)
        user_data = st.session_state.get('user_data', {})
        if not user_data.get('email_verified', True):
            show_email_verification_warning()
            return
        
        # Add styling for logged-in pages
        st.markdown("""
        <style>
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
        
        .main .block-container {
            background: #1e293b !important;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3) !important;
            border: 1px solid #334155 !important;
        }
        
        .main .block-container > div:not(.stPlotlyChart) * {
            color: #e2e8f0 !important;
        }

        .stPlotlyChart * {
            color: #000000 !important;
        }
        
        h1, h2, h3, h4, h5, h6 {
            color: #f1f5f9 !important;
        }
        
        [data-testid="stMetricValue"] {
            color: #60a5fa !important;
        }
        
        [data-testid="stMetricLabel"] {
            color: #cbd5e1 !important;
        }
        
        .js-plotly-plot .plotly, .js-plotly-plot .plot-container {
            background: #ffffff !important;
        }
        
        .stPlotlyChart {
            background: #ffffff !important;
            border-radius: 8px !important;
            padding: 1rem !important;
        }
        
        .dataframe {
            background: #1e293b !important;
            color: #e2e8f0 !important;
        }
        
        .dataframe th {
            background: #334155 !important;
            color: #f1f5f9 !important;
        }
        
        .dataframe td {
            background: #1e293b !important;
            color: #e2e8f0 !important;
            border-color: #334155 !important;
        }
        
        .stTextInput input, .stSelectbox select, .stTextArea textarea {
            background: #334155 !important;
            color: #e2e8f0 !important;
            border-color: #475569 !important;
        }
        
        .main .block-container::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #3b82f6 0%, #06b6d4 100%);
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Render sidebar
        auth_service.render_sidebar()
        
        # Get current page from session state
        current_page = st.session_state.get('current_page', 'Executive Dashboard')
        
        # Handle user settings modal
        if st.session_state.get('show_user_settings', False):
            auth_service.show_user_settings()
        
        # Check if we should show upgrade modal
        if 'show_upgrade_modal' in st.session_state:
            try:
                from components.upgrade_modal import show_upgrade_modal
                
                modal_data = st.session_state['show_upgrade_modal']
                user_data = st.session_state.get('user_data', {})
                org_code = user_data.get('organization_code')
                subscription = st.session_state.subscriptions.get(org_code, {})
                
                show_upgrade_modal(
                    subscription.get('plan', 'basic'),
                    modal_data['feature_name'],
                    modal_data['feature_display_name']
                )
            except Exception as e:
                st.error(f"Upgrade modal error: {e}")
                del st.session_state['show_upgrade_modal']
        
        # Route to appropriate page
        if current_page in page_modules:
            try:
                page_modules[current_page]()
            except Exception as e:
                st.error(f"Error loading {current_page}: {str(e)}")
                st.markdown("### Troubleshooting")
                st.write("This error occurred while loading the page.")
                
                if st.button("🏠 Return to Dashboard"):
                    st.session_state['current_page'] = 'Executive Dashboard'
                    st.rerun()
        else:
            st.error(f"Page '{current_page}' not found")
            
            if st.button("🏠 Go to Dashboard"):
                st.session_state['current_page'] = 'Executive Dashboard'
                st.rerun()
    
    except RecursionError:
        st.error("⚠️ Recursion Error - App reloaded too many times")
        if st.button("🔄 Reset App"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    except Exception as e:
        st.error("Application Error")
        st.write(f"An error occurred: {str(e)}")
        
        with st.expander("🔧 Debug Information"):
            import traceback
            st.code(traceback.format_exc())

def show_system_status():
    """Show system status in sidebar"""
    try:
        with st.sidebar:
            st.markdown("---")
            st.markdown("**System Status**")
            st.success("🟢 Operational")
    except:
        pass

def handle_error(error, context="Application"):
    """Centralized error handling"""
    st.error(f"{context} Error: {str(error)}")
    
    with st.expander("Error Details"):
        st.code(str(error))

if __name__ == "__main__":
    try:
        main()
        show_system_status()
    except Exception as e:
        handle_error(e, "Main Application")
        
        st.markdown("""
        <div class="main-header">
            <h1>⚖️ LegalDoc Pro</h1>
            <p>Enterprise Legal Management Platform</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.error("The application encountered an error during startup.")
        
        if st.button("🔄 Try Again"):
            st.rerun()
