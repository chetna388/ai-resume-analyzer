import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'ai-resume-analyzer-secret-key-2024')
    JWT_EXPIRATION_HOURS = int(os.environ.get('JWT_EXPIRATION_HOURS', '24'))
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB
    DATABASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.db')
    TRAINED_MODEL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'trained_model')
    ALLOWED_EXTENSIONS = {'pdf'}
