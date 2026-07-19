from flask import Blueprint, request, jsonify
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from controllers.resume_controller import upload_resume, predict_category_ctrl, analyze_resume, compare_jd
from utils.auth_helpers import token_required

resume_bp = Blueprint('resume', __name__)

@resume_bp.route('/api/upload-resume', methods=['POST'])
@token_required
def handle_upload_resume(user_id):
    if 'resume' not in request.files:
        return jsonify({'message': 'No file part in the request'}), 400
    file = request.files['resume']
    response, status = upload_resume(file, user_id)
    return jsonify(response), status

@resume_bp.route('/api/predict-category', methods=['POST'])
@token_required
def handle_predict_category(user_id):
    data = request.get_json() or {}
    resume_text = data.get('resume_text', '')
    if not resume_text:
        return jsonify({'message': 'resume_text is required'}), 400
    response, status = predict_category_ctrl(resume_text)
    return jsonify(response), status

@resume_bp.route('/api/analyze-resume', methods=['POST'])
@token_required
def handle_analyze_resume(user_id):
    resume_text = ""
    job_description = ""
    target_role = ""
    
    if request.is_json:
        data = request.get_json()
        resume_text = data.get('resume_text', '')
        job_description = data.get('job_description', '')
        target_role = data.get('target_role', '')
    else:
        if 'resume' in request.files:
            file = request.files['resume']
            res, status = upload_resume(file, user_id)
            if status != 200:
                return jsonify(res), status
            resume_text = res.get('extracted_text', '')
        else:
            resume_text = request.form.get('resume_text', '')
            
        job_description = request.form.get('job_description', '')
        target_role = request.form.get('target_role', '')

    if not resume_text:
        return jsonify({'message': 'resume_text or file is required'}), 400
        
    response, status = analyze_resume(resume_text, job_description, target_role, user_id)
    return jsonify(response), status

@resume_bp.route('/api/compare-job-description', methods=['POST'])
@token_required
def handle_compare_jd(user_id):
    data = request.get_json() or {}
    resume_text = data.get('resume_text', '')
    jd_text = data.get('jd_text', '')
    
    if not resume_text or not jd_text:
        return jsonify({'message': 'resume_text and jd_text are required'}), 400
        
    response, status = compare_jd(resume_text, jd_text)
    return jsonify(response), status
