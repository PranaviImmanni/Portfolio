"""
Flask API Application
Serves object detection and EV failure prediction endpoints
"""
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from pathlib import Path
from config import API_CONFIG
from src.api.routes import register_routes
from src.utils.logger import get_logger

logger = get_logger(__name__)

def create_app():
    """Create and configure Flask application"""
    app = Flask(__name__)
    CORS(app)
    
    # Configure app
    app.config['MAX_CONTENT_LENGTH'] = API_CONFIG['max_upload_size']
    app.config['UPLOAD_FOLDER'] = Path('data/raw/uploads')
    app.config['ALLOWED_EXTENSIONS'] = API_CONFIG['allowed_extensions']
    
    # Create upload directory
    app.config['UPLOAD_FOLDER'].mkdir(parents=True, exist_ok=True)
    
    # Register routes
    register_routes(app)
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Endpoint not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500
    
    @app.route('/health', methods=['GET'])
    def health_check():
        """Health check endpoint"""
        return jsonify({
            'status': 'healthy',
            'service': 'Autonomous Vehicle Vision & EV Analytics API',
            'version': '1.0.0'
        })
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(
        host=API_CONFIG['host'],
        port=API_CONFIG['port'],
        debug=API_CONFIG['debug']
    )

