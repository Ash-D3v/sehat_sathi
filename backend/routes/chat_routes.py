from flask import Blueprint, request, jsonify
import logging
from services.chat_service import ChatService

chat_bp = Blueprint('chat', __name__)
logger = logging.getLogger(__name__)

# Initialize chat service
chat_service = ChatService()

@chat_bp.route('/message', methods=['POST'])
def send_message():
    """Main chat endpoint"""
    try:
        data = request.get_json()
        
        # Validate input
        if not data or 'message' not in data or 'user_id' not in data:
            return jsonify({'error': 'Missing required fields: message, user_id'}), 400
        
        user_message = data['message'].strip()
        user_id = data['user_id']
        location = data.get('location', None)
        
        if not user_message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        # Process message
        response = chat_service.process_message(user_message, user_id, location)
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@chat_bp.route('/history/<user_id>', methods=['GET'])
def get_chat_history(user_id):
    """Get user's chat history"""
    try:
        limit = request.args.get('limit', 10, type=int)
        history = chat_service.get_user_history(user_id)
        
        return jsonify(history)
        
    except Exception as e:
        logger.error(f"Error getting chat history: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@chat_bp.route('/feedback', methods=['POST'])
def submit_feedback():
    """Submit user feedback"""
    try:
        data = request.get_json()
        
        if not data or 'user_id' not in data or 'feedback' not in data:
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Store feedback (implement in chat_service)
        # chat_service.store_feedback(data)
        
        return jsonify({'message': 'Feedback received successfully'})
        
    except Exception as e:
        logger.error(f"Error submitting feedback: {e}")
        return jsonify({'error': 'Internal server error'}), 500