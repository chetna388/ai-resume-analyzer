"""
Resume Controller
=================
Core business logic for resume analysis pipeline.
Orchestrates ML prediction, NLP skill extraction, ATS scoring,
recommendations, and interview question generation.
"""

import os
import sys
import json
import traceback
from werkzeug.utils import secure_filename

# Ensure parent directory is on path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.database import save_analysis
from config import Config

# --- Dynamic imports with fallbacks ---
# These modules are developed in parallel; fallbacks allow the API to start
# even if individual ML/NLP modules are not yet available.

try:
    from utils.pdf_parser import extract_text_from_pdf
except ImportError:
    def extract_text_from_pdf(filepath):
        return "PDF extraction module not available."

try:
    from ml.predictor import predict_category
except ImportError:
    def predict_category(text):
        return {"category": "Unknown", "confidence": 0.0, "top_predictions": []}

try:
    from nlp.preprocessor import preprocess_text
except ImportError:
    def preprocess_text(text):
        return text

try:
    from nlp.skill_extractor import extract_skills, get_required_skills_for_role, compare_skills
except ImportError:
    def extract_skills(text):
        return {'found_skills': [], 'categories': {}, 'count': 0}
    def get_required_skills_for_role(role):
        return []
    def compare_skills(resume_skills, jd_text):
        return {'matching': [], 'missing': [], 'match_percentage': 0.0}

try:
    from utils.ats_scorer import calculate_ats_score
except ImportError:
    def calculate_ats_score(resume_text, jd_text, resume_skills, jd_skills):
        return {'total_score': 0, 'breakdown': {}, 'grade': 'N/A', 'strength': 'N/A'}

try:
    from utils.recommendations import generate_recommendations
except ImportError:
    def generate_recommendations(category, resume_skills, missing_skills, ats_score, resume_text):
        return {'missing_skills': [], 'courses': [], 'improvements': [], 'project_suggestions': [],
                'missing_keywords': [], 'weak_sections': [], 'certifications': []}

try:
    from utils.interview_questions import generate_interview_questions
except ImportError:
    def generate_interview_questions(skills, count=5):
        return []


def upload_resume(file, user_id: int):
    """
    Saves an uploaded PDF resume and extracts its text content.

    Args:
        file: The uploaded file object from Flask request.
        user_id (int): The authenticated user's ID.

    Returns:
        tuple: (response_dict, status_code)
    """
    try:
        if not file or not file.filename:
            return {'message': 'No file provided'}, 400

        filename = secure_filename(file.filename)
        if not filename.lower().endswith('.pdf'):
            return {'message': 'Only PDF files are allowed'}, 400

        # Save file with user_id prefix to avoid collisions
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        filepath = os.path.join(Config.UPLOAD_FOLDER, f"{user_id}_{filename}")
        file.save(filepath)

        # Extract text from PDF
        try:
            extracted_text = extract_text_from_pdf(filepath)
        except Exception as e:
            return {'message': f'Failed to extract text from PDF: {str(e)}'}, 500

        return {
            'message': 'File uploaded successfully',
            'filename': filename,
            'extracted_text': extracted_text,
            'text_length': len(extracted_text)
        }, 200

    except Exception as e:
        return {'message': f'Server error during upload: {str(e)}'}, 500


def predict_category_ctrl(resume_text: str):
    """
    Predicts the job category of a resume.

    Args:
        resume_text (str): Raw resume text.

    Returns:
        tuple: (response_dict, status_code)
    """
    try:
        processed_text = preprocess_text(resume_text)
        prediction = predict_category(processed_text)
        return {
            'category': prediction.get('category', 'Unknown'),
            'confidence': prediction.get('confidence', 0.0),
            'top_predictions': prediction.get('top_predictions', [])
        }, 200
    except Exception as e:
        return {
            'message': f'Prediction error: {str(e)}',
            'category': 'Unknown',
            'confidence': 0.0
        }, 500


def analyze_resume(resume_text: str, job_description: str, target_role: str, user_id: int):
    """
    Full resume analysis pipeline — the core endpoint.

    Steps:
      1. Preprocess resume text
      2. Predict resume category using ML model
      3. Extract skills from resume
      4. Determine required/JD skills
      5. Compare skills (matching vs missing)
      6. Calculate weighted ATS score
      7. Generate improvement recommendations
      8. Generate interview questions
      9. Save analysis to database
      10. Return comprehensive results

    Args:
        resume_text (str): Raw resume text.
        job_description (str): Raw job description text.
        target_role (str): Target job role selected by user.
        user_id (int): Authenticated user's ID.

    Returns:
        tuple: (response_dict, status_code)
    """
    try:
        # Step 1: Preprocess resume text
        processed_text = preprocess_text(resume_text)

        # Step 2: Predict category (graceful fallback if model not trained)
        try:
            prediction = predict_category(processed_text)
            category = prediction.get('category', 'Unknown')
            confidence = prediction.get('confidence', 0.0)
            top_predictions = prediction.get('top_predictions', [])
        except Exception:
            category = 'Unknown'
            confidence = 0.0
            top_predictions = []

        # Step 3: Extract skills from resume
        # extract_skills returns {'found_skills': [...], 'categories': {...}, 'count': int}
        resume_skill_data = extract_skills(resume_text)
        resume_skills_list = resume_skill_data.get('found_skills', [])
        skills_by_category = resume_skill_data.get('categories', {})

        # Step 4: Determine JD/required skills for comparison
        jd_skills_list = []
        if job_description:
            jd_skill_data = extract_skills(job_description)
            jd_skills_list = jd_skill_data.get('found_skills', [])
        elif target_role:
            jd_skills_list = get_required_skills_for_role(target_role)

        # Step 5: Compare resume skills against JD skills
        # compare_skills(resume_skills: list, jd_text: str) -> dict
        # We need to pass the JD text or construct it from the JD skills list
        if job_description:
            skills_comparison = compare_skills(resume_skills_list, job_description)
        elif jd_skills_list:
            # If we only have a role (no JD text), create a pseudo-JD from skills
            pseudo_jd = ' '.join(jd_skills_list)
            skills_comparison = compare_skills(resume_skills_list, pseudo_jd)
        else:
            skills_comparison = {'matching': [], 'missing': [], 'match_percentage': 0.0}

        matching_skills = skills_comparison.get('matching', [])
        missing_skills = skills_comparison.get('missing', [])
        matching_percentage = skills_comparison.get('match_percentage', 0.0)

        # Step 6: Calculate ATS score
        # calculate_ats_score(resume_text, jd_text, resume_skills, jd_skills)
        jd_for_scoring = job_description if job_description else ' '.join(jd_skills_list)
        ats_result = calculate_ats_score(resume_text, jd_for_scoring, resume_skills_list, jd_skills_list)
        ats_score = ats_result.get('total_score', 0)
        score_breakdown = ats_result.get('breakdown', {})
        grade = ats_result.get('grade', 'N/A')
        strength = ats_result.get('strength', 'N/A')

        # Step 7: Generate recommendations
        # generate_recommendations(category, resume_skills, missing_skills, ats_score, resume_text)
        recommendations = generate_recommendations(
            category, resume_skills_list, missing_skills, ats_score, resume_text
        )

        # Step 8: Generate interview questions
        # generate_interview_questions(skills: list, count: int)
        # Use matching skills (skills the candidate knows) for interview prep
        interview_skills = matching_skills if matching_skills else resume_skills_list[:10]
        interview_questions = generate_interview_questions(interview_skills, 5)

        # Step 9: Save analysis to database
        word_count = len(resume_text.split())
        db_data = {
            'filename': None,
            'resume_text': resume_text,
            'category': category,
            'confidence': confidence,
            'ats_score': ats_score,
            'job_description': job_description,
            'matching_percentage': matching_percentage,
            'skills_found': resume_skills_list,
            'missing_skills': missing_skills,
            'recommendations': recommendations,
            'interview_questions': interview_questions,
            'score_breakdown': score_breakdown
        }
        analysis_id = save_analysis(user_id, db_data)

        # Step 10: Return comprehensive results
        return {
            'analysis_id': analysis_id,
            'category': category,
            'confidence': round(confidence, 4),
            'top_predictions': top_predictions,
            'ats_score': ats_score,
            'score_breakdown': score_breakdown,
            'grade': grade,
            'strength': strength,
            'matching_percentage': round(matching_percentage, 2),
            'skills_found': resume_skills_list,
            'skills_by_category': skills_by_category,
            'missing_skills': missing_skills,
            'recommendations': recommendations,
            'interview_questions': interview_questions,
            'resume_stats': {
                'word_count': word_count,
                'char_count': len(resume_text),
                'skill_count': len(resume_skills_list)
            }
        }, 200

    except Exception as e:
        print(f"[ERROR] analyze_resume failed: {traceback.format_exc()}")
        return {'message': f'Analysis error: {str(e)}'}, 500


def compare_jd(resume_text: str, jd_text: str):
    """
    Compares resume text against a job description for skill matching.

    Args:
        resume_text (str): Raw resume text.
        jd_text (str): Raw job description text.

    Returns:
        tuple: (response_dict, status_code)
    """
    try:
        # Extract skills from resume
        resume_skill_data = extract_skills(resume_text)
        resume_skills_list = resume_skill_data.get('found_skills', [])

        # Compare against JD
        comparison = compare_skills(resume_skills_list, jd_text)

        return {
            'similarity_score': comparison.get('match_percentage', 0.0),
            'matching_skills': comparison.get('matching', []),
            'missing_skills': comparison.get('missing', []),
            'match_percentage': comparison.get('match_percentage', 0.0)
        }, 200

    except Exception as e:
        return {'message': f'Error comparing JD: {str(e)}'}, 500
