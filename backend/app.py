from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import os
from datetime import datetime

# Import services
from services.chat_service import ChatService
from services.voice_service import VoiceService
from config.settings import Config

# Import routes
from routes.chat_routes import chat_bp
from routes.voice_routes import voice_bp
from routes.health_routes import health_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Enable CORS
    CORS(app, origins=["http://localhost:3000", "https://your-frontend-domain.com"])
    
    # Setup logging
    setup_logging()
    
    # Register blueprints
    app.register_blueprint(chat_bp, url_prefix='/api/chat')
    app.register_blueprint(voice_bp, url_prefix='/api/voice')
    app.register_blueprint(health_bp, url_prefix='/api/health')
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0'
        })
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Endpoint not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500
    
    return app

def setup_logging():
    """Setup application logging"""
    os.makedirs('./logs', exist_ok=True)
    
    logging.basicConfig(
        level=getattr(logging, Config.LOG_LEVEL),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(Config.LOG_FILE),
            logging.StreamHandler()
        ]
    )

if __name__ == '__main__':
    app = create_app()
    app.run(debug=Config.FLASK_DEBUG, host='0.0.0.0', port=5000)