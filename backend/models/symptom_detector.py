import re
import json
from typing import List, Dict, Tuple
from langdetect import detect
import google.generativeai as genai
from config.settings import Config

class SymptomDetector:
    def __init__(self):
        self.config = Config()
        genai.configure(api_key=self.config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-pro')
        
        # Common symptom keywords in multiple languages
        self.symptom_keywords = {
            'english': [
                'pain', 'ache', 'hurt', 'fever', 'cough', 'cold', 'headache',
                'nausea', 'vomiting', 'diarrhea', 'constipation', 'bleeding',
                'swelling', 'rash', 'itching', 'burning', 'numbness', 'weakness',
                'dizziness', 'fatigue', 'tired', 'breathless', 'chest pain',
                'stomach pain', 'back pain', 'joint pain', 'sore throat',
                'runny nose', 'sneezing', 'chills', 'sweating', 'cramps'
            ],
            'hindi': [
                'दर्द', 'पीड़ा', 'बुखार', 'खांसी', 'सर्दी', 'सिरदर्द',
                'जी मिचलाना', 'उल्टी', 'दस्त', 'कब्ज', 'खून', 'सूजन',
                'खुजली', 'जलन', 'सुन्नता', 'कमजोरी', 'चक्कर', 'थकान',
                'सांस फूलना', 'सीने में दर्द', 'पेट दर्द', 'कमर दर्द'
            ],
            'tamil': [
                'வலி', 'காய்ச்சல்', 'இருமல்', 'சளி', 'தலைவலி',
                'குமட்டல்', 'வாந்தி', 'வயிற்றுப்போக்கு', 'மலச்சிக்கல்',
                'இரத்தம்', 'வீக்கம்', 'அரிப்பு', 'எரிச்சல்', 'பலவீனம்'
            ],
            'telugu': [
                'నొప్పి', 'జ్వరం', 'దగ్గు', 'జలుబు', 'తలనొప్పి',
                'వాంతులు', 'విరేచనలు', 'మలబద్దకం', 'రక్తం', 'వాపు'
            ],
            'bengali': [
                'ব্যথা', 'জ্বর', 'কাশি', 'সর্দি', 'মাথাব্যথা',
                'বমি', 'ডায়রিয়া', 'কোষ্ঠকাঠিন্য', 'রক্ত', 'ফোলা'
            ]
        }
        
        # Medical context patterns
        self.medical_patterns = [
            r'\b(feeling|feel)\s+(sick|unwell|ill|bad)\b',
            r'\b(have|having|got)\s+(a|an)?\s*(fever|cold|cough|headache)\b',
            r'\b(pain|ache|hurt|hurts|hurting)\b',
            r'\b(doctor|hospital|medicine|treatment|symptoms?)\b',
            r'\b(since|for)\s+\d+\s+(days?|weeks?|months?|hours?)\b',
            r'\b(getting\s+worse|not\s+feeling\s+well)\b'
        ]

    def detect_language(self, text: str) -> str:
        """Detect the language of input text"""
        try:
            detected = detect(text)
            language_map = {
                'hi': 'hindi',
                'ta': 'tamil',
                'te': 'telugu',
                'bn': 'bengali',
                'en': 'english'
            }
            return language_map.get(detected, 'english')
        except:
            return 'english'

    def keyword_based_detection(self, text: str, language: str) -> bool:
        """Check if text contains symptom keywords"""
        text_lower = text.lower()
        keywords = self.symptom_keywords.get(language, self.symptom_keywords['english'])
        
        # Check for direct keyword matches
        for keyword in keywords:
            if keyword in text_lower:
                return True
        
        # Check for medical context patterns (mainly for English)
        if language == 'english':
            for pattern in self.medical_patterns:
                if re.search(pattern, text_lower):
                    return True
        
        return False

    def gemini_symptom_detection(self, text: str, language: str) -> Dict:
        """Use Gemini to detect symptoms and extract them"""
        
        language_prompts = {
            'hindi': 'हिंदी',
            'tamil': 'தமிழ்',
            'telugu': 'తెలుగు',
            'bengali': 'বাংলা',
            'english': 'English'
        }
        
        lang_name = language_prompts.get(language, 'English')
        
        prompt = f"""
You are a medical AI assistant. Analyze the following {lang_name} text and determine:

1. Does this text mention any health symptoms or medical complaints?
2. If yes, extract all symptoms mentioned and translate them to English
3. Determine the urgency level (low/medium/high)

Text to analyze: "{text}"

Respond in this exact JSON format:
{{
    "has_symptoms": true/false,
    "symptoms": ["symptom1", "symptom2"],
    "original_language": "{language}",
    "urgency": "low/medium/high",
    "medical_context": true/false,
    "confidence": 0.0-1.0
}}

Rules:
- Only return true for has_symptoms if the text clearly mentions health issues
- Extract symptoms in simple English terms
- High urgency: chest pain, difficulty breathing, severe bleeding, unconsciousness
- Medium urgency: persistent fever, severe pain, bleeding
- Low urgency: mild symptoms, general discomfort
"""

        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Clean the response to extract JSON
            if '```json' in response_text:
                response_text = response_text.split('```json')[1].split('```')[0]
            elif '```' in response_text:
                response_text = response_text.split('```')[1].split('```')[0]
            
            result = json.loads(response_text)
            return result
            
        except Exception as e:
            print(f"Gemini API error: {e}")
            # Fallback to keyword detection
            has_symptoms = self.keyword_based_detection(text, language)
            return {
                "has_symptoms": has_symptoms,
                "symptoms": [],
                "original_language": language,
                "urgency": "low",
                "medical_context": has_symptoms,
                "confidence": 0.5
            }

    def analyze_input(self, user_input: str) -> Dict:
        """Main method to analyze user input for symptoms"""
        
        # Step 1: Detect language
        language = self.detect_language(user_input)
        
        # Step 2: Quick keyword check for efficiency
        has_keywords = self.keyword_based_detection(user_input, language)
        
        # Step 3: If keywords found or uncertain, use Gemini for detailed analysis
        if has_keywords or len(user_input.split()) > 3:
            result = self.gemini_symptom_detection(user_input, language)
        else:
            result = {
                "has_symptoms": False,
                "symptoms": [],
                "original_language": language,
                "urgency": "low",
                "medical_context": False,
                "confidence": 0.9
            }
        
        # Step 4: Add metadata
        result['input_text'] = user_input
        result['detection_method'] = 'gemini' if result.get('confidence', 0) > 0.7 else 'keyword'
        
        return result

    def get_follow_up_questions(self, symptoms: List[str], language: str) -> List[str]:
        """Generate follow-up questions based on detected symptoms"""
        
        questions_map = {
            'english': [
                "How long have you been experiencing these symptoms?",
                "On a scale of 1-10, how would you rate the severity?",
                "Are you taking any medications currently?",
                "Do you have any allergies?"
            ],
            'hindi': [
                "यह लक्षण कितने दिनों से हैं?",
                "1-10 के पैमाने पर, आप इसकी गंभीरता को कैसे आंकेंगे?",
                "क्या आप कोई दवा ले रहे हैं?",
                "क्या आपको कोई एलर्जी है?"
            ],
            'tamil': [
                "இந்த அறிகுறிகள் எத்தனை நாட்களாக உள்ளன?",
                "1-10 அளவில், தீவிரத்தை எப்படி மதிப்பிடுவீர்கள்?",
                "தற்போது ஏதேனும் மருந்துகள் எடுத்துக்கொள்கிறீர்களா?",
                "ஏதேனும் ஒவ்வாமை உள்ளதா?"
            ]
        }
        
        return questions_map.get(language, questions_map['english'])