import streamlit as st
from datetime import datetime

def show():
    """Display the billing management page"""
    
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
    
    # Get user's organization
    user_data = st.session_state.get('user_data', {})
    org_code = user_data.get('organization_code')
    
    if not org_code:
        st.error("⚠️ No organization code found. Please log in again.")
        return
    
    # Try to get subscription manager
    try:
        from services.subscription_manager import SubscriptionManager
        subscription_manager = SubscriptionManager()
    except Exception as e:
        st.error(f"Subscription management service not available: {e}")
        return
    
    # Get current subscription directly from session state
    subscription = st.session_state.subscriptions.get(org_code, {'plan': 'basic', 'status': 'active'})
    current_plan = subscription.get('plan', 'basic')
    
    # Debug info (can remove later)
    with st.expander("🔍 Debug - Current Subscription Info"):
        st.write("**Org Code:**", org_code)
        st.write("**Subscription:**", subscription)
        st.write("**Current Plan:**", current_plan)
    
    # Display current plan
    st.markdown("## 📊 Current Plan")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Plan", current_plan.title())
    
    with col2:
        st.metric("Status", "Active")
    
    with col3:
        st.metric("Billing Cycle", "Monthly")
    
    # Plan comparison
    st.markdown("---")
    st.markdown("## 🎯 Available Plans")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="padding: 1.5rem; background: rgba(255,255,255,0.05); border-radius: 10px; border: 2px solid #6c757d;">
            <h3 style="color: #6c757d;">Basic Plan</h3>
            <h2>$299<span style="font-size: 1rem;">/month</span></h2>
            <hr>
            <p>✅ Document management</p>
            <p>✅ Basic matter tracking</p>
            <p>✅ Up to 3 users</p>
            <p>✅ 5GB storage</p>
            <p>❌ AI features</p>
            <p>❌ Advanced analytics</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if current_plan == 'basic':
            st.success("✓ Current Plan")
        else:
            if st.button("Contact Sales", key="basic", use_container_width=True):
                st.info("Contact support@legaldocpro.com to change plans")
    
    with col2:
        st.markdown("""
        <div style="padding: 1.5rem; background: rgba(0,123,255,0.1); border-radius: 10px; border: 2px solid #007bff;">
            <h3 style="color: #007bff;">Professional Plan</h3>
            <h2>$599<span style="font-size: 1rem;">/month</span></h2>
            <hr>
            <p>✅ Everything in Basic</p>
            <p>✅ 25 AI comparisons/month</p>
            <p>✅ 50 AI insights/month</p>
            <p>✅ 100 advanced searches/month</p>
            <p>✅ Up to 10 users</p>
            <p>✅ 50GB storage</p>
            <p>✅ Priority support</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if current_plan == 'professional':
            st.success("✓ Current Plan")
        elif current_plan == 'basic':
            if st.button("Upgrade to Professional", type="primary", key="prof", use_container_width=True):
                handle_upgrade(subscription_manager, org_code, 'professional')
        else:
            if st.button("Change to Professional", key="prof_change", use_container_width=True):
                st.info("Contact support@legaldocpro.com to change plans")
    
    with col3:
        st.markdown("""
        <div style="padding: 1.5rem; background: rgba(40,167,69,0.1); border-radius: 10px; border: 2px solid #28a745;">
            <h3 style="color: #28a745;">Enterprise Plan</h3>
            <h2>$999<span style="font-size: 1rem;">/month</span></h2>
            <hr>
            <p>✅ Everything in Professional</p>
            <p>✅ <strong>Unlimited</strong> AI features</p>
            <p>✅ Unlimited users</p>
            <p>✅ Unlimited storage</p>
            <p>✅ Custom integrations</p>
            <p>✅ 24/7 support</p>
            <p>✅ API access</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if current_plan == 'enterprise':
            st.success("✓ Current Plan")
        else:
            if st.button("Upgrade to Enterprise", type="primary", key="ent", use_container_width=True):
                handle_upgrade(subscription_manager, org_code, 'enterprise')
    
    # Usage statistics
    if current_plan in ['professional', 'enterprise'] and subscription_manager:
        st.markdown("---")
        st.markdown("## 📈 Usage Statistics This Month")
        
        features = [
            ('case_comparison', 'Case Comparisons'),
            ('ai_insights', 'AI Insights'),
            ('advanced_search', 'Advanced Searches')
        ]
        
        cols = st.columns(len(features))
        
        for idx, (feature_key, feature_name) in enumerate(features):
            with cols[idx]:
                try:
                    usage = subscription_manager.get_feature_usage(org_code, feature_key)
                    limit = subscription_manager.get_feature_limit(org_code, feature_key)
                    
                    if limit == -1:
                        st.metric(feature_name, f"{usage} used", "Unlimited ✨")
                    else:
                        percentage = (usage / limit * 100) if limit > 0 else 0
                        st.metric(feature_name, f"{usage}/{limit}", f"{percentage:.0f}% used")
                        st.progress(min(usage / limit, 1.0) if limit > 0 else 0)
                except:
                    st.metric(feature_name, "N/A")
    
    # Billing history
    st.markdown("---")
    st.markdown("## 📜 Billing History")
    
    # Mock billing data
    import pandas as pd
    
    billing_data = pd.DataFrame({
        'Date': ['2025-01-01', '2024-12-01', '2024-11-01'],
        'Description': [f'{current_plan.title()} Plan', f'{current_plan.title()} Plan', f'{current_plan.title()} Plan'],
        'Amount': ['$299.00' if current_plan == 'professional' else ('$599.00' if current_plan == 'enterprise' else '$999.00')] * 3,
        'Status': ['Paid', 'Paid', 'Paid']
    })
    
    st.dataframe(billing_data, use_container_width=True, hide_index=True)
    
    # Payment method
    st.markdown("---")
    st.markdown("## 💳 Payment Method")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.info("💳 Visa ending in 4242")
        st.caption("Expires 12/2026")
    
    with col2:
        if st.button("Update Payment Method", use_container_width=True):
            st.info("Payment method update coming soon")

def handle_upgrade(subscription_manager, org_code, new_plan):
    """Handle plan upgrade"""
    
    plan_prices = {
        'basic': '$299',
        'professional': '$599',
        'enterprise': '$999'
    }
    
    st.markdown("---")
    
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 2rem 0;
    ">
        <h2>🎉 Upgrading to {new_plan.title()} Plan</h2>
        <p style="font-size: 1.3rem; margin: 1rem 0;">{plan_prices[new_plan]}/month</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Simulate payment processing
    with st.spinner("Processing your upgrade..."):
        import time
        time.sleep(2)
        
        # Update subscription
        if subscription_manager:
            try:
                # Update the subscription in session state
                if 'subscriptions' not in st.session_state:
                    st.session_state.subscriptions = {}
                
                st.session_state.subscriptions[org_code] = {
                    'plan': new_plan,
                    'status': 'active',
                    'start_date': datetime.now().isoformat(),
                    'billing_cycle': 'monthly'
                }
                
                st.success(f"✅ Successfully upgraded to {new_plan.title()} plan!")
                st.balloons()
                
                st.info("Your new features are now active. Redirecting...")
                
                time.sleep(2)
                st.rerun()
            except Exception as e:
                st.error(f"❌ Upgrade failed: {e}")
        else:
            st.error("❌ Subscription manager not available")
if __name__ == "__main__":
    show()            
