import streamlit as st
import pandas as pd

def show():
    """Display the case comparison page"""
    
    def show():
    """Display the case comparison page"""
    
    # Get user's organization - provide fallback
    user_data = st.session_state.get('user_data', {})
    user_email = user_data.get('email', 'demo@example.com')
    org_code = user_data.get('organization_code', user_email)
    
    # If no user data at all, create a default one
    if not user_data:
        st.session_state.user_data = {
            'email': 'demo@example.com',
            'name': 'Demo User',
            'organization_code': 'demo_org'
        }
        user_data = st.session_state.user_data
        org_code = 'demo_org'
    
    # Import subscription manager - make it optional
    try:
        from services.subscription_manager import SubscriptionManager
        subscription_manager = SubscriptionManager()
        has_subscription = True
    except Exception as e:
        # If subscription service unavailable, continue without it
        subscription_manager = None
        has_subscription = False
        st.warning("⚠️ Running in demo mode - subscription features disabled")
    
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
        <h1>🔍 AI Case Comparison</h1>
        <p>AI-powered case analysis and similarity detection</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Get subscription details - handle case where subscription manager doesn't exist
    if has_subscription and subscription_manager:
        subscription = subscription_manager.get_organization_subscription(org_code)
        plan_name = subscription.get('plan', 'basic')
        
        # Enterprise users always have access
        if plan_name == 'enterprise':
            can_use = True
            status = "Unlimited ✨"
        else:
            can_use, status = subscription_manager.can_use_feature_with_limit(org_code, 'case_comparison')
    else:
        # Demo mode - allow unlimited access
        plan_name = 'demo'
        can_use = True
        status = "Demo Mode"
        
    # Show usage status
    col_status1, col_status2, col_status3 = st.columns(3)
    
    with col_status1:
        st.metric("Plan", plan_name.title())
    
    with col_status2:
        if has_subscription and subscription_manager:
            if plan_name == 'professional':
                usage = subscription_manager.get_feature_usage(org_code, 'case_comparison')
                limit = subscription_manager.get_feature_limit(org_code, 'case_comparison')
                st.metric("Usage This Month", f"{usage}/{limit}")
            elif plan_name == 'enterprise':
                st.metric("Usage", "Unlimited ✨")
            else:
                st.metric("Usage", "Not Available")
        else:
            st.metric("Usage", "Demo - Unlimited")
    
    with col_status3:
        if not can_use and plan_name == 'basic':
            st.warning("⚠️ Upgrade Required")
        elif not can_use:
            st.error("❌ Limit Reached")
        else:
            st.success("✅ Available")
    
    # If feature not available, show upgrade prompt
    if not can_use:
        show_upgrade_prompt(plan_name, status)
        return
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["🆕 New Case Analysis", "📊 Bulk Comparison", "📈 Similarity Matrix"])
    
    with tab1:
        show_new_case_comparison(subscription_manager, org_code, plan_name)
    
    with tab2:
        show_bulk_comparison()
    
    with tab3:
        show_similarity_matrix()

def show_upgrade_prompt(current_plan, status):
    """Show upgrade prompt when feature is not available"""
    
    st.markdown("---")
    
    if current_plan == 'basic':
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 3rem;
            border-radius: 20px;
            text-align: center;
        ">
            <h2>🚀 Unlock AI-Powered Case Comparison</h2>
            <p style="font-size: 1.2rem; margin: 1rem 0;">
                Upgrade to Professional or Enterprise to access advanced AI features
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### What You'll Get:")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Professional Plan - $149/month**
            - ✅ 25 AI case comparisons per month
            - ✅ 50 AI insights per month
            - ✅ 100 advanced searches per month
            - ✅ Business intelligence dashboard
            - ✅ Priority support
            """)
        
        with col2:
            st.markdown("""
            **Enterprise Plan - $499/month**
            - ✅ Unlimited AI case comparisons
            - ✅ Unlimited AI insights
            - ✅ Unlimited advanced searches
            - ✅ Custom integrations
            - ✅ 24/7 dedicated support
            - ✅ API access
            """)
        
        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            if st.button("💳 Upgrade to Professional", type="primary", use_container_width=True):
                st.session_state['current_page'] = 'Billing Management'
                st.rerun()
    
    else:  # Professional plan, limit reached
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 2rem;
            border-radius: 20px;
            text-align: center;
        ">
            <h2>⚠️ Monthly Limit Reached</h2>
            <p style="font-size: 1.1rem;">
                You've used all your case comparisons for this month
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### Options:")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.info("""
            **Wait for Next Month**
            
            Your usage limit will reset on the 1st of next month.
            """)
        
        with col2:
            st.success("""
            **Upgrade to Enterprise**
            
            Get unlimited AI features for $499/month
            """)
        
        if st.button("🚀 Upgrade to Enterprise for Unlimited Access", type="primary"):
            st.session_state['current_page'] = 'Billing Management'
            st.rerun()

def show_new_case_comparison(subscription_manager, org_code, plan_name):
    """Show new case comparison interface with usage tracking"""
    
    st.subheader("Compare New Case with Historical Cases")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📝 New Case Details")
        
        new_case = {
            'id': st.text_input("Case ID", value=f"CASE-{pd.Timestamp.now().strftime('%Y%m%d-%H%M')}"),
            'title': st.text_input("Case Title", placeholder="e.g., Smith vs. Johnson Employment Dispute"),
            'type': st.selectbox("Case Type", [
                "Contract Dispute",
                "Employment Law",
                "Intellectual Property",
                "Corporate Law",
                "Real Estate",
                "Personal Injury",
                "Family Law",
                "Criminal Defense",
                "Tax Law",
                "Other"
            ]),
            'client': st.text_input("Client Name", placeholder="Client or Company Name"),
            'description': st.text_area("Case Description", 
                placeholder="Provide a detailed description of the case...",
                height=150),
            'key_facts': st.text_area("Key Facts", 
                placeholder="List the most important facts of the case...",
                height=100),
            'legal_issues': st.text_area("Legal Issues", 
                placeholder="What are the primary legal questions or issues?",
                height=100)
        }
    
    with col2:
        st.markdown("### 📚 Select Previous Cases to Compare")
        
        # Get previous cases from session state
        all_matters = st.session_state.get('matters', [])
        
        if not all_matters:
            st.warning("No previous cases found. Please add some matters first.")
            if st.button("➕ Go to Matter Management"):
                st.session_state['current_page'] = 'Matter Management'
                st.rerun()
            return
        
        # Display available cases
        st.write(f"**Available Cases:** {len(all_matters)}")
        
        # Convert matters to dict format if they're objects
        matter_titles = []
        for m in all_matters:
            if hasattr(m, 'name'):
                matter_titles.append(m.name)
            elif isinstance(m, dict):
                matter_titles.append(m.get('name', m.get('title', 'Unknown')))
        
        # Multi-select for case selection
        selected_case_titles = st.multiselect(
            "Select cases to compare",
            options=matter_titles,
            default=matter_titles[:min(5, len(matter_titles))]
        )
        
        # Filter selected cases
        selected_cases = []
        for m in all_matters:
            if hasattr(m, 'name'):
                if m.name in selected_case_titles:
                    selected_cases.append(m)
            elif isinstance(m, dict):
                title = m.get('name', m.get('title', 'Unknown'))
                if title in selected_case_titles:
                    selected_cases.append(m)
        
        st.info(f"Selected {len(selected_cases)} cases for comparison")
    
    # Comparison button
    st.markdown("---")
    
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
    
    with col_btn2:
        if st.button("🔍 Analyze & Compare Cases", type="primary", use_container_width=True):
            if not new_case['title'] or not new_case['description']:
                st.error("Please fill in at least the case title and description.")
                return
            
            if not selected_cases:
                st.error("Please select at least one previous case to compare.")
                return
            
            # Mock analysis for demo
            with st.spinner("🤖 AI is analyzing cases... This may take 30-60 seconds..."):
                import time
                time.sleep(2)
                
                # Increment usage counter ONLY for non-enterprise users and when subscription exists
                if has_subscription and subscription_manager and plan_name != 'enterprise':
                    subscription_manager.increment_feature_usage(org_code, 'case_comparison')
            
            st.success("✅ Analysis complete!")
            
            # Show updated usage (only for non-enterprise)
            if has_subscription and subscription_manager:
                if plan_name == 'professional':
                    usage = subscription_manager.get_feature_usage(org_code, 'case_comparison')
                    limit = subscription_manager.get_feature_limit(org_code, 'case_comparison')
                    remaining = limit - usage
                    if remaining > 0:
                        st.info(f"📊 You have {remaining} comparisons remaining this month")
                    else:
                        st.warning("⚠️ You've reached your monthly limit")
                elif plan_name == 'enterprise':
                    st.success("✨ Unlimited comparisons available")
            else:
                st.success("✨ Demo mode - Unlimited comparisons")
            
            # Display mock results
            st.markdown("---")
            st.markdown("## 📊 Comparison Results")
            
            with st.expander("📄 Complete Analysis", expanded=True):
                st.markdown(f"""
                ### AI-Powered Case Analysis
                
                Based on analysis of **{len(selected_cases)}** historical cases, here are the findings:
                
                **Overall Similarity Score:** 78%
                
                The new case "{new_case['title']}" ({new_case['type']}) shows strong similarities to previous cases 
                in your database. Key legal precedents and strategies from similar cases can be applied here.
                
                **Key Findings:**
                - Similar fact patterns identified in 3 previous cases
                - Relevant legal precedents: Johnson v. State (2023), Smith Corp. v. Doe (2022)
                - Estimated case duration: 6-9 months
                - Recommended strategy: Focus on settlement negotiations
                """)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 🎯 Most Similar Cases")
                for i, case in enumerate(selected_cases[:3], 1):
                    similarity = 85 - (i * 5)
                    
                    # Handle both object and dict formats
                    if hasattr(case, 'name'):
                        case_title = case.name
                        case_type = getattr(case, 'matter_type', 'N/A')
                        case_status = getattr(case, 'status', 'N/A')
                        case_attorney = getattr(case, 'assigned_attorneys', ['N/A'])[0] if hasattr(case, 'assigned_attorneys') and case.assigned_attorneys else 'N/A'
                    else:
                        case_title = case.get('name', case.get('title', 'Unknown'))
                        case_type = case.get('type', case.get('matter_type', 'N/A'))
                        case_status = case.get('status', 'N/A')
                        case_attorney = case.get('lead_attorney', 'N/A')
                    
                    st.markdown(f"""
                    **{i}. {case_title}** ({similarity}% similar)
                    - Type: {case_type}
                    - Status: {case_status}
                    - Lead: {case_attorney}
                    """)
            
            with col2:
                st.markdown("### 💡 Strategic Recommendations")
                st.markdown("""
                1. **Review precedents** from similar cases
                2. **Consider ADR** - Alternative dispute resolution may be beneficial
                3. **Document everything** - Maintain detailed case records
                4. **Early settlement** - Explore settlement options early
                5. **Expert witnesses** - Consider expert testimony for technical issues
                """)
            
            # Download report
            st.markdown("---")
            report_text = f"""CASE COMPARISON REPORT
Generated: {pd.Timestamp.now()}

NEW CASE:
Title: {new_case['title']}
Type: {new_case['type']}
Client: {new_case['client']}

DESCRIPTION:
{new_case['description']}

ANALYSIS:
Compared with {len(selected_cases)} historical cases
Overall similarity: 78%

SIMILAR CASES:
{chr(10).join([f"- {c.name if hasattr(c, 'name') else c.get('name', c.get('title', 'Unknown'))}" for c in selected_cases[:3]])}

RECOMMENDATIONS:
- Review precedents from similar cases
- Consider alternative dispute resolution
- Maintain detailed documentation
- Explore early settlement options
"""
            
            st.download_button(
                label="📥 Download Full Report",
                data=report_text,
                file_name=f"case_comparison_{new_case['id']}.txt",
                mime="text/plain"
            )

def show_bulk_comparison():
    """Show bulk comparison interface"""
    st.subheader("Bulk Case Comparison")
    st.info("⚠️ Feature coming soon - Each comparison will count toward your monthly limit")
    
    st.markdown("""
    ### 📋 Bulk Comparison Features:
    - Upload multiple cases at once via CSV/Excel
    - Compare against entire case database
    - Generate comprehensive similarity reports
    - Export results to Excel/CSV
    - Batch processing for efficiency
    """)
    
    # Mock upload interface
    uploaded_file = st.file_uploader("Upload case data (CSV or Excel)", type=['csv', 'xlsx'])
    
    if uploaded_file:
        st.success("File uploaded! Feature coming soon.")

def show_similarity_matrix():
    """Show similarity matrix visualization"""
    st.subheader("Case Similarity Matrix")
    st.info("⚠️ Feature coming soon - Matrix generation will count toward your monthly limit")
    
    st.markdown("""
    ### 📊 Similarity Matrix Features:
    - Visual heatmap of case similarities
    - Interactive clustering analysis
    - Pattern identification across cases
    - Export visualizations as images
    - Drill-down into specific case pairs
    """)
    
    # Mock visualization
    st.image("https://via.placeholder.com/800x400/1e3a8a/ffffff?text=Similarity+Matrix+Visualization+Coming+Soon", 
             use_container_width=True)

if __name__ == "__main__":
    show()
