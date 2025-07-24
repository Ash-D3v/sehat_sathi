# Application constants

# Supported languages
SUPPORTED_LANGUAGES = {
    'english': 'en',
    'hindi': 'hi', 
    'tamil': 'ta',
    'telugu': 'te',
    'bengali': 'bn'
}

# Emergency keywords that trigger immediate attention
EMERGENCY_KEYWORDS = [
    'chest pain', 'heart attack', 'stroke', 'difficulty breathing',
    'severe bleeding', 'unconscious', 'overdose', 'poisoning',
    'severe allergic reaction', 'anaphylaxis', 'suicide',
    'emergency', 'ambulance', 'help me', 'dying'
]

# Severity levels
SEVERITY_LEVELS = {
    'LOW': 1,
    'MEDIUM': 2, 
    'HIGH': 3,
    'CRITICAL': 4
}

# Disease categories
DISEASE_CATEGORIES = {
    'respiratory': ['asthma', 'pneumonia', 'bronchitis', 'cold', 'flu'],
    'cardiovascular': ['heart attack', 'hypertension', 'heart failure'],
    'neurological': ['migraine', 'stroke', 'seizure', 'headache'],
    'gastrointestinal': ['gastritis', 'ulcer', 'diarrhea', 'constipation'],
    'infectious': ['infection', 'fever', 'flu', 'covid'],
    'musculoskeletal': ['arthritis', 'back pain', 'muscle strain']
}

# Indian emergency numbers
EMERGENCY_NUMBERS = {
    'national': '108',
    'police': '100',
    'fire': '101',
    'women_helpline': '1091',
    'child_helpline': '1098'
}

# Common symptoms in Indian languages
SYMPTOM_TRANSLATIONS = {
    'english': {
        'fever': 'fever',
        'headache': 'headache', 
        'cough': 'cough',
        'pain': 'pain',
        'nausea': 'nausea'
    },
    'hindi': {
        'fever': 'बुखार',
        'headache': 'सिरदर्द',
        'cough': 'खांसी', 
        'pain': 'दर्द',
        'nausea': 'जी मिचलाना'
    },
    'tamil': {
        'fever': 'காய்ச்சல்',
        'headache': 'தலைவலி',
        'cough': 'இருமல்',
        'pain': 'வலி', 
        'nausea': 'குமட்டல்'
    }
}

# Response templates
RESPONSE_TEMPLATES = {
    'greeting': {
        'english': "Hello! I'm Sehat Saathi, your health assistant. How can I help you today?",
        'hindi': "नमस्ते! मैं सेहत साथी हूं, आपका स्वास्थ्य सहायक। आज मैं आपकी कैसे मदद कर सकता हूं?",
        'tamil': "வணக்கம்! நான் சேகத் சாத்தி, உங்கள் சுகாதார உதவியாளர். இன்று உங்களுக்கு எப்படி உதவ முடியும்?"
    },
    'emergency': {
        'english': "🚨 This seems like an emergency. Please call 108 immediately or go to the nearest hospital.",
        'hindi': "🚨 यह एक आपातकालीन स्थिति लगती है। कृपया तुरंत 108 पर कॉल करें या निकटतम अस्पताल जाएं।",
        'tamil': "🚨 இது அவசர நிலை போல் தெரிகிறது. உடனடியாக 108 ஐ அழைக்கவும் அல்லது அருகிலுள்ள மருத்துவமனைக்கு செல்லவும்."
    }
}

# API Configuration
API_CONFIG = {
    'max_request_size': 16 * 1024 * 1024,  # 16MB
    'request_timeout': 30,  # seconds
    'rate_limit': 100,  # requests per hour per user
    'max_conversation_history': 50
}

# Model Configuration
MODEL_CONFIG = {
    'symptom_confidence_threshold': 0.7,
    'disease_confidence_threshold': 0.6,
    'max_symptoms_per_request': 20,
    'max_follow_up_questions': 5
}

# Hospital search parameters
HOSPITAL_SEARCH = {
    'emergency_radius': 10000,  # 10km for emergencies
    'regular_radius': 5000,     # 5km for regular consultations
    'max_results': 10,
    'required_rating': 3.0
}

# Voice processing settings
VOICE_CONFIG = {
    'max_audio_duration': 60,  # seconds
    'sample_rate': 16000,
    'supported_formats': ['wav', 'mp3', 'ogg'],
    'max_audio_size': 10 * 1024 * 1024  # 10MB
}

# Database collection names
DB_COLLECTIONS = {
    'users': 'users',
    'conversations': 'conversations', 
    'feedback': 'feedback',
    'medical_history': 'medical_history',
    'analytics': 'analytics'
}

# Logging configuration
LOG_CONFIG = {
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'max_file_size': 10 * 1024 * 1024,  # 10MB
    'backup_count': 5
}