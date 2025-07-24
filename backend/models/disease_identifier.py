import torch
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from transformers import AutoModelForCausalLM, AutoTokenizer as ConvTokenizer
from typing import Dict, List
import logging
from config.settings import Config

class DiseaseIdentifier:
    def __init__(self):
        self.config = Config()
        self.logger = logging.getLogger(__name__)
        
        # Conversational backbone
        self.model_name = "microsoft/DialoGPT-medium"
        
        try:
            # Disease classification model
            self.classifier = pipeline(
                "text-classification",
                model="Zabihin/Symptom_to_Diagnosis",
                tokenizer="Zabihin/Symptom_to_Diagnosis",
                cache_dir=self.config.HUGGINGFACE_CACHE_DIR
            )
            
            # Conversational model for follow-up questions
            self.conv_tokenizer = ConvTokenizer.from_pretrained(
                self.model_name,
                cache_dir=self.config.HUGGINGFACE_CACHE_DIR
            )
            self.conv_model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                cache_dir=self.config.HUGGINGFACE_CACHE_DIR
            )
            
            self.logger.info("Disease identification models loaded successfully")
            
        except Exception as e:
            self.logger.error(f"Error loading models: {e}")
            raise

    def predict_disease(self, symptoms_list: List[str]) -> Dict:
        """Predict disease from list of symptoms"""
        try:
            # Prepare symptoms text
            symptoms_text = ", ".join(symptoms_list)
            
            # Get prediction from the model
            prediction = self.classifier(symptoms_text)
            
            # Extract top predictions
            if isinstance(prediction, list):
                top_prediction = prediction[0]
            else:
                top_prediction = prediction
            
            disease = top_prediction['label']
            confidence = top_prediction['score']
            
            # Assess severity based on disease type
            severity = self.assess_severity(disease)
            
            # Get additional info
            recommendations = self.get_recommendations(disease, severity)
            
            result = {
                "disease": disease,
                "confidence": round(confidence, 3),
                "severity": severity,
                "symptoms_analyzed": symptoms_list,
                "recommendations": recommendations,
                "requires_immediate_attention": severity == "high"
            }
            
            self.logger.info(f"Disease prediction: {disease} (confidence: {confidence})")
            return result
            
        except Exception as e:
            self.logger.error(f"Error in disease prediction: {e}")
            return {
                "disease": "Unable to determine",
                "confidence": 0.0,
                "severity": "medium",
                "symptoms_analyzed": symptoms_list,
                "recommendations": ["Please consult a healthcare professional"],
                "requires_immediate_attention": False,
                "error": str(e)
            }

    def assess_severity(self, disease: str) -> str:
        """Assess severity level of the predicted disease"""
        
        # High severity conditions - require immediate medical attention
        high_severity = [
            "heart attack", "stroke", "appendicitis", "heart failure",
            "pneumonia", "meningitis", "sepsis", "pulmonary embolism",
            "diabetic ketoacidosis", "severe allergic reaction",
            "acute coronary syndrome", "anaphylaxis"
        ]
        
        # Medium severity conditions - need medical consultation soon
        medium_severity = [
            "diabetes", "hypertension", "asthma", "bronchitis",
            "urinary tract infection", "gastritis", "migraine",
            "depression", "anxiety", "arthritis", "osteoporosis"
        ]
        
        # Low severity conditions - can be managed with care
        low_severity = [
            "common cold", "flu", "headache", "muscle strain",
            "minor cuts", "mild fever", "fatigue", "indigestion",
            "seasonal allergies", "minor skin irritation"
        ]
        
        disease_lower = disease.lower()
        
        for condition in high_severity:
            if condition in disease_lower:
                return "high"
        
        for condition in medium_severity:
            if condition in disease_lower:
                return "medium"
        
        for condition in low_severity:
            if condition in disease_lower:
                return "low"
        
        # Default to medium if unknown
        return "medium"

    def get_recommendations(self, disease: str, severity: str) -> List[str]:
        """Get recommendations based on disease and severity"""
        
        recommendations = []
        
        if severity == "high":
            recommendations.extend([
                "🚨 Seek immediate medical attention",
                "🏥 Go to the nearest emergency room",
                "📞 Call emergency services if symptoms worsen",
                "🚫 Do not delay medical treatment"
            ])
        elif severity == "medium":
            recommendations.extend([
                "👨‍⚕️ Schedule an appointment with a doctor",
                "📋 Monitor your symptoms closely",
                "💊 Follow prescribed medications if any",
                "🏥 Visit a clinic within 24-48 hours"
            ])
        else:  # low severity
            recommendations.extend([
                "🏠 Rest and take care of yourself",
                "💧 Stay hydrated",
                "🌡️ Monitor your temperature",
                "👨‍⚕️ Consult a doctor if symptoms persist"
            ])
        
        # Disease-specific recommendations
        disease_lower = disease.lower()
        
        if "fever" in disease_lower:
            recommendations.append("🌡️ Take temperature-reducing medication if needed")
        
        if "cough" in disease_lower:
            recommendations.append("🍯 Try warm liquids and honey")
        
        if "pain" in disease_lower:
            recommendations.append("💊 Consider over-the-counter pain relief")
        
        if "infection" in disease_lower:
            recommendations.append("🧼 Maintain good hygiene")
        
        return recommendations

    def generate_conversational_response(self, context: str, max_length: int = 100) -> str:
        """Generate conversational response using DialoGPT"""
        try:
            # Encode the context
            inputs = self.conv_tokenizer.encode(context + self.conv_tokenizer.eos_token, return_tensors='pt')
            
            # Generate response
            with torch.no_grad():
                outputs = self.conv_model.generate(
                    inputs,
                    max_length=max_length,
                    num_return_sequences=1,
                    pad_token_id=self.conv_tokenizer.eos_token_id,
                    do_sample=True,
                    temperature=0.7
                )
            
            # Decode the response
            response = self.conv_tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extract only the new part (after the input context)
            if context in response:
                response = response.replace(context, "").strip()
            
            return response
            
        except Exception as e:
            self.logger.error(f"Error in conversational response: {e}")
            return "I understand your concern. Let me help you with that."

    def get_follow_up_questions(self, disease: str, symptoms: List[str]) -> List[str]:
        """Generate follow-up questions based on predicted disease"""
        
        base_questions = [
            "How long have you been experiencing these symptoms?",
            "Have you taken any medication for this?",
            "Do you have any other symptoms not mentioned?",
            "Any family history of similar conditions?"
        ]
        
        # Disease-specific questions
        disease_lower = disease.lower()
        
        if "diabetes" in disease_lower:
            base_questions.extend([
                "Do you check your blood sugar regularly?",
                "Have you noticed increased thirst or urination?"
            ])
        
        if "heart" in disease_lower:
            base_questions.extend([
                "Do you experience chest pain during physical activity?",
                "Any shortness of breath?"
            ])
        
        if "infection" in disease_lower:
            base_questions.extend([
                "Do you have a fever?",
                "Any recent travel or exposure to illness?"
            ])
        
        return base_questions[:4]  # Return top 4 questions