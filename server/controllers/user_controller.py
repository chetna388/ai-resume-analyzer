import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.database import get_user_by_id, get_user_stats, get_user_analyses

def get_profile(user_id: int):
    """Retrieves user profile and stats for the dashboard."""
    try:
        user = get_user_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
            
        stats = get_user_stats(user_id)
        
        # Omit sensitive information like password_hash
        user_safe = {
            'id': user['id'],
            'username': user['username'],
            'email': user['email'],
            'created_at': user['created_at']
        }
        
        return {
            'user': user_safe,
            'stats': stats
        }, 200
    except Exception as e:
        return {'message': f'Server error fetching profile: {str(e)}'}, 500

def get_history(user_id: int):
    """Retrieves all past resume analyses for a user."""
    try:
        analyses = get_user_analyses(user_id)
        return {
            'analyses': analyses,
            'total': len(analyses)
        }, 200
    except Exception as e:
        return {'message': f'Server error fetching history: {str(e)}'}, 500
