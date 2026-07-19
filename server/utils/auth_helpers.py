from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
import functools
import flask
from flask import request, jsonify
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config

def hash_password(password: str) -> str:
    """Hashes a password for storing in the database."""
    return generate_password_hash(password)

def verify_password(password: str, password_hash: str) -> bool:
    """Verifies a plaintext password against the hashed version."""
    return check_password_hash(password_hash, password)

def generate_token(user_id: int, secret_key: str, expiration_hours: int = 24) -> str:
    """Generates a JWT for authenticated sessions."""
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=expiration_hours),
        'iat': datetime.datetime.utcnow()
    }
    return jwt.encode(payload, secret_key, algorithm='HS256')

def decode_token(token: str, secret_key: str):
    """Decodes a JWT and returns the payload if valid."""
    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def token_required(f):
    """Decorator to require valid JWT in Authorization header."""
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(" ")[1]
        
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
            
        payload = decode_token(token, Config.SECRET_KEY)
        if not payload:
            return jsonify({'message': 'Token is invalid or expired!'}), 401
            
        return f(user_id=payload['user_id'], *args, **kwargs)
    return decorated
