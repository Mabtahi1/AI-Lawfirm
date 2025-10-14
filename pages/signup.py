import streamlit as st
from datetime import datetime, timedelta
from services.subscription_config import SUBSCRIPTION_PLANS
from services.email_service import EmailService, AuthTokenManager

def show():
    """Display signup page with plan selection"""
    
    # Match main app styling
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
    }
    
    /* Light text everywhere */
    * {
        color: #e2e8f0 !important;
    }
    
    h1, h2, h3 {
        color: #f1f5f9 !important;
    }
    
    /* Dark text in input fields */
    input, textarea, select {
        color: #1e293b !important;
        background: white !important;
    }
    
    /* Plan cards */
    .plan-card {
        background: rgba(30, 41, 59, 0.8);
        backdrop-filter: blur(10px);
        border: 2px solid rgba(59, 130, 246, 0.3);
        border-radius: 16px;
        padding: 2rem;
        transition: all 0.3s ease;
    }
    
    .plan-card:hover {
        transform: translateY(-5px);
        border-color: #3b82f6;
        box-shadow: 0 8px 30px rgba(59, 130, 246, 0.4);
    }
    
    .plan-popular {
        border: 3px solid #3b82f6 !important;
        box-shadow: 0 8px 30px rgba(59, 130, 246, 0.5);
        transform: scale(1.05);
    }
    
    .plan-badge {
        background: #3b82f6;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Check if user already selected a plan
    if 'selected_plan' not in st.session_state:
        show_plan_selection()
    else:
        show_signup_form()

def show_plan_selection():
    """Display plan selection cards"""
    
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1 style="font-size: 3rem; margin-bottom: 0.5rem;">⚖️ Welcome to LegalDoc Pro</h1>
        <p style="font-size: 1.3rem; opacity: 0.9;">Choose your plan and start managing your legal practice today</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("### 🚀 Choose Your Plan")
    st.write("Select the plan that best fits your practice needs")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Create 3 columns for plans
    col1, col2, col3 = st.columns(3)
    
    plans = ['basic', 'professional', 'enterprise']
    columns = [col1, col2, col3]
    
    plan_badges = {
        'basic': '📦 Starter',
        'professional': '⭐ Most Popular',
        'enterprise': '👑 Premium'
    }
    
    for plan_name, col in zip(plans, columns):
        plan_details = SUBSCRIPTION_PLANS[plan_name]
        is_popular = (plan_name == 'professional')
        
        with col:
            # Plan card with conditional styling
            card_class = "plan-card plan-popular" if is_popular else "plan-card"
            
            with st.container():
                # Badge
                if plan_name in plan_badges:
                    st.markdown(f"""
                    <div style="text-align: center;">
                        <span class="plan-badge">{plan_badges[plan_name]}</span>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Plan name and price
                st.markdown(f"""
                <div style="text-align: center; padding: 1rem 0;">
                    <h3 style="font-size: 1.5rem; margin-bottom: 0.5rem;">{plan_details['name']}</h3>
                    <h1 style="font-size: 2.5rem; color: #60a5fa;">${plan_details['price']}</h1>
                    <p style="opacity: 0.8;">per month</p>
                    <p style="font-size: 0.9rem; min-height: 60px;">{plan_details['description']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("---")
                
                # Features
                st.markdown("**✨ Features:**")
                key_features = get_plan_key_features(plan_name, plan_details)
                
                for feature in key_features[:6]:  # Show first 6 features
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
    
    with st.expander("📊 View Detailed Feature Comparison"):
        show_feature_comparison()

def get_plan_key_features(plan_name, plan_details):
    """Get key features to display for each plan"""
    
    if plan_name == 'basic':
        return [
            f"{plan_details['limits']['max_matters']} active matters",
            f"{plan_details['limits']['max_documents']} documents",
            f"{plan_details['limits']['max_users']} team members",
            f"{plan_details['limits']['storage_gb']} GB storage",
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
            f"{plan_details['limits']['storage_gb']} GB storage",
            f"🤖 {plan_details['limits']['case_comparisons_per_month']} AI comparisons/mo",
            f"🤖 {plan_details['limits']['ai_insights_per_month']} AI insights/mo",
            "Business intelligence",
            "Priority support"
        ]
    else:  # enterprise
        return [
            "♾️ Unlimited matters",
            "♾️ Unlimited documents",
            "♾️ Unlimited users",
            "♾️ Unlimited storage",
            "♾️ Unlimited AI features",
            "API access",
            "Custom integrations",
            "24/7 dedicated support"
        ]

def show_feature_comparison():
    """Show detailed feature comparison table"""
    
    import pandas as pd
    
    comparison_data = {
        'Feature': [
            'Active Matters',
            'Documents',
            'Team Members',
            'Storage',
            'AI Case Comparison',
            'AI Insights',
            'Advanced Search',
            'Business Intelligence',
            'Mobile App',
            'API Access',
            'Support'
        ],
        'Basic': [
            '50', '500', '3', '10 GB',
            '❌', '❌', '❌', '❌',
            '❌', '❌', 'Email (48h)'
        ],
        'Professional': [
            '200', '5,000', '10', '100 GB',
            '25/month', '50/month', '100/month', '✅',
            '✅', '❌', 'Priority (24h)'
        ],
        'Enterprise': [
            'Unlimited', 'Unlimited', 'Unlimited', 'Unlimited',
            'Unlimited', 'Unlimited', 'Unlimited', '✅',
            '✅', '✅', '24/7 + Manager'
        ]
    }
    
    df = pd.DataFrame(comparison_data)
    st.dataframe(df, use_container_width=True, hide_index=True)

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
        <h3 style="margin: 0; color: white !important;">Selected Plan: {plan_details['name']}</h3>
        <h2 style="margin: 0.5rem 0; color: white !important;">${plan_details['price']}/month</h2>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("← Change Plan", key="change_plan"):
        del st.session_state.selected_plan
        st.rerun()
    
    st.markdown("### 📝 Create Your Account")
    
    with st.form("signup_form"):
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
        
        # Payment info note
        if selected_plan != 'free':
            st.info("💡 14-day free trial - No credit card required! You can add payment information later.")
        
        # Submit button
        submitted = st.form_submit_button("🚀 Start Free Trial", use_container_width=True, type="primary")
        
        if submitted:
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
        'trial_end_date': (datetime.now() + timedelta(days=14)).isoformat(),
        'email_verified': True  # Auto-verify for now
    }
    
    # Create subscription
    subscription_data = {
        'plan': selected_plan,
        'status': 'trial',
        'start_date': datetime.now().isoformat(),
        'trial_end_date': (datetime.now() + timedelta(days=14)).isoformat(),
        'billing_cycle': 'monthly'
    }
    
    # Store in session state
    if 'users' not in st.session_state:
        st.session_state.users = {}
    
    if 'subscriptions' not in st.session_state:
        st.session_state.subscriptions = {}
    
    # Hash password
    hashed_password = AuthTokenManager.hash_password(password)
    
    st.session_state.users[email] = {
        'password': hashed_password,
        'data': user_data
    }
    
    st.session_state.subscriptions[org_code] = subscription_data
    
    # Log the user in immediately
    st.session_state.logged_in = True
    st.session_state.user_data = user_data
    st.session_state.current_page = 'Executive Dashboard'
    
    # Show success and redirect
    st.success(f"✅ Account created successfully! Welcome to LegalDoc Pro, {first_name}!")
    st.balloons()
    
    # Clean up
    if 'selected_plan' in st.session_state:
        del st.session_state.selected_plan
    
    # Redirect
    import time
    time.sleep(2)
    st.rerun()
