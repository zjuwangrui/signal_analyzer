from flask import Flask
from flask_cors import CORS
from config import Config
from .utils.logging_config import setup_logging
import os

def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    CORS(app)
    
    # Load configuration
    app.config.from_object(Config)
    
    # Ensure instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Setup logging
    setup_logging(app.config['LOG_FOLDER'])

    # Register blueprints
    from .api.signal import signal_bp
    from .api.video import video_bp
    app.register_blueprint(signal_bp)
    app.register_blueprint(video_bp)

    return app
