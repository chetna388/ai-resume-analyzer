import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.database import create_user, get_user_by_email
from utils.auth_helpers import hash_password, verify_password, generate_token
from config import Config

def register(data: dict):
    """Handle user registration."""
    try:
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        if not username or not email or not password:
            return {'message': 'Username, email and password are required'}, 400
            
        if len(username) < 3:
            return {'message': 'Username must be at least 3 characters long'}, 400
            
        if '@' not in email:
            return {'message': 'Invalid email address'}, 400
            
        if len(password) < 6:
            return {'message': 'Password must be at least 6 characters long'}, 400
            
        existing_user = get_user_by_email(email)
        if existing_user:
            return {'message': 'User with this email already exists'}, 409
            
        hashed_pw = hash_password(password)
        user_id = create_user(username, email, hashed_pw)
        
        if not user_id:
            return {'message': 'Username might already be taken or another database error occurred'}, 400
            
        token = generate_token(user_id, Config.SECRET_KEY, Config.JWT_EXPIRATION_HOURS)
        
        return {
            'message': 'User registered successfully',
            'token': token,
            'user': {
                'id': user_id,
                'username': username,
                'email': email
            }
        }, 201
        
    except Exception as e:
        return {'message': f'Server error: {str(e)}'}, 500

def login(data: dict):
    """Handle user login."""
    try:
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return {'message': 'Email and password are required'}, 400
            
        user = get_user_by_email(email)
        if not user:
            return {'message': 'Invalid email or password'}, 401
            
        if not verify_password(password, user['password_hash']):
            return {'message': 'Invalid email or password'}, 401
            
        token = generate_token(user['id'], Config.SECRET_KEY, Config.JWT_EXPIRATION_HOURS)
        
        return {
            'message': 'Login successful',
            'token': token,
            'user': {
                'id': user['id'],
                'username': user['username'],
                'email': user['email']
            }
        }, 200
        
    except Exception as e:
        return {'message': f'Server error: {str(e)}'}, 500
