import streamlit as st
from datetime import datetime
import hashlib

# Always use local storage for now
from services.local_storage import LocalStorage

class DataSecurity:
    """Centralized data security and isolation manager"""
    
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
    def save_user_data(data_type, data):
        """
        Save data for current user
        
        IMPORTANT: For documents, this saves METADATA only
        Use save_document() for actual file content
        """
        email = DataSecurity.get_current_user_email()
        return LocalStorage.save_user_data(email, data_type, data)
    
    @staticmethod
    def load_user_data(data_type, default=None):
        """Load data for current user"""
        email = DataSecurity.get_current_user_email()
        return LocalStorage.load_user_data(email, data_type, default)
    
    @staticmethod
    def save_document(document_id, file_content, filename, content_type):
        """
        Save actual document file
        
        This saves the BINARY FILE, not base64 in JSON!
        Returns: file path
        """
        email = DataSecurity.get_current_user_email()
        return LocalStorage.save_document(email, document_id, file_content, filename, content_type)
    
    @staticmethod
    def get_document(document_id, filename):
        """Get actual document file content"""
        email = DataSecurity.get_current_user_email()
        return LocalStorage.get_document(email, document_id, filename)
    
    @staticmethod
    def delete_document(document_id, filename):
        """Delete document file"""
        email = DataSecurity.get_current_user_email()
        return LocalStorage.delete_document(email, document_id, filename)
    
    @staticmethod
    def list_user_documents():
        """List all documents for current user"""
        email = DataSecurity.get_current_user_email()
        return LocalStorage.list_user_documents(email)
    
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
        """Require authentication"""
        if not DataSecurity.verify_session():
            st.error(f"🔒 Please log in to access {page_name}")
            st.info("👉 Go to Login page from the sidebar")
            st.stop()
    
    # Convenience methods for common data types
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
