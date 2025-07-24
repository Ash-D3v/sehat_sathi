from flask import Blueprint, request, jsonify
import logging
from services.location_service import LocationService
from services.database_service import DatabaseService
from utils.validators import validate_location_data, validate_user_profile

health_bp = Blueprint('health', __name__)
logger = logging.getLogger(__name__)

# Initialize services
location_service = LocationService()
database_service = DatabaseService()

@health_bp.route('/hospitals/nearby', methods=['POST'])
def find_nearby_hospitals():
    """Find nearby hospitals based on location and severity"""
    try:
        data = request.get_json()
        
        if not data or 'location' not in data:
            return jsonify({'error': 'Location is required'}), 400
        
        location = data['location']
        severity = data.get('severity', 'medium')
        
        # Validate location
        is_valid, error_msg = validate_location_data(location)
        if not is_valid:
            return jsonify({'error': error_msg}), 400
        
        # Find hospitals
        hospitals = location_service.find_nearby_hospitals(location, severity)
        
        return jsonify({
            'hospitals': hospitals,
            'total_found': len(hospitals),
            'search_location': location,
            'severity': severity
        })
        
    except Exception as e:
        logger.error(f"Error finding hospitals: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@health_bp.route('/emergency-contacts/<city>', methods=['GET'])
def get_emergency_contacts(city):
    """Get emergency contacts for a city"""
    try:
        contacts = location_service.get_emergency_contacts(city)
        
        return jsonify({
            'city': city,
            'emergency_contacts': contacts,
            'national_emergency': '108'
        })
        
    except Exception as e:
        logger.error(f"Error getting emergency contacts: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@health_bp.route('/directions', methods=['POST'])
def get_directions():
    """Get directions between origin and destination"""
    try:
        data = request.get_json()
        
        required_fields = ['origin', 'destination']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'{field} is required'}), 400
        
        # Validate locations
        for field in required_fields:
            is_valid, error_msg = validate_location_data(data[field])
            if not is_valid:
                return jsonify({'error': f'Invalid {field}: {error_msg}'}), 400
        
        # Get directions
        directions = location_service.get_directions(data['origin'], data['destination'])
        
        return jsonify({
            'directions': directions,
            'origin': data['origin'],
            'destination': data['destination']
        })
        
    except Exception as e:
        logger.error(f"Error getting directions: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@health_bp.route('/user/<user_id>/profile', methods=['GET', 'POST'])
def user_profile(user_id):
    """Get or update user profile"""
    try:
        if request.method == 'GET':
            # Get user profile
            history = database_service.get_user_history(user_id)
            user_data = history.get('user_data', {})
            
            return jsonify({
                'user_id': user_id,
                'profile': user_data
            })
        
        elif request.method == 'POST':
            # Update user profile
            data = request.get_json()
            
            if not data:
                return jsonify({'error': 'No profile data provided'}), 400
            
            # Validate profile data
            is_valid, error_msg = validate_user_profile(data)
            if not is_valid:
                return jsonify({'error': error_msg}), 400
            
            # Store profile
            database_service.store_user_profile(user_id, data)
            
            return jsonify({
                'message': 'Profile updated successfully',
                'user_id': user_id
            })
            
    except Exception as e:
        logger.error(f"Error with user profile: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@health_bp.route('/user/<user_id>/medical-history', methods=['GET'])
def get_medical_history(user_id):
    """Get user's medical history"""
    try:
        medical_history = database_service.get_user_medical_history(user_id)
        
        return jsonify({
            'user_id': user_id,
            'medical_history': medical_history,
            'total_entries': len(medical_history)
        })
        
    except Exception as e:
        logger.error(f"Error getting medical history: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@health_bp.route('/feedback', methods=['POST'])
def submit_feedback():
    """Submit user feedback"""
    try:
        data = request.get_json()
        
        required_fields = ['user_id', 'feedback']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'{field} is required'}), 400
        
        user_id = data['user_id']
        feedback = data['feedback']
        conversation_id = data.get('conversation_id', '')
        
        # Validate feedback
        from utils.validators import validate_feedback_data
        is_valid, error_msg = validate_feedback_data(feedback)
        if not is_valid:
            return jsonify({'error': error_msg}), 400
        
        # Store feedback
        database_service.store_feedback(user_id, conversation_id, feedback)
        
        return jsonify({'message': 'Feedback submitted successfully'})
        
    except Exception as e:
        logger.error(f"Error submitting feedback: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@health_bp.route('/health-tips', methods=['GET'])
def get_health_tips():
    """Get general health tips"""
    try:
        language = request.args.get('language', 'english')
        category = request.args.get('category', 'general')
        
        # Health tips database
        health_tips = {
            'general': {
                'english': [
                    "Drink at least 8 glasses of water daily",
                    "Exercise for 30 minutes daily",
                    "Get 7-8 hours of sleep",
                    "Eat a balanced diet with fruits and vegetables",
                    "Practice stress management techniques"
                ],
                'hindi': [
                    "दिन में कम से कम 8 गिलास पानी पिएं",
                    "रोज 30 मिनट व्यायाम करें",
                    "7-8 घंटे की नींद लें",
                    "फल और सब्जियों के साथ संतुलित आहार लें",
                    "तनाव प्रबंधन तकनीकों का अभ्यास करें"
                ]
            },
            'diet': {
                'english': [
                    "Include seasonal fruits in your diet",
                    "Limit processed foods and sugar",
                    "Eat smaller, frequent meals",
                    "Include protein in every meal"
                ]
            }
        }
        
        tips = health_tips.get(category, {}).get(language, 
                health_tips.get('general', {}).get('english', []))
        
        return jsonify({
            'category': category,
            'language': language,
            'tips': tips
        })
        
    except Exception as e:
        logger.error(f"Error getting health tips: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@health_bp.route('/symptoms/common', methods=['GET'])
def get_common_symptoms():
    """Get list of common symptoms"""
    try:
        language = request.args.get('language', 'english')
        
        from utils.constants import SYMPTOM_TRANSLATIONS
        
        symptoms = SYMPTOM_TRANSLATIONS.get(language, 
                  SYMPTOM_TRANSLATIONS.get('english', {}))
        
        return jsonify({
            'language': language,
            'symptoms': symptoms
        })
        
    except Exception as e:
        logger.error(f"Error getting symptoms: {e}")
        return jsonify({'error': 'Internal server error'}), 500