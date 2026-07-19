import os
from flask import Flask, jsonify
from flask_cors import CORS

from config import Config
from models.database import init_db
from routes.auth_routes import auth_bp
from routes.resume_routes import resume_bp
from routes.user_routes import user_bp

def create_app():
    """Application factory for Flask app."""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Enable CORS for frontend clients
    CORS(app, origins=['http://localhost:5173', 'http://localhost:3000'])
    
    # Initialize the database
    init_db()
    
    # Ensure upload directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Register API blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(resume_bp)
    app.register_blueprint(user_bp)
    
    # Global error handlers
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'message': 'Bad request', 'error': str(error)}), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'message': 'Resource not found'}), 404

    @app.errorhandler(413)
    def request_entity_too_large(error):
        return jsonify({'message': 'File too large, maximum size is 10MB'}), 413

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'message': 'Internal server error'}), 500

    @app.route('/health', methods=['GET'])
    def health_check():
        """Health check endpoint to verify API is running."""
        return jsonify({'status': 'healthy'}), 200

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
