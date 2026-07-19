from flask import Blueprint, request, jsonify
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from controllers.auth_controller import register, login

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/register', methods=['POST'])
def handle_register():
    data = request.get_json() or {}
    response, status = register(data)
    return jsonify(response), status

@auth_bp.route('/api/login', methods=['POST'])
def handle_login():
    data = request.get_json() or {}
    response, status = login(data)
    return jsonify(response), status
