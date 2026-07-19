from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def compute_similarity(text1: str, text2: str) -> float:
    """
    Computes cosine similarity between two texts using TF-IDF.
    
    Args:
        text1 (str): First text.
        text2 (str): Second text.
        
    Returns:
        float: Similarity score between 0.0 and 1.0.
    """
    if not text1 or not text2:
        return 0.0
        
    try:
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform([text1, text2])
        
        # Calculate cosine similarity between the two vectors
        cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
        
        return float(cosine_sim[0][0])
    except Exception as e:
        print(f"Error computing similarity: {e}")
        return 0.0

def compute_section_similarity(resume_sections: dict, jd_text: str) -> dict:
    """
    Computes similarity for each resume section against the JD.
    
    Args:
        resume_sections (dict): Dictionary of extracted resume sections.
        jd_text (str): Job description text.
        
    Returns:
        dict: Mapping of section names to similarity scores.
    """
    similarities = {}
    
    if not jd_text or not resume_sections:
        return similarities
        
    for section_name, section_text in resume_sections.items():
        if section_text:
            score = compute_similarity(section_text, jd_text)
            similarities[section_name] = round(score, 4)
        else:
            similarities[section_name] = 0.0
            
    return similarities
