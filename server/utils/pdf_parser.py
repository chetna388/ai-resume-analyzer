import re
try:
    import fitz  # PyMuPDF
except ImportError:
    print("PyMuPDF (fitz) is not installed. Please run: pip install PyMuPDF")
    fitz = None

def extract_text_from_pdf(file_path: str) -> str:
    """
    Extracts text from a PDF file using PyMuPDF.
    
    Args:
        file_path (str): The path to the PDF file.
        
    Returns:
        str: The extracted text.
    """
    if fitz is None:
        raise ImportError("PyMuPDF (fitz) is not installed.")
        
    try:
        doc = fitz.open(file_path)
        text_content = []
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            text_content.append(page.get_text())
            
        doc.close()
        
        # Clean up the extracted text
        full_text = "\n".join(text_content)
        # Normalize newlines and spaces
        full_text = re.sub(r'\r\n|\r', '\n', full_text)
        full_text = re.sub(r'\n{3,}', '\n\n', full_text)
        
        return full_text
    except Exception as e:
        print(f"Error extracting text from PDF {file_path}: {e}")
        return ""

def extract_sections(text: str) -> dict:
    """
    Uses regex patterns to identify and extract resume sections.
    
    Args:
        text (str): The raw resume text.
        
    Returns:
        dict: A dictionary with section names as keys and section content as values.
    """
    if not text:
        return {}
        
    sections = {
        'Summary': '',
        'Experience': '',
        'Education': '',
        'Skills': '',
        'Projects': '',
        'Certifications': '',
        'Contact': ''
    }
    
    # Patterns to match section headers (case insensitive)
    # Using lookaheads to match content until the next section header or EOF
    header_patterns = {
        'Summary': r'(?i)(?:summary|objective|profile|about me)\s*[:\n]',
        'Experience': r'(?i)(?:experience|work history|employment|professional|work experience)\s*[:\n]',
        'Education': r'(?i)(?:education|academic|university|degree|bachelor|master|phd)\s*[:\n]',
        'Skills': r'(?i)(?:skills|technical skills|technologies|competencies)\s*[:\n]',
        'Projects': r'(?i)(?:projects|portfolio|work samples)\s*[:\n]',
        'Certifications': r'(?i)(?:certifications|certificates|credentials)\s*[:\n]'
    }
    
    # Try to extract contact information directly using regex
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    phone_pattern = r'\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b'
    linkedin_pattern = r'(?i)(?:linkedin\.com\/in\/[\w\-]+)'
    
    emails = re.findall(email_pattern, text)
    phones = re.findall(phone_pattern, text)
    linkedins = re.findall(linkedin_pattern, text)
    
    contact_info = []
    if emails: contact_info.extend(emails)
    if phones: contact_info.extend(phones)
    if linkedins: contact_info.extend(linkedins)
    
    sections['Contact'] = '\n'.join(contact_info)
    
    current_section = None
    lines = text.split('\n')
    
    for line in lines:
        cleaned_line = line.strip()
        if not cleaned_line:
            if current_section:
                sections[current_section] += '\n'
            continue
            
        is_header = False
        for sec_name, pattern in header_patterns.items():
            if len(cleaned_line) < 30 and re.match(pattern, cleaned_line + '\n'):
                current_section = sec_name
                is_header = True
                break
                
        if not is_header and current_section:
            sections[current_section] += cleaned_line + '\n'
            
    for key in sections:
        sections[key] = sections[key].strip()
        
    return sections
