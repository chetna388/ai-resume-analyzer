import os
import sys
import pandas as pd
import numpy as np
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score

# Add parent dir to path so nlp imports work
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from nlp.preprocessor import preprocess_text

# Define category mapping for Updated Resume Dataset (Gaurav Duttakiit)
CATEGORY_MAPPING = {
    'Java Developer': 'Java Developer',
    'Python Developer': 'Python Developer',
    'DevOps Engineer': 'DevOps Engineer',
    'Web Designing': 'Frontend Developer',
    'Data Science': 'Data Scientist',
    'Hadoop': 'Data Scientist',
    'Database': 'Backend Developer',
    'DotNet Developer': 'Backend Developer',
    'ETL Developer': 'Backend Developer',
    'Blockchain': 'Full Stack Developer',
    'Testing': 'Backend Developer',
    'Automation Testing': 'DevOps Engineer',
    'Network Security Engineer': 'Cloud Engineer',
    'SAP Developer': 'Backend Developer',
    'HR': 'HR',
    'Advocate': 'Other',
    'Arts': 'Other',
    'Mechanical Engineer': 'Other',
    'Electrical Engineering': 'Other',
    'Civil Engineer': 'Other',
    'Sales': 'Other',
    'Health and Fitness': 'Other',
    'PMO': 'Other',
    'Business Analyst': 'Other',
    'Operations Manager': 'Other'
}

# Define fallback category mapping for LiveCareer Dataset
LIVECAREER_MAPPING = {
    'INFORMATION-TECHNOLOGY': 'Full Stack Developer',
    'ENGINEERING': 'Backend Developer',
    'DESIGNER': 'Frontend Developer',
    'BUSINESS-DEVELOPMENT': 'Full Stack Developer',
    'CONSULTANT': 'Full Stack Developer',
    'PUBLIC-RELATIONS': 'Other',
    'HR': 'HR',
    'ADVOCATE': 'Other',
    'ARTS': 'Other',
    'CONSTRUCTION': 'Other',
    'FINANCE': 'Other',
    'ACCOUNTANT': 'Other',
    'CHEF': 'Other',
    'TEACHER': 'Other',
    'HEALTHCARE': 'Other',
    'FITNESS': 'Other',
    'AGRICULTURE': 'Other',
    'APPAREL': 'Other',
    'AUTOMOBILE': 'Other',
    'AVIATION': 'Other',
    'BANKING': 'Other',
    'BPO': 'Other',
    'DIGITAL-MEDIA': 'Other',
    'SALES': 'Other'
}

def train_model():
    """
    Trains the resume classification model.
    """
    print("Starting model training pipeline...")
    
    # Define paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Possible candidate paths for the CSV file
    candidate_paths = [
        os.path.join(base_dir, 'dataset', 'UpdatedResumeDataSet.csv'),
        os.path.join(base_dir, 'dataset', 'UpdatedResumeDataSet.csv', 'Resume.csv'),
        os.path.join(base_dir, 'dataset', 'Resume.csv'),
        os.path.join(base_dir, 'dataset', 'UpdatedResumeDataSet.csv', 'UpdatedResumeDataSet.csv')
    ]
    
    dataset_path = None
    for path in candidate_paths:
        if os.path.exists(path) and os.path.isfile(path):
            dataset_path = path
            break
            
    if not dataset_path:
        print("Error: Dataset CSV file not found.")
        print("Please place the Kaggle CSV file in the server/dataset/ folder.")
        print(f"Looked in candidates:\n" + "\n".join([f" - {p}" for p in candidate_paths]))
        return
        
    model_dir = os.path.join(base_dir, 'trained_model')
    os.makedirs(model_dir, exist_ok=True)
    
    # 1. Load CSV
    print(f"Loading dataset from {dataset_path}...")
    try:
        df = pd.read_csv(dataset_path)
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return

    # Check columns and normalize
    columns = [col.lower() for col in df.columns]
    resume_col = None
    category_col = None
    
    if 'resume' in columns:
        resume_col = df.columns[columns.index('resume')]
    elif 'resume_str' in columns:
        resume_col = df.columns[columns.index('resume_str')]
        
    if 'category' in columns:
        category_col = df.columns[columns.index('category')]
        
    if not resume_col or not category_col:
        print(f"Error: Could not identify Resume or Category column. Found columns: {df.columns.tolist()}")
        return
        
    print(f"Using column '{resume_col}' for resume text and '{category_col}' for category labels.")
    
    # 2. Map categories dynamically
    print("Mapping categories...")
    sample_categories = df[category_col].dropna().unique()
    is_livecareer = any(cat in ['INFORMATION-TECHNOLOGY', 'BUSINESS-DEVELOPMENT', 'CHEF'] for cat in sample_categories)
    
    if is_livecareer:
        print("Detected LiveCareer dataset format.")
        mapping = LIVECAREER_MAPPING
    else:
        print("Detected Updated Resume Dataset (Gaurav Duttakiit) format.")
        mapping = CATEGORY_MAPPING
        
    df['MappedCategory'] = df[category_col].map(mapping)
    
    # 3. Filter out 'Other' and 'HR'
    print("Filtering categories...")
    df = df[~df['MappedCategory'].isin(['Other', 'HR', None]) & df['MappedCategory'].notna()]
    
    if df.empty:
        print("Error: DataFrame is empty after filtering mapping classes.")
        return
        
    print(f"Dataset size after filtering: {len(df)}")
    
    # 4. Preprocess all resume texts
    print("Preprocessing resume texts (this may take a while)...")
    total = len(df)
    processed_texts = []
    
    for i, text in enumerate(df[resume_col]):
        processed = preprocess_text(str(text))
        processed_texts.append(processed)
        if (i + 1) % 100 == 0:
            print(f"Processed {i + 1}/{total} resumes")
            
    df['CleanedResume'] = processed_texts
    
    # 5. TF-IDF
    print("Vectorizing text...")
    vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 2), sublinear_tf=True)
    X = vectorizer.fit_transform(df['CleanedResume'])
    
    # 6. LabelEncoder
    print("Encoding labels...")
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(df['MappedCategory'])
    
    # 7. Train Test Split
    print("Splitting dataset...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
    
    # 8. LogisticRegression
    print("Training Logistic Regression model...")
    model = LogisticRegression(max_iter=1000, C=1.0, multi_class='multinomial', solver='lbfgs', random_state=42)
    
    # 9. Fit model
    model.fit(X_train, y_train)
    
    # 10. Evaluate
    print("\nEvaluating model on test set...")
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy:.4f}")
    
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=label_encoder.classes_))
    
    # 11. Save model, vectorizer, label_encoder
    print("Saving model and artifacts...")
    joblib.dump(model, os.path.join(model_dir, 'model.joblib'))
    joblib.dump(vectorizer, os.path.join(model_dir, 'vectorizer.joblib'))
    joblib.dump(label_encoder, os.path.join(model_dir, 'label_encoder.joblib'))
    
    # 12. Complete
    print(f"\nModel training complete! Artifacts saved to {model_dir}")

if __name__ == '__main__':
    train_model()
