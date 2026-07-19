import os
import sys
from sklearn.metrics import classification_report, accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

# Add parent dir to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ml.predictor import load_model

def evaluate_model(model, X_test, y_test, label_encoder) -> dict:
    """
    Evaluates a trained model on a test set.
    
    Args:
        model: Trained scikit-learn model.
        X_test: Test features.
        y_test: True test labels.
        label_encoder: LabelEncoder used for target classes.
        
    Returns:
        dict: Evaluation metrics and reports.
    """
    # Predictions
    y_pred = model.predict(X_test)
    
    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='macro', zero_division=0)
    recall = recall_score(y_test, y_pred, average='macro', zero_division=0)
    f1 = f1_score(y_test, y_pred, average='macro', zero_division=0)
    
    # Reports
    report = classification_report(y_test, y_pred, target_names=label_encoder.classes_, output_dict=True, zero_division=0)
    conf_matrix = confusion_matrix(y_test, y_pred).tolist()
    
    return {
        'accuracy': float(accuracy),
        'macro_precision': float(precision),
        'macro_recall': float(recall),
        'macro_f1': float(f1),
        'classification_report': report,
        'confusion_matrix': conf_matrix,
        'classes': label_encoder.classes_.tolist()
    }

def get_model_info() -> dict:
    """
    Retrieves basic information about the currently loaded model.
    
    Returns:
        dict: Information about the model.
    """
    try:
        model, vectorizer, label_encoder = load_model()
        
        info = {
            'model_type': type(model).__name__,
            'number_of_classes': len(label_encoder.classes_),
            'classes': label_encoder.classes_.tolist(),
            'feature_count': len(vectorizer.get_feature_names_out()),
            'status': 'loaded'
        }
        return info
    except FileNotFoundError as e:
        return {
            'status': 'error',
            'error': str(e)
        }
    except Exception as e:
        return {
            'status': 'error',
            'error': f"Unexpected error: {str(e)}"
        }
