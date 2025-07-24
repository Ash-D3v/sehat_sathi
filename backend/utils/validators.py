import re
from typing import Dict, List, Optional, Tuple

def validate_user_input(data: Dict) -> Tuple[bool, str]:
    """Validate user input data"""
    required_fields = ['message', 'user_id']
    
    # Check required fields
    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"
        
        if not data[field] or not str(data[field]).strip():
            return False, f"Field {field} cannot be empty"
    
    # Validate message length
    message = data['message'].strip()
    if len(message) > 1000:
        return False, "Message too long (max 1000 characters)"
    
    if len(message) < 1:
        return False, "Message too short"
    
    # Validate user_id format
    user_id = data['user_id']
    if not re.match(r'^[a-zA-Z0-9_-]+$', user_id):
        return False, "Invalid user_id format"
    
    return True, "Valid input"

def validate_location_data(location: Dict) -> Tuple[bool, str]:
    """Validate location data"""
    if not location:
        return True, "No location provided"  # Location is optional
    
    required_coords = ['lat', 'lng']
    for coord in required_coords:
        if coord not in location:
            return False, f"Missing coordinate: {coord}"
        
        try:
            coord_value = float(location[coord])
            if coord == 'lat' and not (-90 <= coord_value <= 90):
                return False, "Invalid latitude range"
            elif coord == 'lng' and not (-180 <= coord_value <= 180):
                return False, "Invalid longitude range"
        except (ValueError, TypeError):
            return False, f"Invalid {coord} format"
    
    return True, "Valid location"

def validate_symptoms_list(symptoms: List[str]) -> Tuple[bool, str]:
    """Validate symptoms list"""
    if not symptoms:
        return True, "No symptoms provided"  # Can be empty
    
    if len(symptoms) > 20:
        return False, "Too many symptoms (max 20)"
    
    for symptom in symptoms:
        if not isinstance(symptom, str):
            return False, "All symptoms must be strings"
        
        if len(symptom.strip()) < 2:
            return False, "Symptom too short"
        
        if len(symptom) > 100:
            return False, "Symptom too long (max 100 characters)"
    
    return True, "Valid symptoms"

def validate_audio_data(audio_data: bytes) -> Tuple[bool, str]:
    """Validate audio data"""
    if not audio_data:
        return False, "No audio data provided"
    
    # Check file size (max 10MB)
    max_size = 10 * 1024 * 1024  # 10MB
    if len(audio_data) > max_size:
        return False, "Audio file too large (max 10MB)"
    
    # Check minimum size (1KB)
    if len(audio_data) < 1024:
        return False, "Audio file too small"
    
    return True, "Valid audio data"

def validate_language_code(language: str) -> Tuple[bool, str]:
    """Validate language code"""
    supported_languages = [
        'english', 'hindi', 'tamil', 'telugu', 'bengali'
    ]
    
    if language not in supported_languages:
        return False, f"Unsupported language. Supported: {', '.join(supported_languages)}"
    
    return True, "Valid language"

def sanitize_phone_number(phone: str) -> str:
    """Sanitize and format phone number"""
    # Remove all non-digits
    phone = re.sub(r'\D', '', phone)
    
    # Handle Indian numbers
    if phone.startswith('91') and len(phone) == 12:
        return f"+{phone}"
    elif len(phone) == 10:
        return f"+91{phone}"
    
    return phone

def validate_feedback_data(feedback: Dict) -> Tuple[bool, str]:
    """Validate feedback data"""
    required_fields = ['rating', 'message']
    
    for field in required_fields:
        if field not in feedback:
            return False, f"Missing required field: {field}"
    
    # Validate rating
    try:
        rating = int(feedback['rating'])
        if not (1 <= rating <= 5):
            return False, "Rating must be between 1 and 5"
    except (ValueError, TypeError):
        return False, "Invalid rating format"
    
    # Validate message
    message = feedback['message'].strip()
    if len(message) > 500:
        return False, "Feedback message too long (max 500 characters)"
    
    return True, "Valid feedback"

def is_valid_email(email: str) -> bool:
    """Check if email is valid"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_user_profile(profile: Dict) -> Tuple[bool, str]:
    """Validate user profile data"""
    optional_fields = {
        'name': (str, 2, 50),
        'age': (int, 1, 120),
        'email': (str, 5, 100),
        'phone': (str, 10, 15)
    }
    
    for field, (field_type, min_val, max_val) in optional_fields.items():
        if field in profile:
            value = profile[field]
            
            if not isinstance(value, field_type):
                return False, f"Invalid type for {field}"
            
            if field_type == str:
                if len(value) < min_val or len(value) > max_val:
                    return False, f"Invalid length for {field}"
                
                if field == 'email' and not is_valid_email(value):
                    return False, "Invalid email format"
            
            elif field_type == int:
                if value < min_val or value > max_val:
                    return False, f"Invalid range for {field}"
    
    return True, "Valid profile"