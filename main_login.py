import streamlit as st
import time

def show_login_page(auth_service):
    """Show login/signup page"""
    
    # CSS Styling
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    }

    .login-container {
        max-width: 500px;
        margin: 50px auto;
        background: white;
        padding: 3rem;
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.3);
    }

    .auth-header {
        text-align: center;
        margin-bottom: 2rem;
    }

    .auth-header h1 {
        color: #667eea;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }

    .demo-accounts {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1.5rem 0;
        border-left: 4px solid #667eea;
    }

    .demo-accounts strong {
        color: #667eea;
    }

    .stButton button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem;
        border-radius: 10px;
        font-weight: 600;
        font-size: 1rem;
        margin-top: 1rem;
    }

    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }

    .stTextInput input {
        border-radius: 10px;
        border: 2px solid #e9ecef;
        padding: 0.75rem;
    }

    .stTextInput input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
    }
    </style>
    """, unsafe_allow_html=True)

    # Initialize session state for form toggle
    if 'show_signup_form' not in st.session_state:
        st.session_state.show_signup_form = False

    # Main container
    st.markdown('<div class="login-container">', unsafe_allow_html=True)

    # Header
    st.markdown("""
    <div class="auth-header">
        <h1>⚖️ LegalDoc Pro</h1>
        <p style="color: #666; font-size: 1.1rem;">Enterprise Legal Management Platform</p>
    </div>
    """, unsafe_allow_html=True)

    # Show either login or signup form
    if not st.session_state.show_signup_form:
        # ============= LOGIN FORM =============
        st.markdown("### 🔑 Login to Your Account")
        
        # Demo accounts
        st.markdown("""
        <div class="demo-accounts">
            <strong>📝 Demo Accounts:</strong><br><br>
            <strong>Starter:</strong> basic@demo.com / demo123<br>
            <strong>Professional:</strong> pro@demo.com / demo123<br>
            <strong>Enterprise:</strong> enterprise@demo.com / demo123
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            email = st.text_input("📧 Email", placeholder="your@email.com")
            password = st.text_input("🔒 Password", type="password", placeholder="Enter password")
            
            submitted = st.form_submit_button("🚀 Login")
            
            if submitted:
                if not email or not password:
                    st.error("⚠️ Please enter email and password")
                else:
                    with st.spinner("Logging in..."):
                        success, message = auth_service.login(email, password)
                        
                        if success:
                            st.success("✅ Login successful!")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error(f"❌ {message}")
        
        # Toggle to signup
        if st.button("✨ Don't have an account? Sign Up", type="secondary"):
            st.session_state.show_signup_form = True
            st.rerun()

    else:
        # ============= SIGNUP FORM =============
        st.markdown("### ✨ Create Your Account")
        st.info("🎉 14-day free trial. No credit card required!")
        
        with st.form("signup_form"):
            # Organization info
            st.markdown("#### 🏢 Organization")
            col1, col2 = st.columns(2)
            with col1:
                org_name = st.text_input("Firm Name*", placeholder="Smith Law")
            with col2:
                org_code = st.text_input("Org Code*", placeholder="smithlaw")
            
            # Personal info
            st.markdown("#### 👤 Your Information")
            col1, col2 = st.columns(2)
            with col1:
                first_name = st.text_input("First Name*", placeholder="John")
            with col2:
                last_name = st.text_input("Last Name*", placeholder="Smith")
            
            email = st.text_input("📧 Email*", placeholder="john@smithlaw.com")
            
            col1, col2 = st.columns(2)
            with col1:
                password = st.text_input("🔒 Password*", type="password", placeholder="Min. 8 chars")
            with col2:
                confirm_password = st.text_input("🔒 Confirm*", type="password", placeholder="Re-enter")
            
            # Plan selection
            st.markdown("#### 💳 Choose Plan")
            plan = st.selectbox("Select", ["Starter - $299/month", "Professional - $599/month", "Enterprise - $999/month"])
            
            agree = st.checkbox("I agree to Terms")
            
            submitted = st.form_submit_button("🚀 Create Account")
            
            if submitted:
                errors = []
                
                if not all([org_name, org_code, first_name, last_name, email, password]):
                    errors.append("All fields required")
                
                if password and len(password) < 8:
                    errors.append("Password min. 8 characters")
                
                if password != confirm_password:
                    errors.append("Passwords don't match")
                
                if not agree:
                    errors.append("Agree to Terms")
                
                if org_code and (' ' in org_code or org_code != org_code.lower()):
                    errors.append("Org code: lowercase, no spaces")
                
                if errors:
                    for error in errors:
                        st.error(f"⚠️ {error}")
                else:
                    plan_name = "basic" if "Starter" in plan else ("professional" if "Professional" in plan else "enterprise")
                    
                    with st.spinner("Creating account..."):
                        success, message = auth_service.register(
                            email=email,
                            password=password,
                            name=f"{first_name} {last_name}",
                            organization_name=org_name,
                            organization_code=org_code,
                            plan=plan_name
                        )
                        
                        if success:
                            st.success("✅ Account created!")
                            st.balloons()
                            time.sleep(2)
                            st.session_state.show_signup_form = False
                            st.rerun()
                        else:
                            st.error(f"❌ {message}")
        
        # Toggle back to login
        if st.button("🔑 Already have account? Login", type="secondary"):
            st.session_state.show_signup_form = False
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
