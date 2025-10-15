import streamlit as st
from services.subscription_manager import SubscriptionManager
from services.subscription_config import SUBSCRIPTION_PLANS
from datetime import datetime
from services.payment_service import PaymentService

def show():
    """Display billing and subscription management page"""
    
    subscription_manager = SubscriptionManager()
    user_data = st.session_state.get('user_data', {})
    org_code = user_data.get('organization_code')
    
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
    /* Default: Light text everywhere */
    * {
        color: #e2e8f0 !important;
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
    
    # Get current subscription
    subscription = subscription_manager.get_organization_subscription(org_code)
    current_plan = subscription.get('plan', 'basic')
    
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Current Plan", 
        "🚀 Upgrade Options", 
        "📈 Usage History",
        "💳 Payment Methods"  # NEW TAB
    ])
    
    with tab1:
        show_current_plan(subscription_manager, org_code, current_plan)
    
    with tab2:
        show_upgrade_options(subscription_manager, org_code, current_plan)
    
    with tab3:
        show_usage_history(subscription_manager, org_code)
    with tab4:
        show_payment_methods(subscription_manager, org_code, current_plan)

def show_payment_methods(subscription_manager, org_code, current_plan):
    """Show and manage payment methods"""
    
    st.markdown("### 💳 Payment Methods")
    
    payment_service = PaymentService()
    subscription = subscription_manager.get_organization_subscription(org_code)
    
    # Check if on trial
    if subscription.get('status') == 'trial':
        from datetime import datetime
        trial_end = datetime.fromisoformat(subscription['trial_end_date'])
        days_left = (trial_end - datetime.now()).days
        
        if days_left > 0:
            st.info(f"""
            ⏰ **You're on a free trial**
            
            Your trial ends in **{days_left} days**. Add a payment method to continue after your trial.
            """)
        else:
            st.warning("⚠️ **Your trial has expired**. Add a payment method to continue using premium features.")
    
    # Show existing payment methods
    st.markdown("#### Your Payment Methods")
    
    # Mock payment methods (in production, fetch from Stripe)
    payment_methods = st.session_state.get('payment_methods', {}).get(org_code, [])
    
    if payment_methods:
        for idx, method in enumerate(payment_methods):
            col1, col2, col3 = st.columns([3, 2, 1])
            
            with col1:
                st.write(f"**{method['brand']} ending in {method['last4']}**")
                st.caption(f"Expires {method['exp_month']}/{method['exp_year']}")
            
            with col2:
                if method.get('default'):
                    st.success("✅ Default")
                else:
                    if st.button("Set as Default", key=f"default_{idx}"):
                        # Set as default
                        for pm in payment_methods:
                            pm['default'] = False
                        method['default'] = True
                        st.rerun()
            
            with col3:
                if st.button("🗑️", key=f"delete_{idx}"):
                    payment_methods.pop(idx)
                    st.rerun()
            
            st.markdown("---")
    else:
        st.info("No payment methods on file")
    
    # Add new payment method
    st.markdown("#### ➕ Add Payment Method")
    
    with st.expander("Add New Card"):
        with st.form("add_payment_method"):
            col1, col2 = st.columns(2)
            
            with col1:
                card_number = st.text_input("Card Number", placeholder="4242 4242 4242 4242")
                card_name = st.text_input("Name on Card")
            
            with col2:
                col_exp1, col_exp2 = st.columns(2)
                with col_exp1:
                    exp_month = st.selectbox("Month", list(range(1, 13)))
                with col_exp2:
                    exp_year = st.selectbox("Year", list(range(2025, 2036)))
                
                cvv = st.text_input("CVV", max_chars=4, placeholder="123")
            
            set_default = st.checkbox("Set as default payment method", value=len(payment_methods) == 0)
            
            submitted = st.form_submit_button("💾 Save Card", use_container_width=True, type="primary")
            
            if submitted:
                if not card_number or len(card_number.replace(" ", "")) != 16:
                    st.error("Please enter a valid card number")
                elif not cvv or len(cvv) < 3:
                    st.error("Please enter a valid CVV")
                else:
                    # Add payment method
                    new_method = {
                        'brand': 'Visa' if card_number[0] == '4' else 'Mastercard',
                        'last4': card_number.replace(" ", "")[-4:],
                        'exp_month': exp_month,
                        'exp_year': exp_year,
                        'default': set_default or len(payment_methods) == 0
                    }
                    
                    if 'payment_methods' not in st.session_state:
                        st.session_state.payment_methods = {}
                    
                    if org_code not in st.session_state.payment_methods:
                        st.session_state.payment_methods[org_code] = []
                    
                    # If setting as default, remove default from others
                    if new_method['default']:
                        for pm in st.session_state.payment_methods[org_code]:
                            pm['default'] = False
                    
                    st.session_state.payment_methods[org_code].append(new_method)
                    
                    # If trial expired, activate subscription
                    if subscription.get('status') == 'trial':
                        from datetime import datetime
                        trial_end = datetime.fromisoformat(subscription['trial_end_date'])
                        if datetime.now() > trial_end:
                            subscription['status'] = 'active'
                            
                            # Send payment success email
                            user_data = st.session_state.get('user_data', {})
                            email_service = EmailService()
                            plan_details = SUBSCRIPTION_PLANS[current_plan]
                            email_service.send_payment_success_email(
                                user_data['email'],
                                user_data['first_name'],
                                plan_details['price'],
                                plan_details['name']
                            )
                    
                    st.success("✅ Payment method added successfully!")
                    st.rerun()

def show_current_plan(subscription_manager, org_code, current_plan):
    """Display current subscription plan details"""
    
    plan_details = subscription_manager.get_plan_details(current_plan)
    
    # Plan header
    plan_colors = {
        'basic': '#6c757d',
        'professional': '#007bff',
        'enterprise': '#28a745'
    }
    
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, {plan_colors[current_plan]}, {plan_colors[current_plan]}dd);
        color: white;
        padding: 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
    ">
        <h2>{plan_details['name']}</h2>
        <h1>${plan_details['price']}/month</h1>
        <p>{plan_details['description']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Current usage metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        matters = len(st.session_state.get('matters', []))
        max_matters = plan_details['limits']['max_matters']
        matters_display = f"{matters}/{max_matters}" if max_matters != -1 else f"{matters}/∞"
        st.metric("Active Matters", matters_display)
    
    with col2:
        documents = len(st.session_state.get('documents', []))
        max_docs = plan_details['limits']['max_documents']
        docs_display = f"{documents}/{max_docs}" if max_docs != -1 else f"{documents}/∞"
        st.metric("Documents", docs_display)
    
    with col3:
        users = plan_details['limits']['max_users']
        users_display = users if users != -1 else "∞"
        st.metric("Users", f"1/{users_display}")
    
    with col4:
        storage = plan_details['limits']['storage_gb']
        storage_display = f"{storage} GB" if storage != -1 else "∞"
        st.metric("Storage", storage_display)
    
    # AI Usage (for Professional and Enterprise)
    if current_plan in ['professional', 'enterprise']:
        st.markdown("---")
        st.markdown("### 🤖 AI Feature Usage (This Month)")
        
        col_ai1, col_ai2, col_ai3 = st.columns(3)
        
        with col_ai1:
            usage = subscription_manager.get_feature_usage(org_code, 'case_comparison')
            limit = subscription_manager.get_feature_limit(org_code, 'case_comparison')
            
            if limit == -1:
                st.metric("Case Comparisons", f"{usage} (Unlimited)")
            else:
                percentage = (usage / limit * 100) if limit > 0 else 0
                st.metric("Case Comparisons", f"{usage}/{limit}")
                st.progress(percentage / 100)
        
        with col_ai2:
            usage = subscription_manager.get_feature_usage(org_code, 'ai_insights')
            limit = subscription_manager.get_feature_limit(org_code, 'ai_insights')
            
            if limit == -1:
                st.metric("AI Insights", f"{usage} (Unlimited)")
            else:
                percentage = (usage / limit * 100) if limit > 0 else 0
                st.metric("AI Insights", f"{usage}/{limit}")
                st.progress(percentage / 100)
        
        with col_ai3:
            usage = subscription_manager.get_feature_usage(org_code, 'advanced_searches')
            limit = subscription_manager.get_feature_limit(org_code, 'advanced_searches')
            
            if limit == -1:
                st.metric("Advanced Searches", f"{usage} (Unlimited)")
            else:
                percentage = (usage / limit * 100) if limit > 0 else 0
                st.metric("Advanced Searches", f"{usage}/{limit}")
                st.progress(percentage / 100)
    
    # Features list
    st.markdown("---")
    st.markdown("### ✨ Your Plan Features")
    
    col_feat1, col_feat2 = st.columns(2)
    
    features = plan_details['features']
    feature_list = list(features.items())
    mid = len(feature_list) // 2
    
    with col_feat1:
        for feature_key, enabled in feature_list[:mid]:
            icon = "✅" if enabled else "❌"
            feature_name = feature_key.replace('_', ' ').title()
            st.markdown(f"{icon} {feature_name}")
    
    with col_feat2:
        for feature_key, enabled in feature_list[mid:]:
            icon = "✅" if enabled else "❌"
            feature_name = feature_key.replace('_', ' ').title()
            st.markdown(f"{icon} {feature_name}")
    
    # Support level
    st.markdown("---")
    st.markdown("### 🎧 Support")
    st.info(f"**{plan_details['support']}**")
    
    # Billing information
    st.markdown("---")
    st.markdown("### 💳 Billing Information")
    
    col_bill1, col_bill2 = st.columns(2)
    
    with col_bill1:
        st.write(f"**Next Billing Date:** {datetime.now().strftime('%B %d, %Y')}")
        st.write(f"**Amount:** ${plan_details['price']}/month")
    
    with col_bill2:
        st.write(f"**Payment Method:** •••• 4242")
        st.write(f"**Status:** ✅ Active")
    
    # Action buttons
    st.markdown("---")
    col_btn1, col_btn2, col_btn3 = st.columns(3)
    
    with col_btn1:
        if st.button("📄 Download Invoice", use_container_width=True):
            st.info("Invoice generation coming soon!")
    
    with col_btn2:
        if st.button("💳 Update Payment Method", use_container_width=True):
            st.info("Payment method update coming soon!")
    
    with col_btn3:
        if current_plan != 'enterprise':
            if st.button("🚀 Upgrade Plan", type="primary", use_container_width=True):
                st.session_state['show_upgrade_tab'] = True
                st.rerun()

def show_upgrade_options(subscription_manager, org_code, current_plan):
    """Display upgrade options"""
    
    st.markdown("### 🚀 Choose Your Plan")
    
    # Create pricing cards
    col1, col2, col3 = st.columns(3)
    
    plans = ['basic', 'professional', 'enterprise']
    columns = [col1, col2, col3]
    
    for plan_name, col in zip(plans, columns):
        plan_details = subscription_manager.get_plan_details(plan_name)
        
        with col:
            # Highlight current plan
            is_current = (plan_name == current_plan)
            border_color = "#28a745" if is_current else "#dee2e6"
            
            st.markdown(f"""
            <div style="
                border: 3px solid {border_color};
                border-radius: 16px;
                padding: 1.5rem;
                background: white;
                height: 100%;
                position: relative;
            ">
                {"<div style='position: absolute; top: -15px; right: 20px; background: #28a745; color: white; padding: 5px 15px; border-radius: 20px; font-weight: bold;'>CURRENT</div>" if is_current else ""}
                <h3>{plan_details['name']}</h3>
                <h2 style="color: #2E86AB;">${plan_details['price']}<span style="font-size: 1rem; color: #666;">/month</span></h2>
                <p style="color: #666; min-height: 60px;">{plan_details['description']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("**Key Features:**")
            
            # Show top features
            key_features = []
            
            if plan_name == 'basic':
                key_features = [
                    "50 matters",
                    "500 documents",
                    "Core features",
                    "Email support"
                ]
            elif plan_name == 'professional':
                key_features = [
                    "200 matters",
                    "5,000 documents",
                    "25 AI comparisons/mo",
                    "50 AI insights/mo",
                    "Priority support"
                ]
            else:  # enterprise
                key_features = [
                    "Unlimited everything",
                    "Unlimited AI features",
                    "API access",
                    "24/7 support",
                    "Custom integrations"
                ]
            
            for feature in key_features:
                st.markdown(f"✅ {feature}")
            
            st.markdown("---")
            
            # Action button
            if is_current:
                st.button("Current Plan ✓", disabled=True, use_container_width=True, key=f"current_{plan_name}")
            elif plans.index(plan_name) < plans.index(current_plan):
                st.button("Downgrade", use_container_width=True, key=f"downgrade_{plan_name}")
            else:
                if st.button(f"Upgrade to {plan_details['name']}", type="primary", use_container_width=True, key=f"upgrade_{plan_name}"):
                    show_upgrade_confirmation(org_code, plan_name, plan_details)

def show_upgrade_confirmation(org_code, new_plan, plan_details):
    """Show upgrade confirmation dialog"""
    
    st.markdown("---")
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #007bff, #00bfff);
        color: white;
        padding: 2rem;
        border-radius: 16px;
        text-align: center;
    ">
        <h2>🎉 Confirm Upgrade</h2>
        <h3>Upgrade to {plan_details['name']}</h3>
        <p style="font-size: 1.2rem;">New monthly charge: ${plan_details['price']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("✅ Confirm Upgrade", type="primary", use_container_width=True):
            # Update subscription
            if 'subscriptions' not in st.session_state:
                st.session_state.subscriptions = {}
            
            st.session_state.subscriptions[org_code] = {
                'plan': new_plan,
                'status': 'active',
                'start_date': datetime.now().isoformat()
            }
            
            st.success(f"✅ Successfully upgraded to {plan_details['name']}!")
            st.balloons()
            
            # Redirect to dashboard after 2 seconds
            import time
            time.sleep(2)
            st.session_state['current_page'] = 'Executive Dashboard'
            st.rerun()
    
    with col2:
        if st.button("❌ Cancel", use_container_width=True):
            st.rerun()

def show_usage_history(subscription_manager, org_code):
    """Display usage history"""
    
    st.markdown("### 📈 Usage History")
    
    # Mock usage data - in production, this would come from a database
    usage_data = {
        'Date': ['2025-10-01', '2025-10-08', '2025-10-15'],
        'Case Comparisons': [5, 8, 12],
        'AI Insights': [15, 22, 28],
        'Advanced Searches': [30, 45, 67],
        'Documents Created': [25, 38, 52]
    }
    
    import pandas as pd
    df = pd.DataFrame(usage_data)
    
    # Display as table
    st.dataframe(df, use_container_width=True)
    
    # Show chart
    st.markdown("#### Usage Trends")
    
    chart_data = pd.DataFrame({
        'Week': ['Week 1', 'Week 2', 'Week 3'],
        'Case Comparisons': [5, 8, 12],
        'AI Insights': [15, 22, 28]
    })
    
    st.line_chart(chart_data.set_index('Week'))
    
    # Export option
    st.markdown("---")
    csv = df.to_csv(index=False)
    st.download_button(
        label="📥 Download Usage Report (CSV)",
        data=csv,
        file_name=f"usage_report_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )
if __name__ == "__main__":
    show()    
