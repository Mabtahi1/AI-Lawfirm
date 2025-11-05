import stripe
import os
import streamlit as st
from datetime import datetime, timedelta
from services.subscription_config import SUBSCRIPTION_PLANS

class PaymentService:
    """Service for handling Stripe payments"""
    
    def __init__(self):
        self.stripe_secret = os.getenv('STRIPE_SECRET_KEY')
        self.stripe_publishable = os.getenv('STRIPE_PUBLISHABLE_KEY')
        
        if self.stripe_secret:
            stripe.api_key = self.stripe_secret
    
    def create_customer(self, email, name, org_code):
        """Create a Stripe customer"""
        
        if not self.stripe_secret:
            # Development mode
            return f"cus_dev_{org_code}"
        
        try:
            customer = stripe.Customer.create(
                email=email,
                name=name,
                metadata={'org_code': org_code}
            )
            return customer.id
        except Exception as e:
            st.error(f"Error creating customer: {str(e)}")
            return None
    
    def create_payment_intent(self, amount, currency='usd', customer_id=None):
        """Create a payment intent"""
        
        if not self.stripe_secret:
            # Development mode
            return {
                'id': 'pi_dev_123',
                'client_secret': 'dev_secret_123',
                'status': 'succeeded'
            }
        
        try:
            intent = stripe.PaymentIntent.create(
                amount=int(amount * 100),  # Convert to cents
                currency=currency,
                customer=customer_id,
                automatic_payment_methods={'enabled': True}
            )
            return intent
        except Exception as e:
            st.error(f"Error creating payment intent: {str(e)}")
            return None
    
    def create_subscription(self, customer_id, plan_name):
        """Create a Stripe subscription using plan name"""
        
        if not self.stripe_secret:
            # Development mode
            return {
                'id': 'sub_dev_123',
                'status': 'active',
                'current_period_end': (datetime.now() + timedelta(days=30)).timestamp()
            }
        
        try:
            # Get price ID from config
            plan_details = SUBSCRIPTION_PLANS.get(plan_name)
            if not plan_details:
                raise ValueError(f"Invalid plan: {plan_name}")
            
            price_id = plan_details.get('stripe_price_id')
            if not price_id:
                raise ValueError(f"No Stripe price ID configured for {plan_name}")
            
            # Create subscription
            subscription = stripe.Subscription.create(
                customer=customer_id,
                items=[{'price': price_id}],
                trial_period_days=3,
                metadata={'plan': plan_name}
            )
            return subscription
        except Exception as e:
            st.error(f"Error creating subscription: {str(e)}")
            return None
    
    def cancel_subscription(self, subscription_id):
        """Cancel a Stripe subscription"""
        
        if not self.stripe_secret:
            return True
        
        try:
            stripe.Subscription.delete(subscription_id)
            return True
        except Exception as e:
            st.error(f"Error canceling subscription: {str(e)}")
            return False
    
    def update_subscription(self, subscription_id, new_price_id):
        """Update subscription to new plan"""
        
        if not self.stripe_secret:
            return True
        
        try:
            subscription = stripe.Subscription.retrieve(subscription_id)
            stripe.Subscription.modify(
                subscription_id,
                items=[{
                    'id': subscription['items']['data'][0].id,
                    'price': new_price_id
                }]
            )
            return True
        except Exception as e:
            st.error(f"Error updating subscription: {str(e)}")
            return False
    
    def get_publishable_key(self):
        """Get Stripe publishable key"""
        return self.stripe_publishable or "pk_test_development_key"
    
    def show_payment_form(self, plan_name, on_success_callback=None):
        """Show Stripe payment form"""
        
        plan_details = SUBSCRIPTION_PLANS[plan_name]
        amount = plan_details['price']
        
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem;
            border-radius: 16px;
            text-align: center;
            margin-bottom: 2rem;
        ">
            <h2>{plan_details['name']}</h2>
            <h1>${amount}/month</h1>
            <p>14-day free trial • Cancel anytime</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Payment form
        st.markdown("### 💳 Payment Information")
        
        with st.form("payment_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                card_number = st.text_input("Card Number", placeholder="4242 4242 4242 4242")
                card_name = st.text_input("Name on Card")
            
            with col2:
                col_exp1, col_exp2 = st.columns(2)
                with col_exp1:
                    exp_month = st.selectbox("Month", list(range(1, 13)))
                with col_exp2:
                    exp_year = st.selectbox("Year", list(range(2025, 2036)))
                
                cvv = st.text_input("CVV", max_chars=4, placeholder="123")
            
            billing_address = st.text_input("Billing Address")
            
            col_city, col_state, col_zip = st.columns(3)
            with col_city:
                city = st.text_input("City")
            with col_state:
                state = st.text_input("State")
            with col_zip:
                zip_code = st.text_input("ZIP Code")
            
            st.markdown("---")
            
            # Terms
            st.markdown("""
            **By clicking "Start Trial", you agree to:**
            - 14-day free trial starting today
            - Automatic billing of ${}/month after trial
            - You can cancel anytime before trial ends
            """.format(amount))
            
            agree = st.checkbox("I agree to the Terms of Service and Privacy Policy")
            
            submitted = st.form_submit_button("🚀 Start Free Trial", use_container_width=True, type="primary")
            
            if submitted:
                if not agree:
                    st.error("Please agree to the terms")
                elif not card_number or len(card_number.replace(" ", "")) != 16:
                    st.error("Please enter a valid card number")
                elif not cvv or len(cvv) < 3:
                    st.error("Please enter a valid CVV")
                else:
                    # Process payment
                    with st.spinner("Processing payment..."):
                        success = self.process_payment(
                            card_number, exp_month, exp_year, cvv,
                            card_name, amount, plan_name
                        )
                        
                        if success:
                            st.success("✅ Payment successful! Your trial has started.")
                            if on_success_callback:
                                on_success_callback()
                            return True
                        else:
                            st.error("❌ Payment failed. Please check your card details.")
        
        # Test card info
        with st.expander("🧪 Test Card Numbers"):
            st.info("""
            **For testing, use these Stripe test cards:**
            
            **Success:** 4242 4242 4242 4242
            **Decline:** 4000 0000 0000 0002
            **Requires Auth:** 4000 0025 0000 3155
            
            Use any future date for expiry and any 3 digits for CVV.
            """)
        
        return False
    
    def process_payment(self, card_number, exp_month, exp_year, cvv, card_name, amount, plan_name):
        """Process a payment"""
        
        # In development, simulate success
        if not self.stripe_secret:
            import time
            time.sleep(2)  # Simulate processing
            return True
        
        try:
            # Create payment intent
            intent = self.create_payment_intent(amount)
            
            if intent and intent.get('status') == 'succeeded':
                return True
            
            return False
        
        except Exception as e:
            st.error(f"Payment error: {str(e)}")
            return False
