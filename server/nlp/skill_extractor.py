import re

# Comprehensive skill taxonomy
SKILL_TAXONOMY = {
    'PROGRAMMING_LANGUAGES': [
        'Python', 'Java', 'JavaScript', 'TypeScript', 'C', 'C++', 'C#', 'Go', 'Rust', 
        'Ruby', 'PHP', 'Swift', 'Kotlin', 'Scala', 'R', 'MATLAB', 'Perl', 'Shell', 
        'Bash', 'PowerShell', 'SQL', 'HTML', 'CSS', 'Dart', 'Lua', 'Objective-C', 
        'Assembly', 'Groovy', 'Haskell', 'Elixir'
    ],
    'WEB_FRAMEWORKS': [
        'React', 'Angular', 'Vue.js', 'Next.js', 'Nuxt.js', 'Express.js', 'Node.js', 
        'Django', 'Flask', 'FastAPI', 'Spring Boot', 'Ruby on Rails', 'Laravel', 
        'ASP.NET', 'Svelte', 'Gatsby', 'Remix', 'Nest.js', 'jQuery', 'Bootstrap', 
        'Tailwind CSS', 'Material UI', 'Chakra UI'
    ],
    'DATABASES': [
        'MongoDB', 'MySQL', 'PostgreSQL', 'SQLite', 'Redis', 'Cassandra', 'DynamoDB', 
        'Firebase', 'Supabase', 'Neo4j', 'CouchDB', 'MariaDB', 'Oracle', 'SQL Server', 
        'Elasticsearch'
    ],
    'CLOUD_DEVOPS': [
        'AWS', 'Azure', 'GCP', 'Google Cloud', 'Docker', 'Kubernetes', 'Jenkins', 
        'GitHub Actions', 'GitLab CI', 'CircleCI', 'Terraform', 'Ansible', 'Nginx', 
        'Apache', 'Heroku', 'Vercel', 'Netlify', 'DigitalOcean', 'Cloudflare', 'Linux', 
        'CI/CD', 'Microservices'
    ],
    'ML_AI': [
        'TensorFlow', 'PyTorch', 'Scikit-learn', 'Keras', 'OpenCV', 'NLTK', 'spaCy', 
        'Hugging Face', 'Pandas', 'NumPy', 'SciPy', 'Matplotlib', 'Seaborn', 'Plotly', 
        'Jupyter', 'Machine Learning', 'Deep Learning', 'NLP', 'Natural Language Processing', 
        'Computer Vision', 'Reinforcement Learning', 'Neural Networks', 'XGBoost', 
        'LightGBM', 'Random Forest', 'Logistic Regression', 'SVM', 'Transformers', 
        'BERT', 'GPT', 'LLM', 'RAG', 'LangChain', 'MLflow'
    ],
    'TESTING': [
        'Jest', 'Mocha', 'Pytest', 'JUnit', 'Selenium', 'Cypress', 'Playwright', 
        'Postman', 'Swagger', 'Unit Testing', 'Integration Testing', 'E2E Testing', 
        'Test-Driven Development', 'TDD'
    ],
    'TOOLS': [
        'Git', 'GitHub', 'GitLab', 'Bitbucket', 'VS Code', 'IntelliJ', 'Eclipse', 
        'Jira', 'Confluence', 'Slack', 'Figma', 'Notion', 'Trello', 'Agile', 'Scrum', 
        'Kanban', 'REST API', 'GraphQL', 'gRPC', 'WebSocket', 'OAuth', 'JWT', 'Linux', 
        'Vim', 'Webpack', 'Vite', 'Babel', 'ESLint', 'Prettier'
    ],
    'SOFT_SKILLS': [
        'Leadership', 'Communication', 'Problem Solving', 'Teamwork', 'Critical Thinking', 
        'Project Management', 'Time Management', 'Mentoring', 'Collaboration', 'Presentation'
    ]
}

def extract_skills(text: str) -> dict:
    """
    Extracts skills from text using the predefined taxonomy.
    
    Args:
        text (str): The text to extract skills from.
        
    Returns:
        dict: A dictionary containing the list of found skills, categorized skills, and count.
    """
    if not text:
        return {'found_skills': [], 'categories': {}, 'count': 0}
        
    text_lower = text.lower()
    
    found_skills = []
    categories = {category: [] for category in SKILL_TAXONOMY}
    
    for category, skills in SKILL_TAXONOMY.items():
        for skill in skills:
            escaped_skill = re.escape(skill.lower())
            
            if skill.lower() in ['c++', 'c#', '.net', 'asp.net', 'vue.js', 'next.js', 'express.js', 'node.js']:
                pattern = r'(?<![a-zA-Z0-9])' + escaped_skill + r'(?![a-zA-Z0-9])'
            else:
                pattern = r'\b' + escaped_skill + r'\b'
                
            if re.search(pattern, text_lower):
                if skill not in found_skills:
                    found_skills.append(skill)
                    categories[category].append(skill)
                    
    categories = {k: v for k, v in categories.items() if v}
    
    return {
        'found_skills': sorted(found_skills),
        'categories': categories,
        'count': len(found_skills)
    }

def get_required_skills_for_role(role: str) -> list:
    """
    Returns expected skills for a given job role.
    
    Args:
        role (str): The job role.
        
    Returns:
        list: A list of expected skills.
    """
    role_mapping = {
        'Full Stack Developer': ['React', 'Node.js', 'MongoDB', 'Express.js', 'JavaScript', 'HTML', 'CSS', 'Git', 'REST API', 'SQL', 'Docker'],
        'Frontend Developer': ['React', 'JavaScript', 'HTML', 'CSS', 'TypeScript', 'Redux', 'Bootstrap', 'Tailwind CSS', 'Webpack', 'Figma'],
        'Backend Developer': ['Node.js', 'Python', 'Java', 'SQL', 'MongoDB', 'REST API', 'Docker', 'Redis', 'Microservices', 'Git'],
        'Data Scientist': ['Python', 'Pandas', 'NumPy', 'Scikit-learn', 'TensorFlow', 'SQL', 'Matplotlib', 'Jupyter', 'Machine Learning', 'Statistics'],
        'AI Engineer': ['Python', 'TensorFlow', 'PyTorch', 'NLP', 'Deep Learning', 'Machine Learning', 'Computer Vision', 'Hugging Face', 'Docker', 'MLflow'],
        'Cloud Engineer': ['AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'Terraform', 'Linux', 'CI/CD', 'Ansible', 'Microservices'],
        'DevOps Engineer': ['Docker', 'Kubernetes', 'Jenkins', 'AWS', 'Linux', 'Terraform', 'CI/CD', 'Ansible', 'Git', 'Monitoring'],
        'Android Developer': ['Java', 'Kotlin', 'Android SDK', 'Firebase', 'REST API', 'SQLite', 'Git', 'Material Design', 'Retrofit', 'Gradle'],
        'Java Developer': ['Java', 'Spring Boot', 'Hibernate', 'MySQL', 'REST API', 'Maven', 'JUnit', 'Microservices', 'Docker', 'Git'],
        'Python Developer': ['Python', 'Django', 'Flask', 'FastAPI', 'SQL', 'MongoDB', 'REST API', 'Docker', 'Git', 'Pandas']
    }
    
    return role_mapping.get(role, [])

def compare_skills(resume_skills: list, jd_text: str) -> dict:
    """
    Compares skills found in resume to those required in a Job Description (JD).
    
    Args:
        resume_skills (list): List of skills extracted from resume.
        jd_text (str): The raw job description text.
        
    Returns:
        dict: A dictionary containing matching skills, missing skills, and match percentage.
    """
    jd_extraction = extract_skills(jd_text)
    jd_skills = jd_extraction['found_skills']
    
    if not jd_skills:
        return {'matching': [], 'missing': [], 'match_percentage': 0.0}
        
    resume_skills_lower = [s.lower() for s in resume_skills]
    
    matching = []
    missing = []
    
    for jd_skill in jd_skills:
        if jd_skill.lower() in resume_skills_lower:
            matching.append(jd_skill)
        else:
            missing.append(jd_skill)
            
    match_percentage = (len(matching) / len(jd_skills)) * 100.0 if jd_skills else 0.0
    
    return {
        'matching': matching,
        'missing': missing,
        'match_percentage': round(match_percentage, 2)
    }
