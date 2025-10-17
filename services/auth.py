import streamlit as st
from datetime import datetime, timedelta
import hashlib
import uuid

class AuthService:
    """Authentication service with login and registration"""
    
    def __init__(self):
        self.initialize_session_state()
    
    def initialize_session_state(self):
        """Initialize authentication session state"""
        if 'authenticated' not in st.session_state:
            st.session_state.authenticated = False
        
        if 'user_data' not in st.session_state:
            st.session_state.user_data = {}
        
        # Initialize users database (in production, use real database)
        if 'users_db' not in st.session_state:
            st.session_state.users_db = self.get_demo_users()
        
        # Initialize subscriptions
        if 'subscriptions' not in st.session_state:
            st.session_state.subscriptions = self.get_demo_subscriptions()
    
    def get_demo_users(self):
        """Get demo user accounts"""
        return {
            'basic@demo.com': {
                'password': self.hash_password('demo123'),
                'name': 'Basic User',
                'organization_name': 'Demo Basic Firm',
                'organization_code': 'demobasic',
                'role': 'subscription_owner',
                'created_at': datetime.now().isoformat(),
                'email_verified': True
            },
            'pro@demo.com': {
                'password': self.hash_password('demo123'),
                'name': 'Professional User',
                'organization_name': 'Demo Pro Firm',
                'organization_code': 'demopro',
                'role': 'subscription_owner',
                'created_at': datetime.now().isoformat(),
                'email_verified': True
            },
            'enterprise@demo.com': {
                'password': self.hash_password('demo123'),
                'name': 'Enterprise User',
                'organization_name': 'Demo Enterprise Firm',
                'organization_code': 'demoenterprise',
                'role': 'subscription_owner',
                'created_at': datetime.now().isoformat(),
                'email_verified': True
            }
        }
    
    def get_demo_subscriptions(self):
        """Get demo subscriptions"""
        return {
            'demobasic': {
                'plan': 'basic',
                'status': 'active',
                'start_date': datetime.now().isoformat(),
                'billing_cycle': 'monthly',
                'trial_end': (datetime.now() + timedelta(days=14)).isoformat()
            },
            'demopro': {
                'plan': 'professional',
                'status': 'active',
                'start_date': datetime.now().isoformat(),
                'billing_cycle': 'monthly'
            },
            'demoenterprise': {
                'plan': 'enterprise',
                'status': 'active',
                'start_date': datetime.now().isoformat(),
                'billing_cycle': 'monthly'
            }
        }
    
    def hash_password(self, password):
        """Hash password for storage"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def login(self, email, password):
        """Login user"""
        email = email.lower().strip()
        
        # Check if user exists
        if email not in st.session_state.users_db:
            return False, "Invalid email or password"
        
        user = st.session_state.users_db[email]
        
        # Check password
        if user['password'] != self.hash_password(password):
            return False, "Invalid email or password"
        
        # Check email verification
        if not user.get('email_verified', False):
            return False, "Please verify your email address first"
        
        # Get organization code
        org_code = user.get('organization_code')
        
        # Get subscription
        subscription = st.session_state.subscriptions.get(org_code, {
            'plan': 'basic',
            'status': 'active'
        })
        
        # Set session
        st.session_state.authenticated = True
        st.session_state.user_data = {
            'email': email,
            'name': user['name'],
            'organization_name': user['organization_name'],
            'organization_code': org_code,
            'role': user['role'],
            'subscription': subscription
        }
        
        return True, "Login successful"
    
    def register(self, email, password, name, organization_name, organization_code, plan='basic'):
        """Register new user"""
        email = email.lower().strip()
        organization_code = organization_code.lower().strip()
        
        # Validation
        if email in st.session_state.users_db:
            return False, "An account with this email already exists"
        
        if any(u.get('organization_code') == organization_code 
               for u in st.session_state.users_db.values()):
            return False, "This organization code is already taken"
        
        if len(password) < 8:
            return False, "Password must be at least 8 characters"
        
        # Create user
        st.session_state.users_db[email] = {
            'password': self.hash_password(password),
            'name': name,
            'organization_name': organization_name,
            'organization_code': organization_code,
            'role': 'subscription_owner',
            'created_at': datetime.now().isoformat(),
            'email_verified': True  # Auto-verify for demo (in production, send email)
        }
        
        # Create subscription with trial
        st.session_state.subscriptions[organization_code] = {
            'plan': plan,
            'status': 'trial',
            'start_date': datetime.now().isoformat(),
            'trial_end': (datetime.now() + timedelta(days=14)).isoformat(),
            'billing_cycle': 'monthly'
        }
        
        return True, "Account created successfully"
    
    def logout(self):
        """Logout user"""
        st.session_state.authenticated = False
        st.session_state.user_data = {}
    
    def is_authenticated(self):
        """Check if user is authenticated"""
        return st.session_state.get('authenticated', False)
    
    def get_user_data(self):
        """Get current user data"""
        return st.session_state.get('user_data', {})
    
    def require_auth(self):
        """Require authentication - redirect to login if not authenticated"""
        if not self.is_authenticated():
            st.warning("⚠️ Please login to access this page")
            st.stop()
