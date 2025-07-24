from typing import Dict, List
import logging
from datetime import datetime

from models.symptom_detector import SymptomDetector
from models.disease_identifier import DiseaseIdentifier
from models.gemini_handler import GeminiHandler
from services.location_service import LocationService
from services.database_service import DatabaseService

class ChatService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Initialize all components
        self.symptom_detector = SymptomDetector()
        self.disease_identifier = DiseaseIdentifier()
        self.gemini_handler = GeminiHandler()
        self.location_service = LocationService()
        self.database_service = DatabaseService()
        
        self.logger.info("ChatService initialized successfully")

    def process_message(self, user_input: str, user_id: str, location: Dict = None) -> Dict:
        """Main method to process user message"""
        try:
            # Step 1: Analyze input for symptoms
            symptom_analysis = self.symptom_detector.analyze_input(user_input)
            
            response_data = {
                "user_message": user_input,
                "timestamp": datetime.now().isoformat(),
                "user_id": user_id,
                "symptom_analysis": symptom_analysis
            }
            
            if symptom_analysis["has_symptoms"]:
                # Step 2: User has symptoms - process medical flow
                response_data.update(self._process_medical_flow(symptom_analysis, location))
            else:
                # Step 3: General conversation
                response_data.update(self._process_general_conversation(user_input, symptom_analysis["original_language"]))
            
            # Step 4: Store conversation in database
            self._store_conversation(user_id, response_data)
            
            return response_data
            
        except Exception as e:
            self.logger.error(f"Error processing message: {e}")
            return self._create_error_response(str(e))

    def _process_medical_flow(self, symptom_analysis: Dict, location: Dict = None) -> Dict:
        """Process medical-related conversation"""
        symptoms = symptom_analysis["symptoms"]
        language = symptom_analysis["original_language"]
        urgency = symptom_analysis["urgency"]
        
        # Get disease prediction
        disease_prediction = self.disease_identifier.predict_disease(symptoms)
        
        # Generate appropriate response based on urgency
        if urgency == "high" or disease_prediction["severity"] == "high":
            bot_reply = self._generate_emergency_response(disease_prediction, language)
            hospitals = []
            
            # Find nearby hospitals if location provided
            if location:
                hospitals = self.location_service.find_nearby_hospitals(location, "high")
        
        else:
            # Generate helpful medical advice
            bot_reply = self._generate_medical_advice_response(disease_prediction, language)
            hospitals = []
            
            if location and disease_prediction["severity"] == "medium":
                hospitals = self.location_service.find_nearby_hospitals(location, "medium")
        
        # Get follow-up questions
        follow_up_questions = self.disease_identifier.get_follow_up_questions(
            disease_prediction["disease"], 
            symptoms
        )
        
        return {
            "message_type": "medical",
            "bot_reply": bot_reply,
            "disease_prediction": disease_prediction,
            "hospitals": hospitals,
            "follow_up_questions": follow_up_questions,
            "urgency_level": urgency,
            "requires_immediate_attention": disease_prediction["requires_immediate_attention"]
        }

    def _process_general_conversation(self, user_input: str, language: str) -> Dict:
        """Process general conversation"""
        
        # Use Gemini for general health guidance
        bot_reply = self.gemini_handler.generate_health_guidance(user_input, language)
        
        return {
            "message_type": "general",
            "bot_reply": bot_reply,
            "disease_prediction": None,
            "hospitals": [],
            "follow_up_questions": [],
            "urgency_level": "none",
            "requires_immediate_attention": False
        }

    def _generate_emergency_response(self, disease_prediction: Dict, language: str) -> str:
        """Generate emergency response message"""
        
        emergency_messages = {
            'english': f"""🚨 URGENT: Based on your symptoms, you may have {disease_prediction['disease']}. 
This requires IMMEDIATE medical attention. Please:
1. Go to the nearest emergency room immediately
2. Call emergency services (108) if symptoms worsen
3. Do not delay seeking medical help

{' '.join(disease_prediction['recommendations'])}""",
            
            'hindi': f"""🚨 तत्काल: आपके लक्षणों के आधार पर, आपको {disease_prediction['disease']} हो सकता है।
इसके लिए तुरंत चिकित्सा सहायता की आवश्यकता है। कृपया:
1. तुरंत निकटतम अस्पताल जाएं
2. यदि लक्षण बढ़ें तो आपातकालीन सेवाओं (108) को कॉल करें
3. चिकित्सा सहायता लेने में देरी न करें""",
            
            'tamil': f"""🚨 அவசரம்: உங்கள் அறிகுறிகளின் அடிப்படையில், உங்களுக்கு {disease_prediction['disease']} இருக்கலாம்.
இதற்கு உடனடி மருத்துவ கவனிப்பு தேவை. தயவுசெய்து:
1. உடனடியாக அருகிலுள்ள மருத்துவமனைக்கு செல்லுங்கள்
2. அறிகுறிகள் மோசமாகினால் அவசர சேவைகளை (108) அழைக்கவும்"""
        }
        
        return emergency_messages.get(language, emergency_messages['english'])

    def _generate_medical_advice_response(self, disease_prediction: Dict, language: str) -> str:
        """Generate medical advice response"""
        
        advice_templates = {
            'english': f"""Based on your symptoms, you might have {disease_prediction['disease']} (confidence: {disease_prediction['confidence']:.0%}).

Severity Level: {disease_prediction['severity'].upper()}

Recommendations:
{chr(10).join(disease_prediction['recommendations'])}

Please consult with a healthcare professional for proper diagnosis and treatment.""",
            
            'hindi': f"""आपके लक्षणों के आधार पर, आपको {disease_prediction['disease']} हो सकता है (विश्वास: {disease_prediction['confidence']:.0%})।

गंभीरता स्तर: {disease_prediction['severity'].upper()}

सिफारिशें:
{chr(10).join(disease_prediction['recommendations'])}

उचित निदान और उपचार के लिए कृपया किसी स्वास्थ्य विशेषज्ञ से सलाह लें।""",
            
            'tamil': f"""உங்கள் அறிகுறிகளின் அடிப்படையில், உங்களுக்கு {disease_prediction['disease']} இருக்கலாம் (நம்பிக்கை: {disease_prediction['confidence']:.0%})।

தீவிர நிலை: {disease_prediction['severity'].upper()}

பரிந்துரைகள்:
{chr(10).join(disease_prediction['recommendations'])}

சரியான நோயறிதல் மற்றும் சிகிச்சைக்காக மருத்துவ நிபுணரை அணுகவும்."""
        }
        
        return advice_templates.get(language, advice_templates['english'])

    def _store_conversation(self, user_id: str, conversation_data: Dict):
        """Store conversation in Firebase"""
        try:
            self.database_service.store_conversation(user_id, conversation_data)
        except Exception as e:
            self.logger.error(f"Error storing conversation: {e}")

    def _create_error_response(self, error_message: str) -> Dict:
        """Create error response"""
        return {
            "message_type": "error",
            "bot_reply": "I'm sorry, I encountered an error while processing your message. Please try again.",
            "error": error_message,
            "disease_prediction": None,
            "hospitals": [],
            "follow_up_questions": [],
            "urgency_level": "none",
            "requires_immediate_attention": False
        }

    def get_user_history(self, user_id: str) -> Dict:
        """Get user's conversation history"""
        try:
            return self.database_service.get_user_history(user_id)
        except Exception as e:
            self.logger.error(f"Error getting user history: {e}")
            return {}