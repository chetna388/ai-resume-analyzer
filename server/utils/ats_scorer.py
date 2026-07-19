import os
import sys
import re

# Add parent dir to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from nlp.similarity import compute_similarity
from utils.pdf_parser import extract_sections

def calculate_ats_score(resume_text: str, jd_text: str, resume_skills: list, jd_skills: list) -> dict:
    """
    Calculates a weighted ATS score based on resume and job description.
    
    Weights:
    - Resume-JD Similarity (50%)
    - Skill Match (25%)
    - Resume Structure (10%)
    - Project Relevance (10%)
    - Keyword Presence (5%)
    
    Args:
        resume_text (str): Full text of the resume.
        jd_text (str): Full text of the job description.
        resume_skills (list): Skills extracted from resume.
        jd_skills (list): Skills extracted from JD.
        
    Returns:
        dict: Detailed breakdown of the ATS score and final grade.
    """
    if not resume_text or not jd_text:
        return {
            'total_score': 0.0,
            'breakdown': {},
            'grade': 'F',
            'strength': 'Poor'
        }

    # 1. Similarity Score (50%)
    similarity = compute_similarity(resume_text, jd_text)
    # Scale from 0-1 to 0-100
    sim_score = similarity * 100.0
    sim_weighted = sim_score * 0.50

    # 2. Skill Match (25%)
    if jd_skills:
        resume_skills_lower = [s.lower() for s in resume_skills]
        matched_skills = [s for s in jd_skills if s.lower() in resume_skills_lower]
        skill_score = (len(matched_skills) / len(jd_skills)) * 100.0
    else:
        skill_score = 100.0 if resume_skills else 0.0
    skill_weighted = skill_score * 0.25

    # 3. Resume Structure (10%)
    sections = extract_sections(resume_text)
    # Expected core sections
    expected_sections = ['Summary', 'Experience', 'Education', 'Skills']
    present_sections = [s for s in expected_sections if sections.get(s)]
    
    structure_score = (len(present_sections) / len(expected_sections)) * 100.0
    structure_weighted = structure_score * 0.10

    # 4. Project Relevance (10%)
    projects_text = sections.get('Projects', '')
    if projects_text and jd_skills:
        # Check if project text mentions any JD skills
        project_skills_matched = sum(1 for s in jd_skills if s.lower() in projects_text.lower())
        proj_score = min(100.0, (project_skills_matched / max(1, len(jd_skills) * 0.3)) * 100.0)
    else:
        proj_score = 0.0
    proj_weighted = proj_score * 0.10

    # 5. Keyword Presence (5%)
    # Some common action verbs and power words expected in JD/Resumes
    power_words = ['developed', 'managed', 'led', 'created', 'designed', 'optimized', 'implemented', 'achieved']
    kw_found = sum(1 for w in power_words if w in resume_text.lower())
    kw_score = min(100.0, (kw_found / len(power_words)) * 100.0)
    kw_weighted = kw_score * 0.05

    # Total Score
    total_score = sim_weighted + skill_weighted + structure_weighted + proj_weighted + kw_weighted
    total_score = round(total_score, 2)

    # Assign Grade
    if total_score >= 90:
        grade = 'A+'
        strength = 'Excellent'
    elif total_score >= 80:
        grade = 'A'
        strength = 'Good'
    elif total_score >= 70:
        grade = 'B+'
        strength = 'Good'
    elif total_score >= 60:
        grade = 'B'
        strength = 'Average'
    elif total_score >= 50:
        grade = 'C'
        strength = 'Below Average'
    elif total_score >= 40:
        grade = 'D'
        strength = 'Poor'
    else:
        grade = 'F'
        strength = 'Poor'

    return {
        'total_score': total_score,
        'breakdown': {
            'similarity': {'score': round(sim_score, 2), 'weight': 50, 'weighted_score': round(sim_weighted, 2)},
            'skill_match': {'score': round(skill_score, 2), 'weight': 25, 'weighted_score': round(skill_weighted, 2)},
            'resume_structure': {'score': round(structure_score, 2), 'weight': 10, 'weighted_score': round(structure_weighted, 2)},
            'project_relevance': {'score': round(proj_score, 2), 'weight': 10, 'weighted_score': round(proj_weighted, 2)},
            'keyword_presence': {'score': round(kw_score, 2), 'weight': 5, 'weighted_score': round(kw_weighted, 2)}
        },
        'grade': grade,
        'strength': strength
    }
