import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Keys
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')
    
    # Firebase
    FIREBASE_KEY_PATH = os.getenv('FIREBASE_KEY_PATH')
    FIREBASE_PROJECT_ID = os.getenv('FIREBASE_PROJECT_ID')
    
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-secret-key')
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    # Models
    HUGGINGFACE_CACHE_DIR = os.getenv('HUGGINGFACE_CACHE_DIR', './models_cache')
    SYMPTOM_MODEL_NAME = os.getenv('SYMPTOM_MODEL_NAME', 'Zabihin/Symptom_to_Diagnosis')
    CONVERSATIONAL_MODEL = os.getenv('CONVERSATIONAL_MODEL', 'microsoft/DialoGPT-medium')
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', './logs/app.log')