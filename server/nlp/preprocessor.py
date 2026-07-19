import re
import string

try:
    import spacy
    # Load the English NLP model
    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        print("Downloading en_core_web_sm model...")
        import subprocess
        import sys
        subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
        nlp = spacy.load("en_core_web_sm")
except ImportError:
    print("spaCy is not installed. Please install it using: pip install spacy")
    print("Then download the model: python -m spacy download en_core_web_sm")
    nlp = None

def preprocess_text(text: str) -> str:
    """
    Preprocesses the input text for NLP tasks.
    
    Steps:
    1. Convert to lowercase
    2. Remove URLs
    3. Remove email addresses
    4. Remove phone numbers
    5. Remove special characters and extra whitespace
    6. Tokenize with spaCy
    7. Remove stopwords
    8. Lemmatize tokens
    9. Remove punctuation tokens
    10. Join and return cleaned text
    
    Args:
        text (str): The raw text to process.
        
    Returns:
        str: The cleaned, processed text.
    """
    if not isinstance(text, str):
        return ""
        
    # Convert to lowercase
    text = text.lower()
    
    # Remove URLs
    text = re.sub(r'http\S+|www.\S+', '', text, flags=re.MULTILINE)
    
    # Remove email addresses
    text = re.sub(r'\S+@\S+', '', text)
    
    # Remove phone numbers (simplified regex)
    text = re.sub(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', '', text)
    
    # Remove special characters but keep spaces and alphanumeric
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    if nlp is not None:
        # Process text with spaCy
        doc = nlp(text)
        
        cleaned_tokens = []
        for token in doc:
            # Check if token is a stop word or punctuation
            if not token.is_stop and not token.is_punct and token.text.strip():
                # Lemmatize
                cleaned_tokens.append(token.lemma_)
                
        return ' '.join(cleaned_tokens)
    else:
        # Fallback if spaCy is not available
        # Just simple tokenization and removal of punctuation
        return ' '.join([word for word in text.split() if word])
