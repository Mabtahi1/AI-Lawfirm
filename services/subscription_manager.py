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
                    'email_verified': True
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
                    'email_verified': True
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
                    'email_verified': True
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
    
    def show_login(self):
        """Show login page"""
        st.markdown("""
        <div class="main-header">
            <h1>⚖️ LegalDoc Pro</h1>
            <p>Enterprise Legal Management Platform</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown("### Login to Your Account")
            
            # Show demo accounts info
            with st.expander("📝 Demo Accounts", expanded=False):
                st.info("""
                **Basic Plan:** basic@demo.com / demo123
                **Professional Plan:** pro@demo.com / demo123  
                **Enterprise Plan:** enterprise@demo.com / demo123
                """)
            
            email = st.text_input("Email", placeholder="your@email.com")
            password = st.text_input("Password", type="password")
            
            remember_me = st.checkbox("Remember me")
            
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
                        
                        org_code = user_data.get('organization_code')
                        
                        if not org_code:
                            st.error("⚠️ User account missing organization code. Please contact support.")
                            return
                        
                        # Get their subscription
                        subscription = st.session_state.subscriptions.get(org_code, {})
                        
                        # Check if trial expired
                        if subscription.get('status') == 'trial':
                            trial_end_str = subscription.get('trial_end_date')
                            if trial_end_str:
                                from datetime import datetime
                                trial_end = datetime.fromisoformat(trial_end_str)
                                if datetime.now() > trial_end:
                                    st.error("⚠️ Your trial has expired. Please update your payment information to continue.")
                                    return
                        
                        # Log them in
                        st.session_state.logged_in = True
                        st.session_state.user_data = user_data
                        st.session_state.current_page = 'Executive Dashboard'
                        
                        plan = subscription.get('plan', 'basic')
                        st.success(f"Welcome back, {user_data.get('first_name', user_data['name'])}! ({plan.title()} Plan)")
                        st.rerun()
                    else:
                        st.error("❌ Invalid email or password")
                else:
                    st.error("❌ Invalid email or password")
            
            st.markdown("---")
            st.caption("Contact your administrator for access")
    
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
    
    def show_user_settings(self):
        """Show user settings modal"""
        pass
