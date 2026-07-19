from flask import Blueprint, jsonify
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from controllers.user_controller import get_profile, get_history
from utils.auth_helpers import token_required

user_bp = Blueprint('user', __name__)

@user_bp.route('/api/history', methods=['GET'])
@token_required
def handle_get_history(user_id):
    response, status = get_history(user_id)
    return jsonify(response), status

@user_bp.route('/api/profile', methods=['GET'])
@token_required
def handle_get_profile(user_id):
    response, status = get_profile(user_id)
    return jsonify(response), status
