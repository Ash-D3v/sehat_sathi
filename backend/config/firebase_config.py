import firebase_admin
from firebase_admin import credentials, firestore
import os
from config.settings import Config

class FirebaseConfig:
    _instance = None
    _db = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FirebaseConfig, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not firebase_admin._apps:
            self.initialize_firebase()
    
    def initialize_firebase(self):
        """Initialize Firebase Admin SDK"""
        try:
            config = Config()
            
            if os.path.exists(config.FIREBASE_KEY_PATH):
                cred = credentials.Certificate(config.FIREBASE_KEY_PATH)
                firebase_admin.initialize_app(cred, {
                    'projectId': config.FIREBASE_PROJECT_ID
                })
                print("Firebase initialized successfully")
            else:
                print(f"Firebase key file not found at: {config.FIREBASE_KEY_PATH}")
                
        except Exception as e:
            print(f"Error initializing Firebase: {e}")
            raise
    
    def get_db(self):
        """Get Firestore database instance"""
        if self._db is None:
            self._db = firestore.client()
        return self._db

# Global instance
firebase_config = FirebaseConfig()