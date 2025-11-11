from .subscription_config import SUBSCRIPTION_PLANS
import streamlit as st
from datetime import datetime

# Import these at the top to avoid circular imports
from services.email_service import AuthTokenManager, EmailService

class SubscriptionManager:
    """Enhanced subscription manager with usage tracking"""
    
    def __init__(self):
        # Initialize usage tracking in session state
        if 'feature_usage' not in st.session_state:
            st.session_state.feature_usage = {}
        
        # ALWAYS ensure demo users exist (update them every time)
        if 'users' not in st.session_state:
            st.session_state.users = {}
        
        # Force update demo users to ensure they have correct data
        demo_users = {
            'basic@demo.com': {
                'password': AuthTokenManager.hash_password('demo123'),
                'data': {
                    'name': 'Basic User',
                    'first_name': 'Basic',
                    'email': 'basic@demo.com',
                    'organization_code': 'ORG001',
                    'is_subscription_owner': True,
                    'email_verified': True,
                    'role': 'subscription_owner'
                }
            },
            'pro@demo.com': {
                'password': AuthTokenManager.hash_password('demo123'),
                'data': {
                    'name': 'Professional User',
                    'first_name': 'Professional',
                    'email': 'pro@demo.com',
                    'organization_code': 'ORG002',
                    'is_subscription_owner': True,
                    'email_verified': True,
                    'role': 'subscription_owner'
                }
            },
            'enterprise@demo.com': {
                'password': AuthTokenManager.hash_password('demo123'),
                'data': {
                    'name': 'Enterprise User',
                    'first_name': 'Enterprise',
                    'email': 'enterprise@demo.com',
                    'organization_code': 'ORG003',
                    'is_subscription_owner': True,
                    'email_verified': True,
                    'role': 'subscription_owner'
                }
            }
        }
        
        # Update demo users every time
        for email, user_info in demo_users.items():
            st.session_state.users[email] = user_info
        
        # ALWAYS ensure subscriptions are correct
        if 'subscriptions' not in st.session_state:
            st.session_state.subscriptions = {}
        
        # Force update subscriptions every time
        st.session_state.subscriptions.update({
            'ORG001': {'plan': 'basic', 'status': 'active'},
            'ORG002': {'plan': 'professional', 'status': 'active'},
            'ORG003': {'plan': 'enterprise', 'status': 'active'}
        })
    
    def get_organization_subscription(self, org_code):
        """Get subscription details for an organization"""
        subscriptions = st.session_state.get('subscriptions', {})
        return subscriptions.get(org_code, {
            'plan': 'basic',
            'status': 'active',
            'start_date': datetime.now().isoformat(),
            'billing_cycle': 'monthly'
        })
    
    def get_plan_details(self, plan_name):
        """Get details for a specific plan"""
        return SUBSCRIPTION_PLANS.get(plan_name, SUBSCRIPTION_PLANS['basic'])

    def get_plan_limits(self, plan_name):
        """Get all limits for a specific plan"""
        plan_details = self.get_plan_details(plan_name)
        return plan_details.get('limits', {})
    
    def can_use_feature(self, org_code, feature_name):
        """Check if organization can use a specific feature"""
        subscription = self.get_organization_subscription(org_code)
        plan_name = subscription.get('plan', 'basic')
        plan_details = self.get_plan_details(plan_name)
        
        return plan_details['features'].get(feature_name, False)
    
    def get_feature_limit(self, org_code, feature_name):
        """Get the usage limit for a feature"""
        subscription = self.get_organization_subscription(org_code)
        plan_name = subscription.get('plan', 'basic')
        plan_details = self.get_plan_details(plan_name)
        
        limit_key = f"{feature_name}_per_month"
        return plan_details['limits'].get(limit_key, 0)
    
    def get_feature_usage(self, org_code, feature_name):
        """Get current usage for a feature this month"""
        usage_key = f"{org_code}_{feature_name}_{datetime.now().strftime('%Y_%m')}"
        return st.session_state.feature_usage.get(usage_key, 0)
    
    def increment_feature_usage(self, org_code, feature_name):
        """Increment usage counter for a feature"""
        usage_key = f"{org_code}_{feature_name}_{datetime.now().strftime('%Y_%m')}"
        current_usage = st.session_state.feature_usage.get(usage_key, 0)
        st.session_state.feature_usage[usage_key] = current_usage + 1
    
    def can_use_feature_with_limit(self, org_code, feature_name):
        """Check if feature can be used (considers usage limits)"""
        # First check if feature is available in plan
        if not self.can_use_feature(org_code, feature_name):
            return False, "Feature not available in your plan"
        
        # Check usage limits
        limit = self.get_feature_limit(org_code, feature_name)
        
        # -1 means unlimited
        if limit == -1:
            return True, "unlimited"
        
        usage = self.get_feature_usage(org_code, feature_name)
        
        if usage >= limit:
            return False, f"Monthly limit reached ({usage}/{limit})"
        
        return True, f"{usage}/{limit} used"
    
    def has_ai_feature(self, org_code, feature_type):
        """Check if organization has AI features"""
        subscription = self.get_organization_subscription(org_code)
        plan_name = subscription.get('plan', 'basic')
        
        # Basic plan has no AI features
        if plan_name == 'basic':
            return False
        
        # Professional and Enterprise have AI features
        return True
    
    def update_subscription(self, org_code, new_plan):
        """Update subscription plan"""
        try:
            if 'subscriptions' not in st.session_state:
                st.session_state.subscriptions = {}
            
            st.session_state.subscriptions[org_code] = {
                'plan': new_plan,
                'status': 'active',
                'start_date': datetime.now().isoformat(),
                'billing_cycle': 'monthly'
            }
            return True
        except:
            return False
    
    def show_subscription_widget(self, org_code):
        """Display subscription status widget in sidebar"""
        subscription = self.get_organization_subscription(org_code)
        plan_name = subscription.get('plan', 'basic')
        plan_details = self.get_plan_details(plan_name)
        
        # Plan badge
        plan_colors = {
            'basic': '#6c757d',
            'professional': '#007bff',
            'enterprise': '#28a745'
        }
        
        st.markdown(f"""
        <div style="
            background: {plan_colors.get(plan_name, '#6c757d')};
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 8px;
            text-align: center;
            margin: 0.5rem 0;
        ">
            <strong>{plan_details['name']}</strong>
        </div>
        """, unsafe_allow_html=True)
        
        # Show AI usage for Professional plan
        if plan_name == 'professional':
            st.markdown("**AI Usage This Month:**")
            
            ai_features = ['case_comparison', 'ai_insights', 'advanced_search']
            
            for feature in ai_features:
                limit = self.get_feature_limit(org_code, feature)
                usage = self.get_feature_usage(org_code, feature)
                
                if limit > 0:
                    percentage = (usage / limit) * 100 if limit > 0 else 0
                    st.progress(percentage / 100)
                    st.caption(f"{feature.replace('_', ' ').title()}: {usage}/{limit}")
        
        # Show unlimited badge for Enterprise
        elif plan_name == 'enterprise':
            st.markdown("**✨ Unlimited AI Usage**")


class EnhancedAuthService:
    """Authentication service with subscription support"""
    
    def __init__(self):
        self.subscription_manager = SubscriptionManager()
    
    def is_logged_in(self):
        """Check if user is logged in"""
        return st.session_state.get('logged_in', False)
    
    def logout(self):
        """Logout user"""
        st.session_state.logged_in = False
        st.session_state.user_data = None
        st.session_state.current_page = 'Executive Dashboard'

    def login(self, email, password):
        """Login user with email and password"""
        email = email.lower().strip()
        
        # Check if users exist in session state
        if 'users' not in st.session_state:
            st.session_state.users = {}
        
        # Check if user exists
        if email not in st.session_state.users:
            return False, "Invalid email or password"
        
        user = st.session_state.users[email]
        
        # Verify password
        if not AuthTokenManager.verify_password(password, user['password']):
            return False, "Invalid email or password"
        
        # Set logged in state
        st.session_state.logged_in = True
        st.session_state.user_data = user.get('data', {})
        
        # Ensure user_data has required fields
        if 'email' not in st.session_state.user_data:
            st.session_state.user_data['email'] = email
        
        return True, "Login successful"
        
    def has_permission(self, permission_type):
        """Check if user has specific permission"""
        # If not logged in, no permissions
        if not self.is_logged_in():
            return False
        
        user_data = st.session_state.get('user_data', {})
        
        # Subscription owners have all permissions
        if user_data.get('is_subscription_owner', False):
            return True
        
        # Check role-based permissions
        role = user_data.get('role', 'viewer')
        
        if permission_type == 'write':
            return role in ['admin', 'editor', 'subscription_owner']
        elif permission_type == 'read':
            return role in ['admin', 'editor', 'viewer', 'subscription_owner']
        elif permission_type == 'admin':
            return role in ['admin', 'subscription_owner']
        
        return False
    
    def register(self, email, password, name, organization_name, organization_code, plan='basic'):
        """Register new user - FIXED VERSION"""
        email = email.lower().strip()
        organization_code = organization_code.lower().strip()
        
        # Initialize users if not exists
        if 'users' not in st.session_state:
            st.session_state.users = {}
        
        # Initialize subscriptions if not exists
        if 'subscriptions' not in st.session_state:
            st.session_state.subscriptions = {}
        
        # Validation
        if email in st.session_state.users:
            return False, "Email already exists"
        
        if any(u.get('data', {}).get('organization_code') == organization_code 
               for u in st.session_state.users.values()):
            return False, "Organization code already taken"
        
        # Create user with proper nested structure
        st.session_state.users[email] = {
            'password': AuthTokenManager.hash_password(password),
            'data': {
                'name': name,
                'first_name': name.split()[0] if name else '',
                'email': email,
                'organization_name': organization_name,
                'organization_code': organization_code,
                'role': 'subscription_owner',
                'is_subscription_owner': True,
                'email_verified': True,
                'created_at': datetime.now().isoformat()
            }
        }
        
        # Create subscription (ACTIVE - payment already processed)
        st.session_state.subscriptions[organization_code] = {
            'plan': plan,
            'status': 'active',
            'start_date': datetime.now().isoformat(),
            'billing_cycle': 'monthly'
        }

        # Save to persistent storage
        from services.local_storage import LocalStorage
        existing_users = LocalStorage.load_all_users()
        existing_users[email] = {
            'password': st.session_state.users[email]['password'],
            'name': name,
            'organization_name': organization_name,
            'organization_code': organization_code,
            'role': 'subscription_owner',
            'created_at': datetime.now().isoformat()
        }
        LocalStorage.save_all_users(existing_users)
        
        return True, "Account created successfully"
    
    def show_login(self):
        """Beautiful professional login page"""
        
        # Initialize session state
        if 'show_signup_form' not in st.session_state:
            st.session_state.show_signup_form = False
        if 'show_payment_form' not in st.session_state:
            st.session_state.show_payment_form = False
    
        # Create columns for split layout
        col1, col2 = st.columns([1, 1], gap="large")
        
        # ============= LEFT SIDE: Logo & Branding =============
        with col1:
            st.markdown("""
            <div style="padding: 2rem; text-align: center;">
                <div style="width: 280px; height: 280px; position: relative; margin: 1rem auto 2rem auto;">
                    <div style="position: absolute; width: 220px; height: 90px; background: linear-gradient(135deg, rgba(236, 72, 153, 0.6) 0%, rgba(168, 85, 247, 0.5) 100%); border-radius: 50%; top: 10px; left: 30px; transform: rotate(-18deg); filter: blur(2px); box-shadow: 0 15px 40px rgba(236, 72, 153, 0.3);"></div>
                    <div style="position: absolute; width: 220px; height: 90px; background: linear-gradient(135deg, rgba(59, 130, 246, 0.7) 0%, rgba(6, 182, 212, 0.6) 100%); border-radius: 50%; top: 90px; left: 50px; transform: rotate(12deg); filter: blur(2px); box-shadow: 0 15px 40px rgba(59, 130, 246, 0.4);"></div>
                    <div style="position: absolute; width: 220px; height: 90px; background: linear-gradient(135deg, rgba(139, 92, 246, 0.8) 0%, rgba(99, 102, 241, 0.7) 100%); border-radius: 50%; top: 170px; left: 30px; transform: rotate(-12deg); box-shadow: 0 15px 40px rgba(139, 92, 246, 0.5);"></div>
                </div>
                <h1 style="color: white; font-size: 2.8rem; font-weight: 800; margin-bottom: 0.5rem; text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);">⚖️ Prolexis Analytics</h1>
                <p style="color: rgba(255, 255, 255, 0.85); font-size: 1.2rem; font-weight: 300; margin-bottom: 3rem;">Legal Intelligence Platform</p>
                <div style="text-align: left; max-width: 400px; margin: 0 auto; padding: 2rem; background: rgba(255, 255, 255, 0.06); backdrop-filter: blur(10px); border-radius: 16px; border: 1px solid rgba(255, 255, 255, 0.1);">
                    <h3 style="color: white; font-size: 1.3rem; margin-bottom: 1.5rem; font-weight: 600;">✨ Platform Features</h3>
                    <ul style="color: rgba(255, 255, 255, 0.9); font-size: 1rem; line-height: 2; list-style: none; padding: 0;">
                        <li>🤖 AI Document Analysis</li>
                        <li>📊 Business Intelligence</li>
                        <li>⚖️ Case Comparison</li>
                        <li>🔍 Advanced Search</li>
                        <li>💼 Matter Management</li>
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # ============= RIGHT SIDE: Clean Form =============
        with col2:
            st.markdown('<div style="padding: 2rem 1rem;">', unsafe_allow_html=True)
            
            # ============= LOGIN FORM =============
            if not st.session_state.show_signup_form and not st.session_state.show_payment_form:
                st.markdown('<h2 style="color: white; text-align: center; margin-bottom: 2rem; font-weight: 700; font-size: 2rem;">Welcome Back!</h2>', unsafe_allow_html=True)
                
                with st.expander("📝 Demo Accounts"):
                    st.markdown("""
                    **Starter:** basic@demo.com / demo123  
                    **Professional:** pro@demo.com / demo123  
                    **Enterprise:** enterprise@demo.com / demo123
                    """)
                
                with st.form("login_form"):
                    st.markdown("**Email Address**")
                    email_input = st.text_input("Email", placeholder="you@company.com", label_visibility="collapsed", key="login_email")
                    
                    st.markdown("**Password**")
                    pwd_input = st.text_input("Password", type="password", label_visibility="collapsed", key="login_pwd")
                    
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.checkbox("Remember me")
                    with col_b:
                        st.markdown('<p style="text-align: right; color: rgba(255, 255, 255, 0.7); font-size: 0.9rem; margin-top: 0.3rem;">Forgot password?</p>', unsafe_allow_html=True)
                    
                    submitted = st.form_submit_button("Sign In", use_container_width=True, type="primary")
                    
                    if submitted:
                        email = st.session_state.get('login_email', '')
                        password = st.session_state.get('login_pwd', '')
                        
                        if not email or not password:
                            st.error("⚠️ Please enter email and password")
                        else:
                            success, message = self.login(email, password)
                            if success:
                                st.success("✅ Welcome back!")
                                import time
                                time.sleep(1)
                                st.rerun()
                            else:
                                st.error(f"❌ {message}")
                
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown('<p style="text-align: center; color: rgba(255, 255, 255, 0.8);">Don\'t have an account?</p>', unsafe_allow_html=True)
                if st.button("Create Account", use_container_width=True):
                    st.session_state.show_signup_form = True
                    st.rerun()
            
            # ============= SIGNUP FORM =============
            elif st.session_state.show_signup_form and not st.session_state.show_payment_form:
                st.markdown('<h2 style="color: white; text-align: center; margin-bottom: 1.5rem; font-weight: 700; font-size: 2rem;">Get Started</h2>', unsafe_allow_html=True)
                
                with st.form("signup_form"):
                    st.markdown("**Organization**")
                    org_name = st.text_input("Firm Name", placeholder="Smith & Associates")
                    org_code = st.text_input("Organization Code", placeholder="smithlaw")
                    
                    st.markdown("**Your Information**")
                    col_a, col_b = st.columns(2)
                    with col_a:
                        first_name = st.text_input("First Name")
                    with col_b:
                        last_name = st.text_input("Last Name")
                    
                    email = st.text_input("Email", placeholder="john@smithlaw.com")
                    password = st.text_input("Password", type="password", placeholder="Min. 8 characters")
                    confirm_password = st.text_input("Confirm Password", type="password")
                    
                    st.markdown("**Plan**")
                    plan_option = st.selectbox("Choose Plan", [
                        "Starter - $299/mo",
                        "Professional - $599/mo",
                        "Enterprise - $999/mo"
                    ])
                    
                    agree = st.checkbox("I agree to Terms & authorize monthly billing")
                    
                    submitted = st.form_submit_button("Continue to Payment →", use_container_width=True, type="primary")
                    
                    if submitted:
                        errors = []
                        if not all([org_name, org_code, first_name, last_name, email, password]):
                            errors.append("All fields required")
                        if password and len(password) < 8:
                            errors.append("Password must be 8+ characters")
                        if password != confirm_password:
                            errors.append("Passwords don't match")
                        if not agree:
                            errors.append("Must agree to terms")
                        
                        if errors:
                            for error in errors:
                                st.error(f"⚠️ {error}")
                        else:
                            plan_name = "basic" if "Starter" in plan_option else ("professional" if "Professional" in plan_option else "enterprise")
                            st.session_state.temp_signup_data = {
                                'email': email,
                                'password': password,
                                'name': f"{first_name} {last_name}",
                                'organization_name': org_name,
                                'organization_code': org_code,
                                'plan': plan_name
                            }
                            st.session_state.show_payment_form = True
                            st.rerun()
                
                if st.button("← Back to Login", use_container_width=True):
                    st.session_state.show_signup_form = False
                    st.rerun()
            
            # ============= PAYMENT FORM =============
            else:
                from services.payment_service import PaymentService
                
                st.markdown('<h2 style="color: white; text-align: center; margin-bottom: 1.5rem; font-weight: 700;">Complete Payment</h2>', unsafe_allow_html=True)
                
                signup_data = st.session_state.get('temp_signup_data', {})
                plan_name = signup_data.get('plan', 'basic')
                plan_details = SUBSCRIPTION_PLANS.get(plan_name, {})
                
                st.info(f"""**{signup_data.get('organization_name')}**  
                {signup_data.get('email')}  
                {plan_details.get('name')} - ${plan_details.get('price')}/month""")
                
                payment_service = PaymentService()
                
                def complete_registration():
                    data = st.session_state.temp_signup_data
                    success, message = self.register(
                        email=data['email'],
                        password=data['password'],
                        name=data['name'],
                        organization_name=data['organization_name'],
                        organization_code=data['organization_code'],
                        plan=data['plan']
                    )
                    if success:
                        st.session_state.show_payment_form = False
                        st.session_state.show_signup_form = False
                        st.success("✅ Account created!")
                        import time
                        time.sleep(2)
                        st.rerun()
                
                payment_service.show_payment_form(plan_name=plan_name, on_success_callback=complete_registration)
                
                if st.button("← Back", use_container_width=True):
                    st.session_state.show_payment_form = False
                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)


    def _handle_forgot_password(self, email):
        """Handle forgot password request"""
        try:
            from services.email_service import EmailService, AuthTokenManager
            
            # Check if user exists (get users from session state)
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
                    
                    Check your email at **{email}** for the reset link.
                    
                    The link expires in 1 hour.
                    """)
                    st.session_state.show_forgot_password = False
                else:
                    st.warning("Unable to send email. Please contact support.")
            else:
                # Don't reveal if email exists (security best practice)
                st.success(f"""
                ✅ Password reset link sent!
                
                If an account exists for **{email}**, you'll receive a reset email shortly.
                
                The link expires in 1 hour.
                """)
                st.session_state.show_forgot_password = False
        
        except Exception as e:
            st.error(f"Error sending reset email: {str(e)}")
    
    def render_sidebar(self):
        """Render sidebar with subscription info"""
        user_data = st.session_state.get('user_data', {})
        org_code = user_data.get('organization_code')
        
        with st.sidebar:
            st.markdown(f"**{user_data.get('name', 'User')}**")
            st.caption(f"📧 {user_data.get('email', 'N/A')}")
            
            if org_code:
                st.caption(f"🏢 {org_code}")
                
                # Show subscription widget
                self.subscription_manager.show_subscription_widget(org_code)
            else:
                st.warning("⚠️ No organization")
            
            st.divider()
            
            # Navigation with feature gating
            self.show_navigation(org_code)
            
            st.divider()
            
            # Debug button (can be removed in production)
            with st.expander("🔍 Debug Info"):
                st.write("**User Data:**", user_data)
                st.write("**Org Code:**", org_code)
                if org_code and 'subscriptions' in st.session_state:
                    st.write("**Subscription:**", st.session_state.subscriptions.get(org_code))
            
            # Management options for subscription owners
            if user_data.get('is_subscription_owner'):
                if st.button("💳 Billing & Subscription", use_container_width=True):
                    st.session_state['current_page'] = 'Billing Management'
                    st.rerun()
            
            if st.button("🚪 Logout", use_container_width=True):
                self.logout()
                st.rerun()
    
    def show_navigation(self, org_code):
        """Show navigation with subscription-based restrictions"""
        if not org_code:
            st.warning("Please log in to access features")
            return
            
        subscription = self.subscription_manager.get_organization_subscription(org_code)
        if not subscription:
            st.error("Subscription not found")
            return
        
        plan_name = subscription.get('plan', 'basic')
        
        st.markdown("### 🧭 Navigation")
        
        # ========== BASIC FEATURES (All Plans) ==========
        st.markdown("**Core Features**")
        
        basic_pages = [
            ("📊 Dashboard", "Executive Dashboard"),
            ("📁 Documents", "Document Management"),
            ("⚖️ Matters", "Matter Management"),
            ("💰 Billing", "Time & Billing"),
            ("📅 Calendar", "Calendar & Tasks")
        ]
        
        for button_text, page_name in basic_pages:
            if st.button(button_text, key=f"nav_{page_name}", use_container_width=True):
                st.session_state['current_page'] = page_name
                st.rerun()
        
        # ========== AI FEATURES (Professional & Enterprise ONLY) ==========
        st.markdown("---")
        st.markdown("**AI-Powered Features**")
        
        ai_features = [
            ("🤖 AI Insights", "AI Insights", "ai_insights"),
            ("🔍 Case Comparison", "Case Comparison", "case_comparison"),
            ("🔎 Advanced Search", "Advanced Search", "advanced_search"),
            ("📊 Business Intel", "Business Intelligence", "business_intelligence")
        ]
        
        for button_text, page_name, feature_name in ai_features:
            # Always allow navigation to the page - the page itself will handle access control
            if plan_name == 'basic':
                # Basic plan users can still navigate to see upgrade prompt
                if st.button(f"{button_text} 🔒", key=f"nav_{page_name}", use_container_width=True):
                    st.session_state['current_page'] = page_name
                    st.rerun()
                st.caption("⬆️ Upgrade to unlock")
            else:
                # Professional and Enterprise users
                try:
                    can_use, status = self.subscription_manager.can_use_feature_with_limit(org_code, feature_name)
                    
                    # Show usage status for Professional plan
                    if plan_name == 'professional' and status != 'unlimited':
                        display_text = f"{button_text} ({status})"
                    elif not can_use and plan_name == 'professional':
                        display_text = f"{button_text} (Limit Reached)"
                    else:
                        display_text = button_text
                    
                    # Always allow navigation - let the page handle the limit check
                    if st.button(display_text, key=f"nav_{page_name}", use_container_width=True):
                        st.session_state['current_page'] = page_name
                        st.rerun()
                    
                    if not can_use and plan_name == 'professional':
                        st.caption(f"⚠️ {status}")
                except Exception as e:
                    # If subscription check fails, still allow navigation
                    if st.button(button_text, key=f"nav_{page_name}", use_container_width=True):
                        st.session_state['current_page'] = page_name
                        st.rerun()
        
        # ========== ENTERPRISE FEATURES ==========
        if plan_name == 'enterprise':
            st.markdown("---")
            st.markdown("**Enterprise Features**")
            
            enterprise_pages = [
                ("🔗 Integrations", "Integrations")
            ]
            
            for button_text, page_name in enterprise_pages:
                if st.button(button_text, key=f"nav_{page_name}", use_container_width=True):
                    st.session_state['current_page'] = page_name
                    st.rerun()
        elif plan_name in ['basic', 'professional']:
            # Show locked enterprise features
            st.markdown("---")
            st.markdown("**Enterprise Features 🔒**")
            st.caption("Available in Enterprise plan")
    
    def show_user_settings(self):
        """Show user settings modal"""
        pass
