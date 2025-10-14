import streamlit as st
from services.email_service import EmailService, AuthTokenManager

def show():
    """Display forgot password page"""
    
    st.markdown("""
    <div class="main-header">
        <h1>🔐 Forgot Password?</h1>
        <p>Enter your email address and we'll send you a reset link</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("forgot_password_form"):
            email = st.text_input("Email Address", placeholder="your@email.com")
            
            submitted = st.form_submit_button("Send Reset Link", use_container_width=True, type="primary")
            
            if submitted:
                if not email or '@' not in email:
                    st.error("Please enter a valid email address")
                else:
                    # Check if user exists
                    users = st.session_state.get('users', {})
                    
                    if email in users:
                        # Generate reset token
                        reset_token = AuthTokenManager.create_reset_token(email)
                        
                        # Send reset email
                        email_service = EmailService()
                        email_sent = email_service.send_password_reset_email(email, reset_token)
                        
                        if email_sent:
                            st.success(f"""
                            ✅ Password reset link sent!
                            
                            If an account exists for **{email}**, you'll receive a password reset email shortly.
                            
                            The link expires in 1 hour.
                            """)
                        else:
                            st.warning("Unable to send email. Please try again later.")
                    else:
                        # Don't reveal if email exists (security)
                        st.success(f"""
                        ✅ Password reset link sent!
                        
                        If an account exists for **{email}**, you'll receive a password reset email shortly.
                        
                        The link expires in 1 hour.
                        """)
        
        st.markdown("---")
        
        if st.button("← Back to Login"):
            st.query_params.clear()
            st.rerun()
