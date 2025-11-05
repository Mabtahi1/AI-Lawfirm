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
        """Register new user"""
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
        
        # Create user
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
        
        # Create subscription (ACTIVE, no trial)
        st.session_state.subscriptions[organization_code] = {
            'plan': plan,
            'status': 'active',  # ✅ Changed from 'trial' to 'active'
            'start_date': datetime.now().isoformat(),
            'billing_cycle': 'monthly'
            # ✅ Removed trial_end field
        }
        
        return True, "Account created successfully"
    
    def show_login(self):
        """Show login/signup page"""
        
        # CSS Styling
        st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        }
        </style>
        """, unsafe_allow_html=True)
    
        # Initialize session state for form toggle
        if 'show_signup_form' not in st.session_state:
            st.session_state.show_signup_form = False
    
        # Center container
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            # Header
            st.markdown("""
            <div style="text-align: center; margin-bottom: 2rem;">
                <h1 style="color: white;">⚖️ LegalDoc Pro</h1>
                <p style="color: white; font-size: 1.1rem;">Enterprise Legal Management Platform</p>
            </div>
            """, unsafe_allow_html=True)
    
            # Show either login or signup form
            if not st.session_state.show_signup_form:
                # ============= LOGIN FORM =============
                st.markdown("### 🔑 Login to Your Account")
                
                # Demo accounts
                with st.expander("📝 Demo Accounts"):
                    st.markdown("""
                    **Starter:** basic@demo.com / demo123  
                    **Professional:** pro@demo.com / demo123  
                    **Enterprise:** enterprise@demo.com / demo123
                    """)
                
                with st.form("login_form"):
                    email = st.text_input("📧 Email", placeholder="your@email.com")
                    password = st.text_input("🔒 Password", type="password")
                    remember_me = st.checkbox("Remember me")
                    
                    submitted = st.form_submit_button("🚀 Login", use_container_width=True)
                    
                    if submitted:
                        if not email or not password:
                            st.error("⚠️ Please enter email and password")
                        else:
                            success, message = self.login(email, password)
                            if success:
                                st.success("✅ Login successful!")
                                import time
                                time.sleep(1)
                                st.rerun()
                            else:
                                st.error(f"❌ {message}")
                
                # Signup button
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("✨ Don't have an account? Sign Up", use_container_width=True):
                    st.session_state.show_signup_form = True
                    st.rerun()
    
            else:
                # ============= SIGNUP FORM =============
                st.markdown("### ✨ Create Your Account")
                st.info("🎉 14-day free trial. No credit card required!")
                
                with st.form("signup_form"):
                    st.markdown("#### 🏢 Organization")
                    org_name = st.text_input("Firm Name*", placeholder="Smith Law Firm")
                    org_code = st.text_input("Organization Code*", placeholder="smithlaw")
                    
                    st.markdown("#### 👤 Your Information")
                    col_a, col_b = st.columns(2)
                    with col_a:
                        first_name = st.text_input("First Name*")
                    with col_b:
                        last_name = st.text_input("Last Name*")
                    
                    email = st.text_input("📧 Email*", placeholder="john@smithlaw.com")
                    
                    col_a, col_b = st.columns(2)
                    with col_a:
                        password = st.text_input("🔒 Password*", type="password", placeholder="Min. 8 chars")
                    with col_b:
                        confirm_password = st.text_input("🔒 Confirm*", type="password")
                    
                    st.markdown("#### 💳 Choose Plan")
                    plan = st.selectbox("Select Plan", [
                        "Starter - $299/month",
                        "Professional - $599/month",
                        "Enterprise - $999/month"
                    ])
                    
                    agree = st.checkbox("I agree to Terms of Service")
                    
                    submitted = st.form_submit_button("🚀 Create Account", use_container_width=True)
                    
                    if submitted:
                        errors = []
                        
                        if not all([org_name, org_code, first_name, last_name, email, password]):
                            errors.append("All fields required")
                        if password and len(password) < 8:
                            errors.append("Password must be 8+ characters")
                        if password != confirm_password:
                            errors.append("Passwords don't match")
                        if not agree:
                            errors.append("Must agree to Terms")
                        if org_code and (' ' in org_code or org_code != org_code.lower()):
                            errors.append("Org code: lowercase, no spaces")
                        
                        if errors:
                            for error in errors:
                                st.error(f"⚠️ {error}")
                        else:
                            plan_name = "basic" if "Starter" in plan else (
                                "professional" if "Professional" in plan else "enterprise"
                            )
                            
                            success, message = self.register(
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
                                import time
                                time.sleep(2)
                                st.session_state.show_signup_form = False
                                st.rerun()
                            else:
                                st.error(f"❌ {message}")
                
                # Back to login button
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("🔑 Already have an account? Login", use_container_width=True):
                    st.session_state.show_signup_form = False
                    st.rerun()


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
