import re
import json
from typing import List, Dict, Any
from datetime import datetime
import hashlib

def format_symptoms(symptoms: List[str]) -> str:
    """Format symptoms list into readable string"""
    if not symptoms:
        return "No symptoms provided"
    
    if len(symptoms) == 1:
        return symptoms[0]
    elif len(symptoms) == 2:
        return f"{symptoms[0]} and {symptoms[1]}"
    else:
        return f"{', '.join(symptoms[:-1])}, and {symptoms[-1]}"

def sanitize_input(text: str) -> str:
    """Sanitize user input"""
    if not text:
        return ""
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text.strip())
    
    # Remove potentially harmful characters
    text = re.sub(r'[<>\"\'%;()&+]', '', text)
    
    # Limit length
    if len(text) > 1000:
        text = text[:1000]
    
    return text

def generate_user_id(identifier: str = None) -> str:
    """Generate unique user ID"""
    if identifier:
        return hashlib.md5(identifier.encode()).hexdigest()
    else:
        return hashlib.md5(str(datetime.now()).encode()).hexdigest()

def parse_location_string(location_str: str) -> Dict:
    """Parse location string into coordinates"""
    try:
        # Expected format: "lat,lng" or JSON string
        if ',' in location_str and not location_str.startswith('{'):
            lat, lng = location_str.split(',')
            return {
                'lat': float(lat.strip()),
                'lng': float(lng.strip())
            }
        else:
            return json.loads(location_str)
    except:
        return {}

def format_distance(distance_km: float) -> str:
    """Format distance for display"""
    if distance_km < 1:
        return f"{int(distance_km * 1000)} m"
    else:
        return f"{distance_km:.1f} km"

def calculate_severity_score(symptoms: List[str], disease: str) -> int:
    """Calculate severity score (1-10)"""
    base_score = 3
    
    # High-risk symptoms
    high_risk_symptoms = [
        'chest pain', 'difficulty breathing', 'severe bleeding',
        'unconsciousness', 'severe headache', 'heart attack symptoms'
    ]
    
    # High-risk diseases
    high_risk_diseases = [
        'heart attack', 'stroke', 'appendicitis', 'pneumonia',
        'meningitis', 'sepsis'
    ]
    
    for symptom in symptoms:
        for high_risk in high_risk_symptoms:
            if high_risk.lower() in symptom.lower():
                base_score += 3
                break
    
    for high_risk in high_risk_diseases:
        if high_risk.lower() in disease.lower():
            base_score += 4
            break
    
    return min(base_score, 10)

def extract_medical_entities(text: str) -> Dict:
    """Extract medical entities from text"""
    medical_patterns = {
        'duration': r'(\d+)\s*(day|week|month|hour|minute)s?',
        'severity': r'(mild|moderate|severe|extreme|intense)',
        'frequency': r'(always|often|sometimes|rarely|never)',
        'body_parts': r'(head|chest|stomach|back|leg|arm|throat|eye)'
    }
    
    entities = {}
    for entity_type, pattern in medical_patterns.items():
        matches = re.findall(pattern, text.lower())
        if matches:
            entities[entity_type] = matches
    
    return entities

def create_response_template(message_type: str) -> Dict:
    """Create response template based on message type"""
    base_template = {
        'timestamp': datetime.now().isoformat(),
        'message_type': message_type,
        'bot_reply': '',
        'requires_immediate_attention': False
    }
    
    if message_type == 'medical':
        base_template.update({
            'disease_prediction': None,
            'symptom_analysis': {},
            'hospitals': [],
            'follow_up_questions': [],
            'urgency_level': 'low'
        })
    elif message_type == 'general':
        base_template.update({
            'suggestions': [],
            'health_tips': []
        })
    
    return base_template

def log_user_interaction(user_id: str, action: str, data: Dict = None):
    """Log user interaction for analytics"""
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'user_id': user_id,
        'action': action,
        'data': data or {}
    }
    
    # In production, this would go to a logging service
    print(f"USER_INTERACTION: {json.dumps(log_entry)}")

def is_emergency_keyword(text: str) -> bool:
    """Check if text contains emergency keywords"""
    emergency_words = [
        'emergency', 'urgent', 'help', 'ambulance', 'hospital',
        'chest pain', 'heart attack', 'stroke', 'bleeding',
        'unconscious', 'severe pain', 'can\'t breathe'
    ]
    
    text_lower = text.lower()
    return any(word in text_lower for word in emergency_words)