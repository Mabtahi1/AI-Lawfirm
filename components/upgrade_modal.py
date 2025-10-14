import streamlit as st
from services.subscription_config import SUBSCRIPTION_PLANS

def show_upgrade_modal(current_plan, feature_name, feature_display_name):
    """Show upgrade modal when user clicks locked feature"""
    
    st.markdown(f"""
    <div style="
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0,0,0,0.7);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 9999;
    ">
        <div style="
            background: white;
            padding: 3rem;
            border-radius: 20px;
            max-width: 800px;
            width: 90%;
            max-height: 90vh;
            overflow-y: auto;
        ">
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 style="color: #2E86AB;">🔓 Unlock {feature_display_name}</h1>
        <p style="font-size: 1.2rem; color: #666;">
            Upgrade your plan to access this premium feature
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Show feature benefits
    feature_benefits = {
        'case_comparison': {
            'icon': '🔍',
            'benefits': [
                'AI-powered case analysis',
                'Compare with historical cases',
                'Find similarities and differences',
                'Get strategic recommendations',
                'Predict case outcomes'
            ]
        },
        'ai_insights': {
            'icon': '🤖',
            'benefits': [
                'AI document analysis',
                'Automated summarization',
                'Key points extraction',
                'Risk assessment',
                'Smart recommendations'
            ]
        },
        'advanced_search': {
            'icon': '🔎',
            'benefits': [
                'Semantic search across all documents',
                'Natural language queries',
                'Advanced filters',
                'Search history',
                'Saved searches'
            ]
        },
        'business_intelligence': {
            'icon': '📊',
            'benefits': [
                'Advanced analytics dashboards',
                'Custom reports',
                'Revenue forecasting',
                'Performance metrics',
                'Data export'
            ]
        }
    }
    
    feature_info = feature_benefits.get(feature_name, {
        'icon': '✨',
        'benefits': ['Premium feature access']
    })
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown(f"### {feature_info['icon']} What You'll Get:")
        for benefit in feature_info['benefits']:
            st.markdown(f"✅ {benefit}")
    
    with col2:
        st.markdown("### 💎 Recommended Plan:")
        
        if current_plan == 'basic':
            # Recommend Professional
            plan_details = SUBSCRIPTION_PLANS['professional']
            
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
                color: white;
                padding: 2rem;
                border-radius: 16px;
                text-align: center;
            ">
                <h2>{plan_details['name']}</h2>
                <h1>${plan_details['price']}/month</h1>
                <p>Get {plan_details['limits']['case_comparisons_per_month']} AI comparisons per month</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("🚀 Upgrade to Professional", type="primary", use_container_width=True, key="upgrade_to_pro"):
                st.session_state['upgrade_to_plan'] = 'professional'
                st.session_state['current_page'] = 'Billing Management'
                st.rerun()
        
        elif current_plan == 'professional':
            # Recommend Enterprise
            plan_details = SUBSCRIPTION_PLANS['enterprise']
            
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
                color: white;
                padding: 2rem;
                border-radius: 16px;
                text-align: center;
            ">
                <h2>{plan_details['name']}</h2>
                <h1>${plan_details['price']}/month</h1>
                <p>Unlimited AI features + Premium support</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("🚀 Upgrade to Enterprise", type="primary", use_container_width=True, key="upgrade_to_ent"):
                st.session_state['upgrade_to_plan'] = 'enterprise'
                st.session_state['current_page'] = 'Billing Management'
                st.rerun()
    
    st.markdown("---")
    
    # Comparison table
    st.markdown("### 📊 Plan Comparison")
    
    comparison_df = {
        'Feature': [feature_display_name, 'Monthly Usage', 'Support', 'Price'],
        'Basic (Current)' if current_plan == 'basic' else 'Basic': [
            '❌ Not Available',
            '-',
            'Email (48h)',
            '$49/mo'
        ],
        'Professional' + (' (Current)' if current_plan == 'professional' else ''): [
            '✅ Available',
            '25/month',
            'Priority (24h)',
            '$149/mo'
        ],
        'Enterprise': [
            '✅ Available',
            'Unlimited',
            '24/7 + Manager',
            '$499/mo'
        ]
    }
    
    import pandas as pd
    df = pd.DataFrame(comparison_df)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    col_btn1, col_btn2 = st.columns(2)
    
    with col_btn1:
        if st.button("📋 View All Plans", use_container_width=True):
            st.session_state['current_page'] = 'Billing Management'
            st.rerun()
    
    with col_btn2:
        if st.button("❌ Close", use_container_width=True):
            if 'show_upgrade_modal' in st.session_state:
                del st.session_state['show_upgrade_modal']
            st.rerun()
    
    st.markdown("</div></div>", unsafe_allow_html=True)

def trigger_upgrade_modal(feature_name, feature_display_name):
    """Trigger the upgrade modal"""
    st.session_state['show_upgrade_modal'] = {
        'feature_name': feature_name,
        'feature_display_name': feature_display_name
    }
