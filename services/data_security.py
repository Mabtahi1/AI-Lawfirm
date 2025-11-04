import streamlit as st
import json
import os
import hashlib
from datetime import datetime

class DataSecurity:
    """Centralized data security and isolation manager"""
    
    DATA_DIR = "user_data"
    
    @staticmethod
    def get_current_user_email():
        """Get currently logged-in user's email - ALWAYS use this"""
        user_data = st.session_state.get('user_data', {})
        email = user_data.get('email', None)
        
        if not email:
            st.error("🔒 Session expired. Please log in again.")
            st.session_state.clear()
            st.stop()
        
        return email
    
    @staticmethod
    def get_user_id():
        """Get secure user ID hash"""
        email = DataSecurity.get_current_user_email()
        return hashlib.sha256(email.encode()).hexdigest()[:16]
    
    @staticmethod
    def get_user_data_path(data_type):
        """Get secure path for user's data file"""
        email = DataSecurity.get_current_user_email()
        safe_email = email.replace('@', '_at_').replace('.', '_').replace('/', '_')
        
        # Create user-specific directory
        user_dir = os.path.join(DataSecurity.DATA_DIR, safe_email)
        os.makedirs(user_dir, exist_ok=True)
        
        return os.path.join(user_dir, f"{data_type}.json")
    
    @staticmethod
    def save_user_data(data_type, data):
        """Save data ONLY for current user"""
        file_path = DataSecurity.get_user_data_path(data_type)
        
        # Add metadata
        secure_data = {
            'owner': DataSecurity.get_current_user_email(),
            'last_modified': datetime.now().isoformat(),
            'data': data
        }
        
        with open(file_path, 'w') as f:
            json.dump(secure_data, f, default=str, indent=2)
    
    @staticmethod
    def load_user_data(data_type, default=None):
        """Load data ONLY for current user"""
        file_path = DataSecurity.get_user_data_path(data_type)
        
        if not os.path.exists(file_path):
            return default if default is not None else []
        
        try:
            with open(file_path, 'r') as f:
                secure_data = json.load(f)
            
            # Verify owner matches current user
            if secure_data.get('owner') != DataSecurity.get_current_user_email():
                st.error("🚨 Security violation: Data owner mismatch!")
                return default if default is not None else []
            
            return secure_data.get('data', default if default is not None else [])
        
        except Exception as e:
            st.error(f"Error loading data: {e}")
            return default if default is not None else []
    
    @staticmethod
    def verify_session():
        """Verify user session is valid"""
        if 'user_data' not in st.session_state:
            return False
        
        user_data = st.session_state.get('user_data', {})
        if not user_data.get('email'):
            return False
        
        return True
    
    @staticmethod
    def require_auth(page_name="this page"):
        """Decorator/function to require authentication"""
        if not DataSecurity.verify_session():
            st.error(f"🔒 Please log in to access {page_name}")
            st.info("👉 Go to Login page from the sidebar")
            st.stop()
    
    @staticmethod
    def get_user_matters():
        """Get ONLY current user's matters"""
        return DataSecurity.load_user_data('matters', [])
    
    @staticmethod
    def get_user_documents():
        """Get ONLY current user's documents"""
        return DataSecurity.load_user_data('documents', [])
    
    @staticmethod
    def get_user_time_entries():
        """Get ONLY current user's time entries"""
        return DataSecurity.load_user_data('time_entries', [])
    
    @staticmethod
    def get_user_invoices():
        """Get ONLY current user's invoices"""
        return DataSecurity.load_user_data('invoices', [])
    
    @staticmethod
    def get_user_tasks():
        """Get ONLY current user's tasks"""
        return DataSecurity.load_user_data('tasks', [])
    
    @staticmethod
    def get_user_events():
        """Get ONLY current user's events"""
        return DataSecurity.load_user_data('events', [])
    
    @staticmethod
    def get_user_clients():
        """Get ONLY current user's portal clients"""
        return DataSecurity.load_user_data('portal_clients', [])
