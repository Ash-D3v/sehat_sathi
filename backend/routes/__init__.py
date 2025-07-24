# Routes package init
from .chat_routes import chat_bp
from .voice_routes import voice_bp  
from .health_routes import health_bp

__all__ = ['chat_bp', 'voice_bp', 'health_bp']