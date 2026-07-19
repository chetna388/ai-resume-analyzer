import sqlite3
import json
import os
from datetime import datetime
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config

def get_db():
    """Returns a new sqlite database connection."""
    conn = sqlite3.connect(Config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the SQLite database and create tables if they do not exist."""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create analyses table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER REFERENCES users(id),
                filename TEXT,
                resume_text TEXT,
                category TEXT,
                confidence REAL,
                ats_score REAL,
                job_description TEXT,
                matching_percentage REAL,
                skills_found TEXT,
                missing_skills TEXT,
                recommendations TEXT,
                interview_questions TEXT,
                score_breakdown TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
    except Exception as e:
        print(f"Database initialization error: {e}")
    finally:
        if conn:
            conn.close()

def create_user(username, email, password_hash):
    """Creates a new user and returns their ID."""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (username, email, password_hash)
            VALUES (?, ?, ?)
        ''', (username, email, password_hash))
        conn.commit()
        user_id = cursor.lastrowid
        return user_id
    except sqlite3.IntegrityError:
        return None # User email or username already exists
    except Exception as e:
        print(f"Error creating user: {e}")
        return None
    finally:
        if conn:
            conn.close()

def get_user_by_email(email):
    """Retrieve a user by their email address."""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
        return dict(user) if user else None
    except Exception as e:
        print(f"Error getting user by email: {e}")
        return None
    finally:
        if conn:
            conn.close()

def get_user_by_id(user_id):
    """Retrieve a user by their ID."""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        return dict(user) if user else None
    except Exception as e:
        print(f"Error getting user by id: {e}")
        return None
    finally:
        if conn:
            conn.close()

def save_analysis(user_id, data_dict):
    """Save resume analysis results to the database."""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        def safe_json(val):
            return json.dumps(val) if val is not None else None
            
        cursor.execute('''
            INSERT INTO analyses (
                user_id, filename, resume_text, category, confidence,
                ats_score, job_description, matching_percentage,
                skills_found, missing_skills, recommendations,
                interview_questions, score_breakdown
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            user_id,
            data_dict.get('filename'),
            data_dict.get('resume_text'),
            data_dict.get('category'),
            data_dict.get('confidence'),
            data_dict.get('ats_score'),
            data_dict.get('job_description'),
            data_dict.get('matching_percentage'),
            safe_json(data_dict.get('skills_found')),
            safe_json(data_dict.get('missing_skills')),
            safe_json(data_dict.get('recommendations')),
            safe_json(data_dict.get('interview_questions')),
            safe_json(data_dict.get('score_breakdown'))
        ))
        conn.commit()
        analysis_id = cursor.lastrowid
        return analysis_id
    except Exception as e:
        print(f"Error saving analysis: {e}")
        return None
    finally:
        if conn:
            conn.close()

def get_user_analyses(user_id):
    """Get all historical analyses for a specific user."""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM analyses WHERE user_id = ? ORDER BY created_at DESC', (user_id,))
        rows = cursor.fetchall()
        analyses = []
        for row in rows:
            analysis = dict(row)
            # Parse JSON strings back to dicts/lists
            for field in ['skills_found', 'missing_skills', 'recommendations', 'interview_questions', 'score_breakdown']:
                if analysis.get(field):
                    try:
                        analysis[field] = json.loads(analysis[field])
                    except json.JSONDecodeError:
                        analysis[field] = None
            analyses.append(analysis)
        return analyses
    except Exception as e:
        print(f"Error getting user analyses: {e}")
        return []
    finally:
        if conn:
            conn.close()

def get_analysis_by_id(analysis_id, user_id):
    """Get a single historical analysis by its ID and user ID."""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM analyses WHERE id = ? AND user_id = ?', (analysis_id, user_id))
        row = cursor.fetchone()
        if not row:
            return None
        analysis = dict(row)
        for field in ['skills_found', 'missing_skills', 'recommendations', 'interview_questions', 'score_breakdown']:
            if analysis.get(field):
                try:
                    analysis[field] = json.loads(analysis[field])
                except json.JSONDecodeError:
                    analysis[field] = None
        return analysis
    except Exception as e:
        print(f"Error getting analysis: {e}")
        return None
    finally:
        if conn:
            conn.close()

def get_user_stats(user_id):
    """Get aggregated statistics for a user's dashboard."""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # Get total analyses count
        cursor.execute('SELECT COUNT(*) FROM analyses WHERE user_id = ?', (user_id,))
        total_analyses = cursor.fetchone()[0]
        
        if total_analyses == 0:
            return {'total_analyses': 0, 'avg_ats_score': 0.0, 'top_category': None}
            
        # Get average ATS score
        cursor.execute('SELECT AVG(ats_score) FROM analyses WHERE user_id = ?', (user_id,))
        avg_ats_score = cursor.fetchone()[0] or 0.0
        
        # Get most common category
        cursor.execute('''
            SELECT category, COUNT(*) as count 
            FROM analyses 
            WHERE user_id = ? AND category IS NOT NULL AND category != 'Unknown'
            GROUP BY category 
            ORDER BY count DESC 
            LIMIT 1
        ''', (user_id,))
        top_cat_row = cursor.fetchone()
        top_category = top_cat_row['category'] if top_cat_row else None
        
        return {
            'total_analyses': total_analyses,
            'avg_ats_score': round(avg_ats_score, 2),
            'top_category': top_category
        }
    except Exception as e:
        print(f"Error getting user stats: {e}")
        return {'total_analyses': 0, 'avg_ats_score': 0.0, 'top_category': None}
    finally:
        if conn:
            conn.close()
