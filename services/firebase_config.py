import firebase_admin
from firebase_admin import credentials, db
import os

# Initialize Firebase
if not firebase_admin._apps:
    # Path to your service account key
    cred_path = os.path.join(os.path.dirname(__file__), '..', 'firebase-credentials.json')
    
    cred = credentials.Certificate(cred_path)
    
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://ai-legaldoc-default-rtdb.firebaseio.com'
    })
