from .subscription_config import SUBSCRIPTION_PLANS, FEATURE_DISPLAY
import streamlit as st
from datetime import datetime

class SubscriptionManager:
    """Enhanced subscription manager with usage tracking"""
    
    def __init__(self):
        self.subscription_manager = SubscriptionManager()
    
        # Add demo users for testing
        if 'users' not in st.session_state:
            st.session_state.users = {
                'basic@demo.com': {
                    'password': 'demo123',
                    'data': {
                        'name': 'Basic User',
                        'email': 'basic@demo.com',
                        'organization_code': 'ORG001',
                        'is_subscription_owner': True
                    }
                },
                'pro@demo.com': {
                    'password': 'demo123',
                    'data': {
                        'name': 'Professional User',
                        'email': 'pro@demo.com',
                        'organization_code': 'ORG002',
                        'is_subscription_owner': True
                    }
                },
                'enterprise@demo.com': {
                    'password': 'demo123',
                    'data': {
                        'name': 'Enterprise User',
                        'email': 'enterprise@demo.com',
                        'organization_code': 'ORG003',
                        'is_subscription_owner': True
                    }
                }
            }
        
        if 'subscriptions' not in st.session_state:
            st.session_state.subscriptions = {
                'ORG001': {'plan': 'basic', 'status': 'active'},
                'ORG002': {'plan': 'professional', 'status': 'active'},
                'ORG003': {'plan': 'enterprise', 'status': 'active'}
            }
        # Initialize usage tracking in session state
        if 'feature_usage' not in st.session_state:
            st.session_state.feature_usage = {}
    
    def get_organization_subscription(self, org_code):
        """Get subscription details for an organization"""
        # This would typically come from a database
        # For now, return from session state or default
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
            
            ai_features = ['case_comparisons', 'ai_insights', 'advanced_searches']
            
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
    
    def show_login(self):
        """Show login page"""
    
        st.markdown("""
        <div class="main-header">
            <h1>⚖️ LegalDoc Pro</h1>
            <p>Enterprise Legal Management Platform</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Tabs for login and signup
        tab1, tab2 = st.tabs(["🔐 Login", "✨ Sign Up"])
        
        with tab1:
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col2:
                st.markdown("### Login to Your Account")
                
                email = st.text_input("Email", placeholder="your@email.com")
                password = st.text_input("Password", type="password")
                
                remember_me = st.checkbox("Remember me")
                
                # Forgot password link
                col_link1, col_link2 = st.columns([1, 1])
                
                with col_link2:
                    if st.button("Forgot Password?", key="forgot_pass_link"):
                        st.query_params.update({"page": "forgot_password"})
                        st.rerun()
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                if st.button("Login", use_container_width=True, type="primary"):
                    # Check if user exists
                    users = st.session_state.get('users', {})
                    
                    if email in users:
                        # Verify password
                        stored_password = users[email]['password']
                        
                        if AuthTokenManager.verify_password(password, stored_password):
                            # Valid login
                            user_data = users[email]['data']
                            
                            # Check if email verified
                            if not user_data.get('email_verified', False):
                                st.warning("⚠️ Please verify your email before logging in.")
                                
                                if st.button("📨 Resend Verification Email"):
                                    email_service = EmailService()
                                    verification_token = AuthTokenManager.create_verification_token(email)
                                    email_service.send_verification_email(email, verification_token)
                                    st.success("Verification email sent!")
                                return
                            
                            org_code = user_data['organization_code']
                            
                            # Get their subscription
                            subscription = st.session_state.subscriptions.get(org_code, {})
                            
                            # Check if trial expired
                            if subscription.get('status') == 'trial':
                                from datetime import datetime
                                trial_end = datetime.fromisoformat(subscription['trial_end_date'])
                                if datetime.now() > trial_end:
                                    st.error("⚠️ Your trial has expired. Please update your payment information to continue.")
                                    if st.button("💳 Update Payment"):
                                        st.session_state['show_billing'] = True
                                    return
                            
                            # Log them in
                            st.session_state.logged_in = True
                            st.session_state.user_data = user_data
                            st.session_state.current_page = 'Executive Dashboard'
                            
                            st.success(f"Welcome back, {user_data['first_name']}!")
                            st.rerun()
                        else:
                            st.error("❌ Invalid email or password")
                    else:
                        st.error("❌ Invalid email or password")
                
                st.markdown("---")
                
                col_help1, col_help2 = st.columns(2)
                
                with col_help1:
                    st.caption("Don't have an account?")
                
                with col_help2:
                    st.caption("[Need help?](mailto:support@legaldocpro.com)")
        
        with tab2:
            # Import and show signup page
            from pages.signup import show as show_signup
            show_signup()
    
    
    def render_sidebar(self):
        """Render sidebar with subscription info"""
        user_data = st.session_state.get('user_data', {})
        org_code = user_data.get('organization_code')
        
        with st.sidebar:
            st.markdown(f"**{user_data.get('name', 'User')}**")
            if org_code:
                st.markdown(f"**{org_code}**")
                
                # Show subscription widget
                self.subscription_manager.show_subscription_widget(org_code)
            
            st.divider()
            
            # Navigation with feature gating
            self.show_navigation(org_code)
            
            st.divider()
            
            # Management options for subscription owners
            if user_data.get('is_subscription_owner'):
                if st.button("💳 Billing & Subscription"):
                    st.session_state['current_page'] = 'Billing Management'  # CHANGED THIS
                    st.rerun()
            
            if st.button("🚪 Logout"):
                self.logout()
                st.rerun()
    
    def show_navigation(self, org_code):
        """Show navigation with subscription-based restrictions"""
        if not org_code:
            return
            
        subscription = self.subscription_manager.get_organization_subscription(org_code)
        if not subscription:
            return
        
        plan_name = subscription.get('plan', 'basic')
        
        # Show trial banner if on trial
        if subscription.get('status') == 'trial':
            from datetime import datetime
            trial_end = datetime.fromisoformat(subscription['trial_end_date'])
            days_left = (trial_end - datetime.now()).days
            
            if days_left > 0:
                st.sidebar.warning(f"⏰ Trial: {days_left} days left")
            else:
                st.sidebar.error("⚠️ Trial Expired")
        
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
            can_use, status = self.subscription_manager.can_use_feature_with_limit(org_code, feature_name)
            
            if plan_name == 'basic':
                # Basic plan users see locked features
                if st.button(f"{button_text} 🔒", disabled=True, use_container_width=True, key=f"nav_{page_name}"):
                    pass
                # Show tooltip
                st.caption(f"⬆️ Upgrade to Professional")
            else:
                # Professional and Enterprise users
                if can_use:
                    # Show usage status for Professional plan
                    if plan_name == 'professional' and status != 'unlimited':
                        display_text = f"{button_text} ({status})"
                    else:
                        display_text = button_text
                    
                    if st.button(display_text, key=f"nav_{page_name}", use_container_width=True):
                        st.session_state['current_page'] = page_name
                        st.rerun()
                else:
                    # Professional plan - limit reached
                    if st.button(f"{button_text} 🔒", disabled=True, use_container_width=True, key=f"nav_{page_name}"):
                        pass
                    st.caption(f"{status}")
        
        # ========== ENTERPRISE FEATURES ==========
        if plan_name == 'enterprise':
            st.markdown("---")
            st.markdown("**Enterprise Features**")
            
            enterprise_pages = [
                ("🔗 Integrations", "Integrations"),
                ("📱 Mobile App", "Mobile App"),
                ("⚙️ Settings", "System Settings")
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

        # ========== AI FEATURES ==========
    st.markdown("---")
    st.markdown("**AI-Powered Features**")
    
    ai_features = [
        ("🤖 AI Insights", "AI Insights", "ai_insights"),
        ("🔍 Case Comparison", "Case Comparison", "case_comparison"),
        ("🔎 Advanced Search", "Advanced Search", "advanced_search"),
        ("📊 Business Intel", "Business Intelligence", "business_intelligence")
    ]
    
    for button_text, page_name, feature_name in ai_features:
        can_use, status = self.subscription_manager.can_use_feature_with_limit(org_code, feature_name)
        
        if plan_name == 'basic':
            # Basic plan - show upgrade prompt on click
            if st.button(f"{button_text} 🔒", key=f"nav_{page_name}", use_container_width=True):
                trigger_upgrade_modal(feature_name, button_text.replace('🔒', '').strip())
                st.rerun()
            st.caption("⬆️ Upgrade to unlock")
        else:
            # Professional/Enterprise plans
            if can_use:
                if plan_name == 'professional' and status != 'unlimited':
                    display_text = f"{button_text} ({status})"
                else:
                    display_text = button_text
                
                if st.button(display_text, key=f"nav_{page_name}", use_container_width=True):
                    st.session_state['current_page'] = page_name
                    st.rerun()
            else:
                # Limit reached - show upgrade to Enterprise
                if st.button(f"{button_text} 🔒", key=f"nav_{page_name}", use_container_width=True):
                    trigger_upgrade_modal(feature_name, button_text)
                    st.rerun()
                st.caption(f"{status}")
    
    # Check if we should show upgrade modal
    if 'show_upgrade_modal' in st.session_state:
        modal_data = st.session_state['show_upgrade_modal']
        show_upgrade_modal(
            plan_name,
            modal_data['feature_name'],
            modal_data['feature_display_name']
        )
    def show_user_settings(self):
        """Show user settings modal"""
        pass
