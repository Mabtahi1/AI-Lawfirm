import os
import json
from datetime import datetime
import streamlit as st

class LocalStorage:
    """Local file storage for documents (before S3)"""
    
    DATA_DIR = "user_data"
    DOCUMENTS_DIR = "documents"
    
    @staticmethod
    def get_user_directory(user_email):
        """Get user-specific directory"""
        safe_email = user_email.replace('@', '_at_').replace('.', '_').replace('/', '_')
        user_dir = os.path.join(LocalStorage.DATA_DIR, safe_email)
        os.makedirs(user_dir, exist_ok=True)
        return user_dir
    
    @staticmethod
    def get_documents_directory(user_email):
        """Get user's documents directory"""
        user_dir = LocalStorage.get_user_directory(user_email)
        docs_dir = os.path.join(user_dir, LocalStorage.DOCUMENTS_DIR)
        os.makedirs(docs_dir, exist_ok=True)
        return docs_dir
    
    @staticmethod
    def save_document(user_email, document_id, file_content, filename, content_type):
        """
        Save document as actual file (not in JSON!)
        
        Structure:
        user_data/
        └── user_at_email_com/
            ├── documents.json          ← Metadata only
            └── documents/              ← Actual files here
                ├── doc-123_contract.pdf
                └── doc-456_brief.docx
        """
        try:
            docs_dir = LocalStorage.get_documents_directory(user_email)
            
            # Create safe filename
            safe_filename = f"{document_id}_{filename}"
            file_path = os.path.join(docs_dir, safe_filename)
            
            # Save the actual file
            with open(file_path, 'wb') as f:
                f.write(file_content)
            
            # Return the relative path
            return file_path
        
        except Exception as e:
            st.error(f"Error saving document: {e}")
            return None
    @staticmethod
    def load_all_users():
        """Load all registered users from Firebase"""
        try:
            from services.firebase_config import db
            ref = db.reference('users')
            users = ref.get()
            return users if users else {}
        except:
            return {}
    
    @staticmethod
    def save_all_users(users_dict):
        """Save all users to Firebase"""
        try:
            from services.firebase_config import db
            ref = db.reference('users')
            ref.set(users_dict)
        except Exception as e:
            st.error(f"Error saving users: {e}")
    @staticmethod
    def get_document(user_email, document_id, filename):
        """Retrieve document file"""
        try:
            docs_dir = LocalStorage.get_documents_directory(user_email)
            safe_filename = f"{document_id}_{filename}"
            file_path = os.path.join(docs_dir, safe_filename)
            
            if not os.path.exists(file_path):
                return None
            
            with open(file_path, 'rb') as f:
                return f.read()
        
        except Exception as e:
            st.error(f"Error retrieving document: {e}")
            return None
    
    @staticmethod
    def delete_document(user_email, document_id, filename):
        """Delete document file"""
        try:
            docs_dir = LocalStorage.get_documents_directory(user_email)
            safe_filename = f"{document_id}_{filename}"
            file_path = os.path.join(docs_dir, safe_filename)
            
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            
            return False
        
        except Exception as e:
            st.error(f"Error deleting document: {e}")
            return False
    
    @staticmethod
    def list_user_documents(user_email):
        """List all document files for a user"""
        try:
            docs_dir = LocalStorage.get_documents_directory(user_email)
            
            files = []
            for filename in os.listdir(docs_dir):
                file_path = os.path.join(docs_dir, filename)
                if os.path.isfile(file_path):
                    files.append({
                        'filename': filename,
                        'size': os.path.getsize(file_path),
                        'modified': datetime.fromtimestamp(os.path.getmtime(file_path))
                    })
            
            return files
        
        except Exception as e:
            return []
    
    @staticmethod
    def save_user_data(user_email, data_type, data):
        """Save user data (metadata only, NO file content!)"""
        user_dir = LocalStorage.get_user_directory(user_email)
        file_path = os.path.join(user_dir, f"{data_type}.json")
        
        # Add metadata
        secure_data = {
            'owner': user_email,
            'last_modified': datetime.now().isoformat(),
            'data': data
        }
        
        with open(file_path, 'w') as f:
            json.dump(secure_data, f, default=str, indent=2)
    
    @staticmethod
    def load_user_data(user_email, data_type, default=None):
        """Load user data"""
        user_dir = LocalStorage.get_user_directory(user_email)
        file_path = os.path.join(user_dir, f"{data_type}.json")
        
        if not os.path.exists(file_path):
            return default if default is not None else []
        
        try:
            with open(file_path, 'r') as f:
                secure_data = json.load(f)
            
            # Verify owner
            if secure_data.get('owner') != user_email:
                st.error("🚨 Security violation: Data owner mismatch!")
                return default if default is not None else []
            
            return secure_data.get('data', default if default is not None else [])
        
        except Exception as e:
            st.error(f"Error loading data: {e}")
            return default if default is not None else []
