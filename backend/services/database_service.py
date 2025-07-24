import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
from typing import Dict, List
import logging
from config.settings import Config

class DatabaseService:
    def __init__(self):
        self.config = Config()
        self.logger = logging.getLogger(__name__)
        
        # Initialize Firebase if not already done
        if not firebase_admin._apps:
            try:
                cred = credentials.Certificate(self.config.FIREBASE_KEY_PATH)
                firebase_admin.initialize_app(cred)
                self.logger.info("Firebase initialized successfully")
            except Exception as e:
                self.logger.error(f"Error initializing Firebase: {e}")
                raise
        
        self.db = firestore.client()

    def store_conversation(self, user_id: str, conversation_data: Dict):
        """Store conversation data in Firestore"""
        try:
            # Add timestamp
            conversation_data['created_at'] = firestore.SERVER_TIMESTAMP
            conversation_data['updated_at'] = firestore.SERVER_TIMESTAMP
            
            # Store in conversations collection
            doc_ref = self.db.collection('conversations').add(conversation_data)
            
            # Also update user's latest conversation
            user_ref = self.db.collection('users').document(user_id)
            user_ref.set({
                'last_conversation': conversation_data,
                'last_active': firestore.SERVER_TIMESTAMP,
                'total_conversations': firestore.Increment(1)
            }, merge=True)
            
            self.logger.info(f"Conversation stored for user {user_id}")
            
        except Exception as e:
            self.logger.error(f"Error storing conversation: {e}")
            raise

    def get_user_history(self, user_id: str, limit: int = 10) -> Dict:
        """Get user's conversation history"""
        try:
            # Get recent conversations
            conversations_ref = self.db.collection('conversations')\
                .where('user_id', '==', user_id)\
                .order_by('created_at', direction=firestore.Query.DESCENDING)\
                .limit(limit)
            
            conversations = []
            for doc in conversations_ref.stream():
                conv_data = doc.to_dict()
                conv_data['id'] = doc.id
                conversations.append(conv_data)
            
            # Get user profile
            user_ref = self.db.collection('users').document(user_id)
            user_doc = user_ref.get()
            user_data = user_doc.to_dict() if user_doc.exists else {}
            
            return {
                'user_data': user_data,
                'conversations': conversations,
                'total_found': len(conversations)
            }
            
        except Exception as e:
            self.logger.error(f"Error getting user history: {e}")
            return {'user_data': {}, 'conversations': [], 'total_found': 0}

    def store_user_profile(self, user_id: str, profile_data: Dict):
        """Store or update user profile"""
        try:
            profile_data['updated_at'] = firestore.SERVER_TIMESTAMP
            
            user_ref = self.db.collection('users').document(user_id)
            user_ref.set(profile_data, merge=True)
            
            self.logger.info(f"Profile updated for user {user_id}")
            
        except Exception as e:
            self.logger.error(f"Error storing user profile: {e}")
            raise

    def get_user_medical_history(self, user_id: str) -> List[Dict]:
        """Get user's medical history (symptoms and diagnoses)"""
        try:
            medical_ref = self.db.collection('conversations')\
                .where('user_id', '==', user_id)\
                .where('message_type', '==', 'medical')\
                .order_by('created_at', direction=firestore.Query.DESCENDING)\
                .limit(20)
            
            medical_history = []
            for doc in medical_ref.stream():
                data = doc.to_dict()
                if 'disease_prediction' in data and data['disease_prediction']:
                    medical_entry = {
                        'date': data.get('timestamp', ''),
                        'symptoms': data.get('symptom_analysis', {}).get('symptoms', []),
                        'predicted_disease': data['disease_prediction']['disease'],
                        'severity': data['disease_prediction']['severity'],
                        'confidence': data['disease_prediction']['confidence']
                    }
                    medical_history.append(medical_entry)
            
            return medical_history
            
        except Exception as e:
            self.logger.error(f"Error getting medical history: {e}")
            return []

    def store_feedback(self, user_id: str, conversation_id: str, feedback: Dict):
        """Store user feedback"""
        try:
            feedback_data = {
                'user_id': user_id,
                'conversation_id': conversation_id,
                'feedback': feedback,
                'created_at': firestore.SERVER_TIMESTAMP
            }
            
            self.db.collection('feedback').add(feedback_data)
            self.logger.info(f"Feedback stored for user {user_id}")
            
        except Exception as e:
            self.logger.error(f"Error storing feedback: {e}")
            raise