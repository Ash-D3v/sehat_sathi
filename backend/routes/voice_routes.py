from flask import Blueprint, request, jsonify, send_file
import logging
import io
from services.voice_service import VoiceService
from services.chat_service import ChatService
from utils.validators import validate_audio_data, validate_user_input

voice_bp = Blueprint('voice', __name__)
logger = logging.getLogger(__name__)

# Initialize services
voice_service = VoiceService()
chat_service = ChatService()

@voice_bp.route('/speech-to-text', methods=['POST'])
def speech_to_text():
    """Convert speech to text"""
    try:
        # Check if audio file is present
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400
        
        audio_file = request.files['audio']
        if audio_file.filename == '':
            return jsonify({'error': 'No audio file selected'}), 400
        
        # Read audio data
        audio_data = audio_file.read()
        
        # Validate audio data
        is_valid, error_msg = validate_audio_data(audio_data)
        if not is_valid:
            return jsonify({'error': error_msg}), 400
        
        # Get language parameter
        language = request.form.get('language', 'en-IN')
        
        # Process audio
        result = voice_service.speech_to_text(audio_data, language)
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in voice chat: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@voice_bp.route('/supported-languages', methods=['GET'])
def get_supported_languages():
    """Get list of supported languages for voice"""
    return jsonify({
        'languages': voice_service.language_codes,
        'default': 'english'
    })