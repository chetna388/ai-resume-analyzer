import os
import sys
import joblib
import numpy as np

# Add parent dir to path so nlp imports work
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from nlp.preprocessor import preprocess_text

# Module-level cache variables
_model = None
_vectorizer = None
_label_encoder = None

def load_model() -> tuple:
    """
    Loads the trained model, vectorizer, and label encoder from disk.
    Caches them in module-level variables for subsequent calls.
    
    Returns:
        tuple: (model, vectorizer, label_encoder)
        
    Raises:
        FileNotFoundError: If the model files are not found.
    """
    global _model, _vectorizer, _label_encoder
    
    # Return cached if already loaded
    if _model is not None and _vectorizer is not None and _label_encoder is not None:
        return _model, _vectorizer, _label_encoder
        
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    model_dir = os.path.join(base_dir, 'trained_model')
    
    model_path = os.path.join(model_dir, 'model.joblib')
    vectorizer_path = os.path.join(model_dir, 'vectorizer.joblib')
    le_path = os.path.join(model_dir, 'label_encoder.joblib')
    
    if not (os.path.exists(model_path) and os.path.exists(vectorizer_path) and os.path.exists(le_path)):
        raise FileNotFoundError(
            f"Model files not found in {model_dir}. "
            "Please run server/ml/train_model.py first to generate the models."
        )
        
    try:
        _model = joblib.load(model_path)
        _vectorizer = joblib.load(vectorizer_path)
        _label_encoder = joblib.load(le_path)
    except Exception as e:
        raise RuntimeError(f"Error loading model files: {e}")
        
    return _model, _vectorizer, _label_encoder

def predict_category(text: str) -> dict:
    """
    Predicts the job category for a given resume text.
    
    Args:
        text (str): The raw resume text.
        
    Returns:
        dict: The prediction results including category, confidence, and top predictions.
    """
    if not text:
        return {
            'category': 'Unknown',
            'confidence': 0.0,
            'top_predictions': []
        }
        
    try:
        # Load model if not cached
        model, vectorizer, label_encoder = load_model()
        
        # Preprocess text
        cleaned_text = preprocess_text(text)
        
        if not cleaned_text.strip():
            return {
                'category': 'Unknown',
                'confidence': 0.0,
                'top_predictions': []
            }
            
        # Transform with vectorizer
        X = vectorizer.transform([cleaned_text])
        
        # Get prediction and probability scores
        probabilities = model.predict_proba(X)[0]
        
        # Get the highest probability prediction
        pred_idx = np.argmax(probabilities)
        pred_category = label_encoder.inverse_transform([pred_idx])[0]
        max_prob = float(probabilities[pred_idx])
        
        # Get top 3 predictions
        top_indices = np.argsort(probabilities)[::-1][:3]
        top_predictions = []
        for idx in top_indices:
            cat = label_encoder.inverse_transform([idx])[0]
            prob = float(probabilities[idx])
            top_predictions.append({
                'category': cat,
                'confidence': round(prob, 4)
            })
            
        return {
            'category': pred_category,
            'confidence': round(max_prob, 4),
            'top_predictions': top_predictions
        }
    except Exception as e:
        print(f"Error during prediction: {e}")
        return {
            'category': 'Error',
            'confidence': 0.0,
            'top_predictions': [],
            'error': str(e)
        }
