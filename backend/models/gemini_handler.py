import google.generativeai as genai
import json
from typing import Dict, List
import logging
from config.settings import Config

class GeminiHandler:
    def __init__(self):
        self.config = Config()
        self.logger = logging.getLogger(__name__)
        
        # Configure Gemini
        genai.configure(api_key=self.config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-pro')
        
        # System prompts for different languages
        self.system_prompts = {
            'english': """You are Sehat Saathi, a friendly AI health assistant that speaks all Indian languages. 
Your role is to provide helpful health guidance while being empathetic and culturally sensitive.
Always remind users that you're not a replacement for professional medical advice.""",
            
            'hindi': """आप सेहत साथी हैं, एक मित्रवत AI स्वास्थ्य सहायक जो सभी भारतीय भाषाओं में बात करता है।
आपका काम सहायक स्वास्थ्य मार्गदर्शन प्रदान करना है।""",
            
            'tamil': """நீங்கள் சேகத் சாத்தி, அனைத்து இந்திய மொழிகளிலும் பேசும் ஒரு நட்பான AI சுகாதார உதவியாளர்.
உங்கள் பங்கு பயனுள்ள சுகாதார வழிகாட்டுதலை வழங்குவதாகும்."""
        }

    def generate_health_guidance(self, user_input: str, language: str) -> str:
        """Generate general health guidance response"""
        
        system_prompt = self.system_prompts.get(language, self.system_prompts['english'])
        
        prompt = f"""{system_prompt}

User message: "{user_input}"
Language: {language}

Please provide a helpful, empathetic response in {language}. If the user is asking about health topics:
1. Provide general health information
2. Suggest healthy lifestyle tips
3. Encourage consulting healthcare professionals for specific concerns
4. Be culturally sensitive to Indian context

Keep the response conversational and supportive."""

        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            self.logger.error(f"Gemini API error in health guidance: {e}")
            
            # Fallback responses
            fallback_responses = {
                'english': "I understand your concern. For the best guidance on your health, I recommend consulting with a healthcare professional who can provide personalized advice.",
                'hindi': "मैं आपकी चिंता समझता हूं। आपके स्वास्थ्य के लिए सबसे अच्छा मार्गदर्शन पाने के लिए, मैं किसी स्वास्थ्य विशेषज्ञ से सलाह लेने की सिफारिश करता हूं।",
                'tamil': "உங்கள் கவலையை நான் புரிந்துகொள்கிறேன். உங்கள் ஆரோக்கியத்திற்கான சிறந்த வழிகாட்டுதலுக்கு, தனிப்பட்ட ஆலோசனை வழங்கக்கூடிய சுகாதார நிபுணரை அணுகுமாறு பரிந்துரைக்கிறேன்."
            }
            
            return fallback_responses.get(language, fallback_responses['english'])

    def translate_response(self, text: str, target_language: str) -> str:
        """Translate response to target language"""
        
        if target_language == 'english':
            return text
        
        language_names = {
            'hindi': 'Hindi',
            'tamil': 'Tamil',
            'telugu': 'Telugu',
            'bengali': 'Bengali'
        }
        
        target_lang_name = language_names.get(target_language, 'Hindi')
        
        prompt = f"""Translate the following English text to {target_lang_name}. 
Maintain the medical context and be culturally appropriate for Indian users.

Text to translate: "{text}"

Provide only the translation, no explanations."""

        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            self.logger.error(f"Translation error: {e}")
            return text  # Return original if translation fails