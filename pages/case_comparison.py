import streamlit as st
import pandas as pd

def show():
    """Display the case comparison page"""
    # FIRST LINE - Test if function is called at all
    st.write("🧪 DEBUG: show() function was called!")
    st.write("🧪 Session state keys:", list(st.session_state.keys()))
    # Try to import services with error handling
    try:
        from services.case_comparison import CaseComparisonService
        from services.subscription_manager import SubscriptionManager
    except ImportError as e:
        st.error(f"❌ Missing required services: {e}")
        st.info("Please ensure the following files exist:")
        st.code("""
services/
├── case_comparison.py (with CaseComparisonService class)
└── subscription_manager.py (with SubscriptionManager class)
        """)
        
        if st.button("🏠 Return to Dashboard"):
            st.session_state['current_page'] = 'Executive Dashboard'
            st.rerun()
        return
    except Exception as e:
        st.error(f"❌ Error loading services: {e}")
        return
    
    # Initialize services
    try:
        comparison_service = CaseComparisonService()
        subscription_manager = SubscriptionManager()
    except Exception as e:
        st.error(f"❌ Error initializing services: {e}")
        return
    
    # Get user's organization
    user_data = st.session_state.get('user_data', {})
    org_code = user_data.get('organization_code')
    
    if not org_code:
        st.error("⚠️ No organization code found. Please log in again.")
        return
    
    # Check if user can access this feature
    try:
        can_use, status = subscription_manager.can_use_feature_with_limit(org_code, 'case_comparison')
    except Exception as e:
        st.error(f"❌ Error checking subscription: {e}")
        can_use = False
        status = "Error"
    
    st.markdown("""
    <div class="main-header">
        <h1>🔍 Case Comparison & Analysis</h1>
        <p>Compare new cases with historical data using AI-powered analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Show usage status
    try:
        subscription = subscription_manager.get_organization_subscription(org_code)
        plan_name = subscription.get('plan', 'basic')
    except:
        plan_name = 'basic'
        subscription = {'plan': 'basic'}
    
    col_status1, col_status2, col_status3 = st.columns(3)
    
    with col_status1:
        st.metric("Plan", plan_name.title())
    
    with col_status2:
        if plan_name == 'professional':
            try:
                usage = subscription_manager.get_feature_usage(org_code, 'case_comparison')
                limit = subscription_manager.get_feature_limit(org_code, 'case_comparison')
                st.metric("Usage This Month", f"{usage}/{limit}")
            except:
                st.metric("Usage This Month", "0/25")
        elif plan_name == 'enterprise':
            st.metric("Usage", "Unlimited ✨")
        else:
            st.metric("Usage", "Not Available")
    
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
        show_new_case_comparison(comparison_service, subscription_manager, org_code)
    
    with tab2:
        show_bulk_comparison(comparison_service, subscription_manager, org_code)
    
    with tab3:
        show_similarity_matrix(comparison_service, subscription_manager, org_code)

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

def show_new_case_comparison(comparison_service, subscription_manager, org_code):
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
        
        # Multi-select for case selection
        selected_case_titles = st.multiselect(
            "Select cases to compare",
            options=[m['title'] for m in all_matters],
            default=[m['title'] for m in all_matters[:min(5, len(all_matters))]]  # Select first 5 by default
        )
        
        # Filter selected cases
        selected_cases = [m for m in all_matters if m['title'] in selected_case_titles]
        
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
            
            # Check limit one more time before processing
            try:
                can_use, status = subscription_manager.can_use_feature_with_limit(org_code, 'case_comparison')
            except:
                st.error("Error checking subscription status")
                return
            
            if not can_use:
                st.error(f"Cannot perform comparison: {status}")
                return
            
            # Show loading
            with st.spinner("🤖 AI is analyzing cases... This may take 30-60 seconds..."):
                try:
                    # Perform comparison
                    result = comparison_service.compare_cases(new_case, selected_cases)
                    
                    # Increment usage counter
                    subscription_manager.increment_feature_usage(org_code, 'case_comparison')
                except Exception as e:
                    st.error(f"❌ Analysis error: {e}")
                    return
            
            if result.get('success'):
                st.success("✅ Analysis complete!")
                
                # Show updated usage
                try:
                    usage = subscription_manager.get_feature_usage(org_code, 'case_comparison')
                    limit = subscription_manager.get_feature_limit(org_code, 'case_comparison')
                    
                    if limit != -1:  # Not unlimited
                        remaining = limit - usage
                        if remaining > 0:
                            st.info(f"📊 You have {remaining} comparisons remaining this month")
                        else:
                            st.warning("⚠️ You've reached your monthly limit")
                except:
                    pass
                
                # Display results
                st.markdown("---")
                st.markdown("## 📊 Comparison Results")
                
                # Full analysis
                with st.expander("📄 Complete Analysis", expanded=True):
                    st.markdown(result.get('analysis', 'No analysis available'))
                
                # Similar cases
                col_results1, col_results2 = st.columns(2)
                
                with col_results1:
                    st.markdown("### 🎯 Most Similar Cases")
                    if result.get('similar_cases'):
                        for case in result['similar_cases']:
                            st.markdown(f"""
                            <div class="document-card">
                                <h4>{case.get('title', 'Untitled')}</h4>
                                <p><strong>Type:</strong> {case.get('type', 'N/A')}</p>
                                <p><strong>Case ID:</strong> {case.get('case_id', 'N/A')}</p>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.info("No highly similar cases found.")
                
                with col_results2:
                    st.markdown("### ⚠️ Key Differences")
                    if result.get('key_differences'):
                        for diff in result['key_differences']:
                            st.markdown(f"• {diff}")
                    else:
                        st.info("No significant differences identified.")
                
                # Recommendations
                st.markdown("### 💡 Strategic Recommendations")
                if result.get('recommendations'):
                    for i, rec in enumerate(result['recommendations'], 1):
                        st.markdown(f"{i}. {rec}")
                else:
                    st.info("No specific recommendations at this time.")
                
                # Download report
                st.markdown("---")
                report_text = f"""CASE COMPARISON REPORT
Generated: {pd.Timestamp.now()}

NEW CASE:
{new_case['title']}
Type: {new_case['type']}
Client: {new_case['client']}

ANALYSIS:
{result.get('analysis', 'No analysis available')}
"""
                
                st.download_button(
                    label="📥 Download Full Report",
                    data=report_text,
                    file_name=f"case_comparison_{new_case['id']}.txt",
                    mime="text/plain"
                )
            else:
                st.error(f"❌ Analysis failed: {result.get('error', 'Unknown error')}")

def show_bulk_comparison(comparison_service, subscription_manager, org_code):
    """Show bulk comparison interface"""
    st.subheader("Bulk Case Comparison")
    st.info("⚠️ Feature coming soon - Each comparison will count toward your monthly limit")
    
    st.markdown("""
    ### 📋 Bulk Comparison Features:
    - Upload multiple cases at once
    - Compare against entire case database
    - Generate comprehensive similarity report
    - Export results to Excel/CSV
    """)

def show_similarity_matrix(comparison_service, subscription_manager, org_code):
    """Show similarity matrix visualization"""
    st.subheader("Case Similarity Matrix")
    st.info("⚠️ Feature coming soon - Matrix generation will count toward your monthly limit")
    
    st.markdown("""
    ### 📊 Similarity Matrix Features:
    - Visual representation of case similarities
    - Interactive heatmap
    - Cluster analysis
    - Pattern identification
    """)
