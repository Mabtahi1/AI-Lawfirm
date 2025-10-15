import streamlit as st
from datetime import datetime

def show():
    """Display the billing management page"""
    
    st.markdown("""
    <div class="main-header">
        <h1>💳 Billing Management</h1>
        <p>Manage your subscription and billing details</p>
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
            <h2>$0<span style="font-size: 1rem;">/month</span></h2>
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
            <h2>$149<span style="font-size: 1rem;">/month</span></h2>
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
            <h2>$499<span style="font-size: 1rem;">/month</span></h2>
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
        'Amount': ['$149.00' if current_plan == 'professional' else ('$499.00' if current_plan == 'enterprise' else '$0.00')] * 3,
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
        'basic': '$0',
        'professional': '$149',
        'enterprise': '$499'
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
