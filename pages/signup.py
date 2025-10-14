import streamlit as st
from datetime import datetime
from services.subscription_config import SUBSCRIPTION_PLANS

def show():
    """Display signup page with plan selection"""
    
    st.markdown("""
    <div class="main-header">
        <h1>⚖️ Welcome to LegalDoc Pro</h1>
        <p>Choose your plan and start managing your legal practice today</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if user already selected a plan
    if 'selected_plan' not in st.session_state:
        show_plan_selection()
    else:
        show_signup_form()

def show_plan_selection():
    """Display plan selection cards"""
    
    st.markdown("### 🚀 Choose Your Plan")
    st.markdown("Select the plan that best fits your practice needs")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Create 3 columns for plans
    col1, col2, col3 = st.columns(3)
    
    plans = ['basic', 'professional', 'enterprise']
    columns = [col1, col2, col3]
    
    plan_colors = {
        'basic': '#6c757d',
        'professional': '#007bff',
        'enterprise': '#28a745'
    }
    
    plan_badges = {
        'basic': '📦 Starter',
        'professional': '⭐ Most Popular',
        'enterprise': '👑 Premium'
    }
    
    for plan_name, col in zip(plans, columns):
        plan_details = SUBSCRIPTION_PLANS[plan_name]
        
        with col:
            # Highlight professional plan
            is_popular = (plan_name == 'professional')
            border_style = "3px solid #007bff" if is_popular else "2px solid #dee2e6"
            
            st.markdown(f"""
            <div style="
                border: {border_style};
                border-radius: 20px;
                padding: 2rem;
                background: white;
                height: 100%;
                position: relative;
                box-shadow: {'0 8px 30px rgba(0,123,255,0.3)' if is_popular else '0 4px 15px rgba(0,0,0,0.1)'};
                transform: {'scale(1.05)' if is_popular else 'scale(1)'};
            ">
                {f'<div style="position: absolute; top: -15px; left: 50%; transform: translateX(-50%); background: {plan_colors[plan_name]}; color: white; padding: 8px 20px; border-radius: 20px; font-weight: bold; font-size: 0.85rem;">{plan_badges[plan_name]}</div>' if plan_name in plan_badges else ''}
                
                <div style="text-align: center; margin-top: {'20px' if plan_name in plan_badges else '0'};">
                    <h3 style="color: {plan_colors[plan_name]}; margin-bottom: 1rem;">{plan_details['name']}</h3>
                    <h1 style="color: #2E86AB; margin: 1rem 0;">
                        ${plan_details['price']}
                        <span style="font-size: 1rem; color: #666;">/month</span>
                    </h1>
                    <p style="color: #666; min-height: 60px; font-size: 0.9rem;">{plan_details['description']}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Feature list
            st.markdown("**✨ Features:**")
            
            key_features = get_plan_key_features(plan_name, plan_details)
            
            for feature in key_features:
                st.markdown(f"✅ {feature}")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Select button
            button_type = "primary" if is_popular else "secondary"
            if st.button(
                f"Select {plan_details['name']}", 
                key=f"select_{plan_name}",
                use_container_width=True,
                type=button_type
            ):
                st.session_state.selected_plan = plan_name
                st.rerun()
    
    # Comparison link
    st.markdown("---")
    st.markdown("### 📊 Compare All Features")
    
    if st.button("View Detailed Feature Comparison", use_container_width=True):
        show_feature_comparison()

def get_plan_key_features(plan_name, plan_details):
    """Get key features to display for each plan"""
    
    if plan_name == 'basic':
        return [
            f"{plan_details['limits']['max_matters']} active matters",
            f"{plan_details['limits']['max_documents']} documents",
            f"{plan_details['limits']['max_users']} team members",
            "Document management",
            "Time & billing",
            "Client portal",
            "Email support"
        ]
    elif plan_name == 'professional':
        return [
            f"{plan_details['limits']['max_matters']} active matters",
            f"{plan_details['limits']['max_documents']} documents",
            f"{plan_details['limits']['max_users']} team members",
            "Everything in Basic +",
            f"🤖 {plan_details['limits']['case_comparisons_per_month']} AI case comparisons/mo",
            f"🤖 {plan_details['limits']['ai_insights_per_month']} AI insights/mo",
            "Business intelligence",
            "Priority support"
        ]
    else:  # enterprise
        return [
            "♾️ Unlimited everything",
            "♾️ Unlimited AI features",
            "Everything in Professional +",
            "API access",
            "Custom integrations",
            "White label options",
            "24/7 dedicated support",
            "Account manager"
        ]

def show_feature_comparison():
    """Show detailed feature comparison table"""
    
    st.markdown("### 📊 Detailed Feature Comparison")
    
    comparison_data = {
        'Feature': [
            'Active Matters',
            'Documents',
            'Team Members',
            'Storage',
            'Document Management',
            'Matter Management',
            'Time & Billing',
            'Calendar & Tasks',
            'Client Portal',
            'AI Case Comparison',
            'AI Insights',
            'Advanced Search',
            'Business Intelligence',
            'Integrations',
            'Mobile App',
            'API Access',
            'White Label',
            'Support'
        ],
        'Basic': [
            '50', '500', '3', '10 GB',
            '✅', '✅', '✅', '✅', '✅',
            '❌', '❌', '❌', '❌',
            '❌', '❌', '❌', '❌',
            'Email (48h)'
        ],
        'Professional': [
            '200', '5,000', '10', '100 GB',
            '✅', '✅', '✅', '✅', '✅',
            '25/month', '50/month', '100/month', '✅',
            '✅', '✅', '❌', '❌',
            'Priority (24h)'
        ],
        'Enterprise': [
            'Unlimited', 'Unlimited', 'Unlimited', 'Unlimited',
            '✅', '✅', '✅', '✅', '✅',
            'Unlimited', 'Unlimited', 'Unlimited', '✅',
            '✅', '✅', '✅', '✅',
            '24/7 + Manager'
        ]
    }
    
    import pandas as pd
    df = pd.DataFrame(comparison_data)
    
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    if st.button("← Back to Plan Selection"):
        st.rerun()

def show_signup_form():
    """Show signup form after plan selection"""
    
    selected_plan = st.session_state.selected_plan
    plan_details = SUBSCRIPTION_PLANS[selected_plan]
    
    # Show selected plan at top
    plan_colors = {
        'basic': '#6c757d',
        'professional': '#007bff',
        'enterprise': '#28a745'
    }
    
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, {plan_colors[selected_plan]}, {plan_colors[selected_plan]}dd);
        color: white;
        padding: 1.5rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        text-align: center;
    ">
        <h3 style="margin: 0;">Selected Plan: {plan_details['name']}</h3>
        <h2 style="margin: 0.5rem 0;">${plan_details['price']}/month</h2>
        <p style="margin: 0; opacity: 0.9; font-size: 0.9rem;">
            <a href="#" style="color: white; text-decoration: underline;" onclick="return false;">Change Plan</a>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("← Change Plan", key="change_plan"):
        del st.session_state.selected_plan
        st.rerun()
    
    st.markdown("### 📝 Create Your Account")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Personal Information**")
        first_name = st.text_input("First Name *", placeholder="John")
        last_name = st.text_input("Last Name *", placeholder="Doe")
        email = st.text_input("Email *", placeholder="john@lawfirm.com")
        phone = st.text_input("Phone", placeholder="(555) 123-4567")
    
    with col2:
        st.markdown("**Organization Information**")
        org_name = st.text_input("Firm/Organization Name *", placeholder="Smith & Associates")
        org_size = st.selectbox("Organization Size", [
            "Solo Practitioner",
            "2-5 attorneys",
            "6-10 attorneys",
            "11-25 attorneys",
            "25+ attorneys"
        ])
        practice_area = st.multiselect("Practice Areas", [
            "Corporate Law",
            "Family Law",
            "Criminal Defense",
            "Personal Injury",
            "Real Estate",
            "Intellectual Property",
            "Employment Law",
            "Tax Law",
            "Estate Planning",
            "Other"
        ])
    
    st.markdown("---")
    st.markdown("**Security**")
    
    col_pass1, col_pass2 = st.columns(2)
    
    with col_pass1:
        password = st.text_input("Password *", type="password", placeholder="Minimum 8 characters")
    
    with col_pass2:
        confirm_password = st.text_input("Confirm Password *", type="password")
    
    st.markdown("---")
    
    # Terms and conditions
    agree_terms = st.checkbox("I agree to the Terms of Service and Privacy Policy *")
    marketing_emails = st.checkbox("Send me updates and marketing emails", value=True)
    
    st.markdown("---")
    
    # Payment information (for paid plans)
    if selected_plan != 'free':
        st.markdown("### 💳 Payment Information")
        st.info("💡 14-day free trial - No credit card required! You can add payment information later.")
        
        # Uncomment below for actual payment collection
        # col_card1, col_card2 = st.columns(2)
        # with col_card1:
        #     card_number = st.text_input("Card Number", placeholder="1234 5678 9012 3456")
        #     card_name = st.text_input("Name on Card", placeholder="John Doe")
        # with col_card2:
        #     col_exp1, col_exp2, col_cvv = st.columns(3)
        #     with col_exp1:
        #         exp_month = st.selectbox("Month", list(range(1, 13)))
        #     with col_exp2:
        #         exp_year = st.selectbox("Year", list(range(2025, 2036)))
        #     with col_cvv:
        #         cvv = st.text_input("CVV", placeholder="123", max_chars=4)
    
    st.markdown("---")
    
    # Summary
    col_summary1, col_summary2 = st.columns([2, 1])
    
    with col_summary1:
        st.markdown("**Order Summary**")
        st.write(f"Plan: {plan_details['name']}")
        st.write(f"Billing: {plan_details['billing_cycle'].title()}")
        if selected_plan != 'free':
            st.write("First 14 days: **FREE**")
            st.write(f"After trial: ${plan_details['price']}/month")
    
    with col_summary2:
        st.markdown("**Today's Charge**")
        st.markdown(f"<h2 style='color: #28a745; margin: 0;'>$0.00</h2>", unsafe_allow_html=True)
        st.caption("Free trial - 14 days")
    
    st.markdown("---")
    
    # Submit button
    col_submit1, col_submit2, col_submit3 = st.columns([1, 2, 1])
    
    with col_submit2:
        if st.button("🚀 Start Free Trial", type="primary", use_container_width=True):
            # Validation
            errors = []
            
            if not first_name or not last_name:
                errors.append("Please enter your full name")
            
            if not email or '@' not in email:
                errors.append("Please enter a valid email address")
            
            if not org_name:
                errors.append("Please enter your organization name")
            
            if not password or len(password) < 8:
                errors.append("Password must be at least 8 characters")
            
            if password != confirm_password:
                errors.append("Passwords do not match")
            
            if not agree_terms:
                errors.append("You must agree to the Terms of Service")
            
            if errors:
                for error in errors:
                    st.error(error)
            else:
                # Create account
                create_account(
                    first_name, last_name, email, phone,
                    org_name, org_size, practice_area,
                    password, selected_plan
                )

def create_account(first_name, last_name, email, phone, org_name, org_size, practice_area, password, selected_plan):
    """Create new user account"""
    
    # Generate organization code
    import random
    import string
    org_code = 'ORG' + ''.join(random.choices(string.digits, k=6))
    
    # Create user data
    user_data = {
        'name': f"{first_name} {last_name}",
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'phone': phone,
        'organization_code': org_code,
        'organization_name': org_name,
        'organization_size': org_size,
        'practice_areas': practice_area,
        'is_subscription_owner': True,
        'created_at': datetime.now().isoformat(),
        'trial_end_date': (datetime.now() + timedelta(days=14)).isoformat()
    }
    
    # Create subscription
    subscription_data = {
        'plan': selected_plan,
        'status': 'trial',
        'start_date': datetime.now().isoformat(),
        'trial_end_date': (datetime.now() + timedelta(days=14)).isoformat(),
        'billing_cycle': 'monthly'
    }
    
    # Store in session state (in production, save to database)
    if 'users' not in st.session_state:
        st.session_state.users = {}
    
    if 'subscriptions' not in st.session_state:
        st.session_state.subscriptions = {}
    
    st.session_state.users[email] = {
        'password': password,  # In production, hash this!
        'data': user_data
    }
    
    st.session_state.subscriptions[org_code] = subscription_data
    
    # Log the user in
    st.session_state.logged_in = True
    st.session_state.user_data = user_data
    st.session_state.current_page = 'Executive Dashboard'
    
    # Show success and redirect
    st.success(f"✅ Account created successfully! Welcome to LegalDoc Pro, {first_name}!")
    st.balloons()
    
    # Small delay then redirect
    import time
    time.sleep(2)
    st.rerun()
