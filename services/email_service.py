import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import streamlit as st
from datetime import datetime, timedelta
import secrets
import hashlib

class EmailService:
    """Service for sending emails"""
    
    def __init__(self):
        self.api_key = os.getenv('SENDGRID_API_KEY')
        self.from_email = os.getenv('SENDGRID_FROM_EMAIL', 'noreply@legaldocpro.com')
        self.app_url = os.getenv('APP_URL', 'http://localhost:5002')
    
    def send_email(self, to_email, subject, html_content):
        """Send an email using SendGrid"""
        
        if not self.api_key:
            # Development mode - just show message
            st.info(f"📧 Email would be sent to {to_email}: {subject}")
            return True
        
        try:
            message = Mail(
                from_email=self.from_email,
                to_emails=to_email,
                subject=subject,
                html_content=html_content
            )
            
            sg = SendGridAPIClient(self.api_key)
            response = sg.send(message)
            
            return response.status_code in [200, 201, 202]
        
        except Exception as e:
            st.error(f"Failed to send email: {str(e)}")
            return False
            
    def send_registration_confirmation_email(self, email, name, organization_name, organization_code, plan):
        """Send confirmation email after registration"""
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                .info-box {{ background: white; padding: 15px; margin: 15px 0; border-left: 4px solid #667eea; border-radius: 5px; }}
                .button {{ display: inline-block; background: #667eea; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
                .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🎉 Welcome to Prolexis Analytics!</h1>
                </div>
                <div class="content">
                    <h2>Hi {name},</h2>
                    <p>Your account has been created successfully!</p>
                    
                    <div class="info-box">
                        <strong>📋 Account Details:</strong><br>
                        <strong>Plan:</strong> {plan.title()}<br>
                        <strong>Organization:</strong> {organization_name}<br>
                        <strong>Organization Code:</strong> {organization_code}
                    </div>
                    
                    <p style="text-align: center;">
                        <a href="https://prolexisanalytics.com/app/" class="button">Login Now</a>
                    </p>
                    
                    <p>If you have any questions, contact us at support@prolexisanalytics.com</p>
                </div>
                <div class="footer">
                    <p>© 2025 Prolexis Analytics. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(
            to_email=email,
            subject=f"Welcome to Prolexis Analytics - {plan.title()} Plan",
            html_content=html_content
        )
        
    def send_verification_email(self, email, verification_token):
        """Send email verification link"""
        
        verification_url = f"{self.app_url}?verify={verification_token}"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                .button {{ display: inline-block; background: #667eea; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
                .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>⚖️ Welcome to LegalDoc Pro!</h1>
                </div>
                <div class="content">
                    <h2>Verify Your Email Address</h2>
                    <p>Thank you for signing up! Please verify your email address to activate your account and start your 14-day free trial.</p>
                    
                    <p style="text-align: center;">
                        <a href="{verification_url}" class="button">Verify Email Address</a>
                    </p>
                    
                    <p>Or copy and paste this link into your browser:</p>
                    <p style="word-break: break-all; color: #667eea;">{verification_url}</p>
                    
                    <p><strong>This link expires in 24 hours.</strong></p>
                    
                    <p>If you didn't create an account with LegalDoc Pro, please ignore this email.</p>
                </div>
                <div class="footer">
                    <p>© 2025 LegalDoc Pro. All rights reserved.</p>
                    <p>123 Legal Street, City, ST 12345</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(
            to_email=email,
            subject="Verify Your Email - LegalDoc Pro",
            html_content=html_content
        )
    
    def send_password_reset_email(self, email, reset_token):
        """Send password reset link"""
        
        reset_url = f"{self.app_url}?reset={reset_token}"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                .button {{ display: inline-block; background: #667eea; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
                .warning {{ background: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 20px 0; }}
                .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🔐 Password Reset Request</h1>
                </div>
                <div class="content">
                    <h2>Reset Your Password</h2>
                    <p>We received a request to reset your password for your LegalDoc Pro account.</p>
                    
                    <p style="text-align: center;">
                        <a href="{reset_url}" class="button">Reset Password</a>
                    </p>
                    
                    <p>Or copy and paste this link into your browser:</p>
                    <p style="word-break: break-all; color: #667eea;">{reset_url}</p>
                    
                    <div class="warning">
                        <strong>⚠️ Security Notice:</strong> This link expires in 1 hour. If you didn't request this reset, please ignore this email and your password will remain unchanged.
                    </div>
                    
                    <p>For security reasons, we never send passwords via email.</p>
                </div>
                <div class="footer">
                    <p>© 2025 LegalDoc Pro. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(
            to_email=email,
            subject="Password Reset - LegalDoc Pro",
            html_content=html_content
        )
    
    def send_welcome_email(self, email, name, plan_name):
        """Send welcome email after verification"""
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                .feature {{ background: white; padding: 15px; margin: 10px 0; border-left: 4px solid #667eea; border-radius: 5px; }}
                .button {{ display: inline-block; background: #667eea; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
                .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🎉 Welcome to LegalDoc Pro!</h1>
                </div>
                <div class="content">
                    <h2>Hi {name},</h2>
                    <p>Your email has been verified and your <strong>{plan_name}</strong> account is now active!</p>
                    
                    <h3>🚀 Get Started:</h3>
                    
                    <div class="feature">
                        <strong>📁 Step 1:</strong> Upload your first documents
                    </div>
                    <div class="feature">
                        <strong>⚖️ Step 2:</strong> Create your first matter
                    </div>
                    <div class="feature">
                        <strong>⏱️ Step 3:</strong> Start tracking time
                    </div>
                    <div class="feature">
                        <strong>🤖 Step 4:</strong> Try AI-powered case comparison
                    </div>
                    
                    <p style="text-align: center;">
                        <a href="{self.app_url}" class="button">Open LegalDoc Pro</a>
                    </p>
                    
                    <h3>💡 Need Help?</h3>
                    <p>Check out our <a href="{self.app_url}/help">Help Center</a> or contact our support team at support@legaldocpro.com</p>
                    
                    <p><strong>Your 14-day free trial is now active!</strong></p>
                </div>
                <div class="footer">
                    <p>© 2025 LegalDoc Pro. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(
            to_email=email,
            subject=f"Welcome to LegalDoc Pro - {plan_name} Plan",
            html_content=html_content
        )
    
    def send_payment_success_email(self, email, name, amount, plan_name):
        """Send payment confirmation email"""
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #28a745 0%, #20c997 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                .receipt {{ background: white; padding: 20px; border-radius: 5px; margin: 20px 0; }}
                .total {{ font-size: 24px; color: #28a745; font-weight: bold; }}
                .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>✅ Payment Successful!</h1>
                </div>
                <div class="content">
                    <h2>Thank You, {name}!</h2>
                    <p>Your payment has been processed successfully.</p>
                    
                    <div class="receipt">
                        <h3>Receipt</h3>
                        <p><strong>Plan:</strong> {plan_name}</p>
                        <p><strong>Amount:</strong> <span class="total">${amount:.2f}</span></p>
                        <p><strong>Date:</strong> {datetime.now().strftime('%B %d, %Y')}</p>
                        <p><strong>Next Billing Date:</strong> {(datetime.now() + timedelta(days=30)).strftime('%B %d, %Y')}</p>
                    </div>
                    
                    <p>Your subscription will renew automatically. You can manage your subscription anytime in your account settings.</p>
                    
                    <p>If you have any questions, please contact us at billing@legaldocpro.com</p>
                </div>
                <div class="footer">
                    <p>© 2025 LegalDoc Pro. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(
            to_email=email,
            subject=f"Payment Confirmation - ${amount:.2f}",
            html_content=html_content
        )
    
    def send_trial_expiring_email(self, email, name, days_left):
        """Send trial expiring reminder"""
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #ffc107 0%, #ff9800 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                .button {{ display: inline-block; background: #ffc107; color: #212529; padding: 15px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; font-weight: bold; }}
                .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>⏰ Your Trial is Ending Soon</h1>
                </div>
                <div class="content">
                    <h2>Hi {name},</h2>
                    <p>Your LegalDoc Pro free trial ends in <strong>{days_left} days</strong>.</p>
                    
                    <p>To continue using all the features you love, please add your payment information.</p>
                    
                    <p style="text-align: center;">
                        <a href="{self.app_url}?page=billing" class="button">Add Payment Method</a>
                    </p>
                    
                    <p><strong>What happens next?</strong></p>
                    <ul>
                        <li>If you add payment: Seamless transition to paid plan</li>
                        <li>If you don't: Access will be limited to free features</li>
                    </ul>
                    
                    <p>Questions? Contact us at support@legaldocpro.com</p>
                </div>
                <div class="footer">
                    <p>© 2025 LegalDoc Pro. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(
            to_email=email,
            subject=f"Trial Ending in {days_left} Days - LegalDoc Pro",
            html_content=html_content
        )


class AuthTokenManager:
    """Manage authentication tokens"""
    
    @staticmethod
    def generate_token():
        """Generate a secure random token"""
        return secrets.token_urlsafe(32)
    
    @staticmethod
    def hash_password(password):
        """Hash a password using SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def verify_password(password, hashed_password):
        """Verify a password against its hash"""
        return hashlib.sha256(password.encode()).hexdigest() == hashed_password
    
    @staticmethod
    def create_verification_token(email):
        """Create email verification token"""
        token = AuthTokenManager.generate_token()
        
        # Store token in session state
        if 'verification_tokens' not in st.session_state:
            st.session_state.verification_tokens = {}
        
        st.session_state.verification_tokens[token] = {
            'email': email,
            'expires': (datetime.now() + timedelta(hours=24)).isoformat(),
            'type': 'verification'
        }
        
        return token
    
    @staticmethod
    def create_reset_token(email):
        """Create password reset token"""
        token = AuthTokenManager.generate_token()
        
        # Store token in session state
        if 'reset_tokens' not in st.session_state:
            st.session_state.reset_tokens = {}
        
        st.session_state.reset_tokens[token] = {
            'email': email,
            'expires': (datetime.now() + timedelta(hours=1)).isoformat(),
            'type': 'reset'
        }
        
        return token
    
    @staticmethod
    def verify_token(token, token_type='verification'):
        """Verify a token and return associated email"""
        
        token_store = st.session_state.get(f'{token_type}_tokens', {})
        
        if token not in token_store:
            return None, "Invalid token"
        
        token_data = token_store[token]
        
        # Check expiration
        expires = datetime.fromisoformat(token_data['expires'])
        if datetime.now() > expires:
            del token_store[token]
            return None, "Token expired"
        
        return token_data['email'], None
