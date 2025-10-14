import streamlit as st
from services.subscription_manager import SubscriptionManager
from services.subscription_config import SUBSCRIPTION_PLANS
from datetime import datetime

def show():
    """Display billing and subscription management page"""
    
    subscription_manager = SubscriptionManager()
    user_data = st.session_state.get('user_data', {})
    org_code = user_data.get('organization_code')
    
    st.markdown("""
    <div class="main-header">
        <h1>💳 Billing & Subscription</h1>
        <p>Manage your subscription and view usage</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Get current subscription
    subscription = subscription_manager.get_organization_subscription(org_code)
    current_plan = subscription.get('plan', 'basic')
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["📊 Current Plan", "🚀 Upgrade Options", "📈 Usage History"])
    
    with tab1:
        show_current_plan(subscription_manager, org_code, current_plan)
    
    with tab2:
        show_upgrade_options(subscription_manager, org_code, current_plan)
    
    with tab3:
        show_usage_history(subscription_manager, org_code)

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
