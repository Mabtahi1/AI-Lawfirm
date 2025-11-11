import streamlit as st
from datetime import datetime, timedelta
import hashlib

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
        
        # Load from persistent storage FIRST
        from services.local_storage import LocalStorage
        stored_users = LocalStorage.load_all_users()
        
        # Initialize users database - merge with stored users
        if 'users_db' not in st.session_state:
            demo_users = self.get_demo_users()
            # Merge: stored users + demo users
            demo_users.update(stored_users)
            st.session_state.users_db = demo_users
        
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
                'billing_cycle': 'monthly'
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
        
        # Get organization code
        org_code = user.get('organization_code')
        
        # Get subscription
        subscription = st.session_state.subscriptions.get(org_code, {
            'plan': 'basic',
            'status': 'active'
        })
        
        # Set session
        st.session_state.authenticated = True
        st.session_state.logged_in = True  # Added this
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
        
        # CHECK PERSISTENT STORAGE
        from services.local_storage import LocalStorage
        existing_users = LocalStorage.load_all_users()

        #Debug
        st.write("DEBUG: Existing users:", list(existing_users.keys()))
        st.write("DEBUG: Trying to register:", email)
        st.write("DEBUG: Email exists?", email in existing_users)
        
        if email in existing_users:
            return False, "An account with this email already exists"
        
        # Check organization code in persistent storage
        if any(u.get('organization_code') == organization_code for u in existing_users.values()):
            return False, "This organization code is already taken"
        
        if len(password) < 8:
            return False, "Password must be at least 8 characters"
        
        # Create user
        user_data = {
            'password': self.hash_password(password),
            'name': name,
            'organization_name': organization_name,
            'organization_code': organization_code,
            'role': 'subscription_owner',
            'created_at': datetime.now().isoformat(),
            'email_verified': True
        }
        
        # Save to session state
        st.session_state.users_db[email] = user_data
        
        # Save to persistent storage
        # Save to persistent storage
        existing_users[email] = user_data
        st.write("🔍 BEFORE SAVE - Users to save:", list(existing_users.keys()))
        
        try:
            LocalStorage.save_all_users(existing_users)
            st.success("✅ save_all_users() completed")
        except Exception as e:
            st.error(f"❌ save_all_users() failed: {e}")
        
        # Verify it saved
        loaded = LocalStorage.load_all_users()
        st.write("🔍 AFTER SAVE - Loaded users:", list(loaded.keys()))
        
        if email in loaded:
            st.success(f"✅ {email} confirmed in storage!")
        else:
            st.error(f"❌ {email} NOT in storage after save!")
        
        # Create subscription with trial
        subscription_data = {
            'plan': plan,
            'status': 'trial',
            'start_date': datetime.now().isoformat(),
            'trial_end': (datetime.now() + timedelta(days=14)).isoformat(),
            'billing_cycle': 'monthly'
        }
        
        st.session_state.subscriptions[organization_code] = subscription_data
        
        return True, "Account created successfully"
    
    def show_login(self):
        """Show login/signup page"""
        # Import here to avoid circular import
        import main_login
        main_login.show_login_page(self)
    
    def render_sidebar(self):
        """Render sidebar for logged in users"""
        # This will be implemented by your existing app
        pass
    
    def logout(self):
        """Logout user"""
        st.session_state.authenticated = False
        st.session_state.logged_in = False
        st.session_state.user_data = {}
