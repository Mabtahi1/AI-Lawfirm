import streamlit as st
import pandas as pd
from services.case_comparison import CaseComparisonService

def show():
    """Display the case comparison page"""
    
    st.markdown("""
    <div class="main-header">
        <h1>🔍 Case Comparison & Analysis</h1>
        <p>Compare new cases with historical data using AI-powered analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize service
    comparison_service = CaseComparisonService()
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["🆕 New Case Analysis", "📊 Bulk Comparison", "📈 Similarity Matrix"])
    
    with tab1:
        show_new_case_comparison(comparison_service)
    
    with tab2:
        show_bulk_comparison(comparison_service)
    
    with tab3:
        show_similarity_matrix(comparison_service)

def show_new_case_comparison(comparison_service):
    """Show new case comparison interface"""
    
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
            return
        
        # Display available cases
        st.write(f"**Available Cases:** {len(all_matters)}")
        
        # Multi-select for case selection
        selected_case_titles = st.multiselect(
            "Select cases to compare",
            options=[m['title'] for m in all_matters],
            default=[m['title'] for m in all_matters[:5]]  # Select first 5 by default
        )
        
        # Filter selected cases
        selected_cases = [m for m in all_matters if m['title'] in selected_case_titles]
        
        st.info(f"Selected {len(selected_cases)} cases for comparison")
        
        # Show selected cases summary
        if selected_cases:
            with st.expander("📋 View Selected Cases"):
                for case in selected_cases:
                    st.markdown(f"**{case['title']}** - {case.get('type', 'N/A')}")
    
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
            
            # Show loading
            with st.spinner("🤖 AI is analyzing cases... This may take 30-60 seconds..."):
                # Perform comparison
                result = comparison_service.compare_cases(new_case, selected_cases)
            
            if result['success']:
                st.success("✅ Analysis complete!")
                
                # Display results
                st.markdown("---")
                st.markdown("## 📊 Comparison Results")
                
                # Full analysis
                with st.expander("📄 Complete Analysis", expanded=True):
                    st.markdown(result['analysis'])
                
                # Similar cases
                col_results1, col_results2 = st.columns(2)
                
                with col_results1:
                    st.markdown("### 🎯 Most Similar Cases")
                    if result['similar_cases']:
                        for case in result['similar_cases']:
                            st.markdown(f"""
                            <div class="document-card">
                                <h4>{case['title']}</h4>
                                <p><strong>Type:</strong> {case['type']}</p>
                                <p><strong>Case ID:</strong> {case['case_id']}</p>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.info("No highly similar cases found.")
                
                with col_results2:
                    st.markdown("### ⚠️ Key Differences")
                    if result['key_differences']:
                        for diff in result['key_differences']:
                            st.markdown(f"• {diff}")
                    else:
                        st.info("No significant differences identified.")
                
                # Recommendations
                st.markdown("### 💡 Strategic Recommendations")
                if result['recommendations']:
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
{result['analysis']}
"""
                
                st.download_button(
                    label="📥 Download Full Report",
                    data=report_text,
                    file_name=f"case_comparison_{new_case['id']}.txt",
                    mime="text/plain"
                )
            else:
                st.error(f"❌ Analysis failed: {result.get('error', 'Unknown error')}")

def show_bulk_comparison(comparison_service):
    """Show bulk comparison interface"""
    
    st.subheader("Bulk Case Comparison")
    st.info("Compare multiple cases at once to find patterns and similarities")
    
    all_matters = st.session_state.get('matters', [])
    
    if len(all_matters) < 2:
        st.warning("You need at least 2 cases for bulk comparison.")
        return
    
    # Select multiple cases
    selected_titles = st.multiselect(
        "Select cases to compare",
        options=[m['title'] for m in all_matters],
        default=[m['title'] for m in all_matters[:min(5, len(all_matters))]]
    )
    
    if st.button("🔄 Compare Selected Cases"):
        if len(selected_titles) < 2:
            st.error("Please select at least 2 cases.")
            return
        
        selected_matters = [m for m in all_matters if m['title'] in selected_titles]
        
        with st.spinner("Analyzing cases..."):
            # Create comparison matrix
            comparison_data = []
            
            for i, case1 in enumerate(selected_matters):
                for case2 in selected_matters[i+1:]:
                    score = comparison_service.quick_similarity_score(case1, case2)
                    comparison_data.append({
                        'Case 1': case1['title'],
                        'Case 2': case2['title'],
                        'Similarity Score': f"{score:.2f}",
                        'Case 1 Type': case1.get('type', 'N/A'),
                        'Case 2 Type': case2.get('type', 'N/A')
                    })
            
            if comparison_data:
                df = pd.DataFrame(comparison_data)
                st.dataframe(df, use_container_width=True)
                
                # Download results
                csv = df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Comparison Results",
                    data=csv,
                    file_name="bulk_case_comparison.csv",
                    mime="text/csv"
                )

def show_similarity_matrix(comparison_service):
    """Show similarity matrix visualization"""
    
    st.subheader("Case Similarity Matrix")
    st.info("Visual representation of how similar your cases are to each other")
    
    all_matters = st.session_state.get('matters', [])
    
    if len(all_matters) < 2:
        st.warning("You need at least 2 cases to generate a similarity matrix.")
        return
    
    # Limit to prevent too many API calls
    max_cases = st.slider("Number of cases to include", 2, min(10, len(all_matters)), 5)
    
    if st.button("Generate Similarity Matrix"):
        with st.spinner(f"Calculating similarities for {max_cases} cases..."):
            selected_matters = all_matters[:max_cases]
            
            # Create matrix
            matrix_data = []
            case_titles = [m['title'][:30] + '...' if len(m['title']) > 30 else m['title'] 
                          for m in selected_matters]
            
            for case1 in selected_matters:
                row = []
                for case2 in selected_matters:
                    if case1['id'] == case2['id']:
                        row.append(1.0)
                    else:
                        score = comparison_service.quick_similarity_score(case1, case2)
                        row.append(score)
                matrix_data.append(row)
            
            # Create DataFrame
            df_matrix = pd.DataFrame(matrix_data, columns=case_titles, index=case_titles)
            
            # Display heatmap using Streamlit
            st.write("### Similarity Heatmap")
            st.write("Values range from 0 (completely different) to 1 (nearly identical)")
            
            # Style the dataframe
            styled_df = df_matrix.style.background_gradient(cmap='RdYlGn', vmin=0, vmax=1).format("{:.2f}")
            st.dataframe(styled_df, use_container_width=True)
