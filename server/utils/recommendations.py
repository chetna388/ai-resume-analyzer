import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.pdf_parser import extract_sections

# Comprehensive curated data
COURSE_DATABASE = {
    'Python': {'course_name': 'Python for Everybody Specialization', 'platform': 'Coursera', 'url': 'https://www.coursera.org/specializations/python'},
    'Java': {'course_name': 'Java Programming and Software Engineering Fundamentals', 'platform': 'Coursera', 'url': 'https://www.coursera.org/specializations/java-programming'},
    'JavaScript': {'course_name': 'Modern JavaScript From The Beginning', 'platform': 'Udemy', 'url': 'https://www.udemy.com/course/modern-javascript-from-the-beginning/'},
    'React': {'course_name': 'React - The Complete Guide', 'platform': 'Udemy', 'url': 'https://www.udemy.com/course/react-the-complete-guide-incl-redux/'},
    'Node.js': {'course_name': 'NodeJS - The Complete Guide', 'platform': 'Udemy', 'url': 'https://www.udemy.com/course/nodejs-the-complete-guide/'},
    'Docker': {'course_name': 'Docker Mastery: with Kubernetes +Swarm', 'platform': 'Udemy', 'url': 'https://www.udemy.com/course/docker-mastery/'},
    'Kubernetes': {'course_name': 'Kubernetes for the Absolute Beginners', 'platform': 'Udemy', 'url': 'https://www.udemy.com/course/learn-kubernetes/'},
    'AWS': {'course_name': 'AWS Certified Solutions Architect - Associate', 'platform': 'Udemy', 'url': 'https://www.udemy.com/course/aws-certified-solutions-architect-associate-saa-c03/'},
    'Machine Learning': {'course_name': 'Machine Learning Specialization', 'platform': 'Coursera', 'url': 'https://www.coursera.org/specializations/machine-learning'},
    'Deep Learning': {'course_name': 'Deep Learning Specialization', 'platform': 'Coursera', 'url': 'https://www.coursera.org/specializations/deep-learning'},
    'SQL': {'course_name': 'The Complete SQL Bootcamp', 'platform': 'Udemy', 'url': 'https://www.udemy.com/course/the-complete-sql-bootcamp/'},
    'MongoDB': {'course_name': 'MongoDB - The Complete Developer\'s Guide', 'platform': 'Udemy', 'url': 'https://www.udemy.com/course/mongodb-the-complete-developers-guide/'},
    'TensorFlow': {'course_name': 'DeepLearning.AI TensorFlow Developer', 'platform': 'Coursera', 'url': 'https://www.coursera.org/professional-certificates/tensorflow-in-practice'},
    'Pandas': {'course_name': 'Data Analysis with Pandas and Python', 'platform': 'Udemy', 'url': 'https://www.udemy.com/course/data-analysis-with-pandas/'},
    'Spring Boot': {'course_name': 'Spring & Hibernate for Beginners', 'platform': 'Udemy', 'url': 'https://www.udemy.com/course/spring-hibernate-tutorial/'},
    'C++': {'course_name': 'Beginning C++ Programming', 'platform': 'Udemy', 'url': 'https://www.udemy.com/course/beginning-c-plus-plus-programming/'},
    'C#': {'course_name': 'C# Basics for Beginners', 'platform': 'Udemy', 'url': 'https://www.udemy.com/course/csharp-tutorial-for-beginners/'},
    'Azure': {'course_name': 'AZ-900: Microsoft Azure Fundamentals', 'platform': 'Udemy', 'url': 'https://www.udemy.com/course/microsoft-azure-beginners-guide/'},
    'GCP': {'course_name': 'Google Cloud Digital Leader Certification', 'platform': 'Coursera', 'url': 'https://www.coursera.org/professional-certificates/google-cloud-digital-leader'},
    'Linux': {'course_name': 'Linux Mastery: Master the Linux Command Line', 'platform': 'Udemy', 'url': 'https://www.udemy.com/course/linux-mastery/'},
    'Git': {'course_name': 'Git Complete: The definitive, step-by-step guide', 'platform': 'Udemy', 'url': 'https://www.udemy.com/course/git-complete/'},
    'CI/CD': {'course_name': 'Continuous Integration and Continuous Delivery', 'platform': 'Coursera', 'url': 'https://www.coursera.org/learn/continuous-integration'},
    'Django': {'course_name': 'Python and Django Full Stack Web Developer Bootcamp', 'platform': 'Udemy', 'url': 'https://www.udemy.com/course/python-and-django-full-stack-web-developer-bootcamp/'},
    'Flask': {'course_name': 'REST APIs with Flask and Python', 'platform': 'Udemy', 'url': 'https://www.udemy.com/course/rest-api-flask-and-python/'},
    'Angular': {'course_name': 'Angular - The Complete Guide', 'platform': 'Udemy', 'url': 'https://www.udemy.com/course/the-complete-guide-to-angular-2/'},
    'Vue.js': {'course_name': 'Vue - The Complete Guide', 'platform': 'Udemy', 'url': 'https://www.udemy.com/course/vuejs-2-the-complete-guide/'},
    'TypeScript': {'course_name': 'Understanding TypeScript', 'platform': 'Udemy', 'url': 'https://www.udemy.com/course/understanding-typescript/'},
    'NLP': {'course_name': 'Natural Language Processing Specialization', 'platform': 'Coursera', 'url': 'https://www.coursera.org/specializations/natural-language-processing'},
    'Computer Vision': {'course_name': 'Computer Vision Fundamentals', 'platform': 'Coursera', 'url': 'https://www.coursera.org/learn/computer-vision-fundamentals'},
    'Terraform': {'course_name': 'Terraform for the Absolute Beginners', 'platform': 'Udemy', 'url': 'https://www.udemy.com/course/terraform-for-the-absolute-beginners/'}
}

PROJECT_SUGGESTIONS = {
    'Full Stack Developer': [
        {'title': 'E-commerce Platform', 'description': 'Build a full e-commerce store with user authentication, product management, cart, and Stripe payment integration.', 'skills_demonstrated': 'React, Node.js, Express, MongoDB, Redux, Stripe API'},
        {'title': 'Social Media Dashboard', 'description': 'Create a responsive dashboard showing real-time metrics with data visualization.', 'skills_demonstrated': 'Vue.js/React, D3.js/Chart.js, REST APIs, CSS Grid'},
        {'title': 'Task Management System', 'description': 'Trello-clone with drag-and-drop functionality, workspaces, and real-time updates.', 'skills_demonstrated': 'TypeScript, Next.js, PostgreSQL, WebSockets'},
        {'title': 'Blog with CMS', 'description': 'A complete blogging platform with a custom admin panel, rich text editor, and SEO optimization.', 'skills_demonstrated': 'Django/Flask, Python, SQL, HTML/CSS'},
        {'title': 'Real-time Chat Application', 'description': 'Multi-room chat app with file sharing, typing indicators, and read receipts.', 'skills_demonstrated': 'MERN Stack, Socket.io, JWT Authentication'}
    ],
    'Frontend Developer': [
        {'title': 'Interactive Weather App', 'description': 'Weather forecast using third-party APIs, geolocation, and dynamic background based on weather.', 'skills_demonstrated': 'JavaScript, REST API, HTML/CSS, Geolocation'},
        {'title': 'Netflix Clone', 'description': 'Pixel-perfect UI clone of Netflix with trailer playing capabilities using TMDB API.', 'skills_demonstrated': 'React, Redux, Firebase, Styled Components'},
        {'title': 'Animated Portfolio', 'description': 'Personal portfolio with scroll animations, 3D elements, and responsive design.', 'skills_demonstrated': 'Three.js, GSAP, HTML5, CSS3'},
        {'title': 'Expense Tracker', 'description': 'Client-side application to track income/expenses with visual charts and local storage.', 'skills_demonstrated': 'React/Angular, Chart.js, LocalStorage'},
        {'title': 'Job Board UI', 'description': 'Modern job board interface with advanced filtering, search, and pagination.', 'skills_demonstrated': 'Vue.js, Tailwind CSS, State Management'}
    ],
    'Backend Developer': [
        {'title': 'RESTful API for Book Store', 'description': 'Comprehensive API with CRUD operations, filtering, sorting, pagination, and role-based access.', 'skills_demonstrated': 'Node.js/Python, Express/FastAPI, MongoDB/PostgreSQL, JWT'},
        {'title': 'Microservices E-commerce', 'description': 'Decomposed backend into user, product, and order services communicating via message broker.', 'skills_demonstrated': 'Java Spring Boot, RabbitMQ/Kafka, Docker'},
        {'title': 'URL Shortener', 'description': 'System design classic with redirect functionality, analytics tracking, and rate limiting.', 'skills_demonstrated': 'Go/Python, Redis, SQL, Nginx'},
        {'title': 'Web Scraper & API', 'description': 'Automated scheduled scraper that processes data and serves it via GraphQL.', 'skills_demonstrated': 'Python, BeautifulSoup/Scrapy, GraphQL, Celery'},
        {'title': 'Authentication Server', 'description': 'OAuth2.0 provider implementation with MFA support and session management.', 'skills_demonstrated': 'Node.js, Passport.js, Redis, Security Best Practices'}
    ],
    'Data Scientist': [
        {'title': 'Customer Churn Prediction', 'description': 'End-to-end pipeline to predict which customers will leave, with feature importance analysis.', 'skills_demonstrated': 'Python, Pandas, Scikit-learn, XGBoost'},
        {'title': 'Recommendation System', 'description': 'Collaborative and content-based filtering system for movies or products.', 'skills_demonstrated': 'Python, Matrix Factorization, Cosine Similarity'},
        {'title': 'Sales Forecasting', 'description': 'Time series forecasting for retail sales with seasonality handling.', 'skills_demonstrated': 'ARIMA, Prophet, Pandas, Matplotlib'},
        {'title': 'Sentiment Analysis on Twitter Data', 'description': 'Pipeline to stream tweets, classify sentiment, and visualize trends.', 'skills_demonstrated': 'NLP, NLTK, API integration, Tableau/PowerBI'},
        {'title': 'Interactive Data Dashboard', 'description': 'Web dashboard presenting insights from a complex dataset with interactive filters.', 'skills_demonstrated': 'Streamlit/Dash, Plotly, Data Wrangling'}
    ],
    'AI Engineer': [
        {'title': 'RAG-based Document Q&A', 'description': 'Upload PDFs and ask questions using LangChain and a vector database.', 'skills_demonstrated': 'LangChain, OpenAI API/LLama, Pinecone/Chroma, Python'},
        {'title': 'Image Classification Service', 'description': 'Custom CNN or fine-tuned ResNet exposed via REST API for object detection.', 'skills_demonstrated': 'PyTorch/TensorFlow, FastAPI, Docker'},
        {'title': 'Voice Assistant', 'description': 'Speech-to-text, intent recognition, and text-to-speech application.', 'skills_demonstrated': 'Whisper API, NLP, Audio Processing'},
        {'title': 'Code Generation Tool', 'description': 'Fine-tuned LLM for generating boilerplate code for a specific framework.', 'skills_demonstrated': 'Hugging Face, Peft/LoRA, Transformers'},
        {'title': 'Autonomous Trading Bot', 'description': 'Reinforcement learning agent trained to trade crypto/stocks based on historical data.', 'skills_demonstrated': 'Reinforcement Learning, Gym, Pandas'}
    ],
    'Cloud Engineer': [
        {'title': 'Serverless Image Processing', 'description': 'Pipeline that triggers on image upload, resizes, and stores results.', 'skills_demonstrated': 'AWS Lambda, S3, EventBridge, IAM'},
        {'title': 'Multi-tier Architecture Automation', 'description': 'Infrastructure as Code template for deploying a secure VPC, RDS, and Auto-scaling groups.', 'skills_demonstrated': 'Terraform/CloudFormation, AWS/Azure, Networking'},
        {'title': 'Highly Available Web App', 'description': 'Deploy an application with Load Balancer across multiple availability zones with CDN.', 'skills_demonstrated': 'ALB, CloudFront, EC2/VMs, Route53'},
        {'title': 'Cost Optimization Dashboard', 'description': 'Tool to aggregate cloud billing data and suggest right-sizing opportunities.', 'skills_demonstrated': 'Cloud APIs, Python, Dashboarding'},
        {'title': 'Disaster Recovery Setup', 'description': 'Automated cross-region database replication and failover mechanism.', 'skills_demonstrated': 'RDS Multi-AZ, Automation Scripts, Cloud Architecture'}
    ],
    'DevOps Engineer': [
        {'title': 'End-to-End CI/CD Pipeline', 'description': 'Pipeline that lints, tests, builds Docker image, and deploys to Kubernetes.', 'skills_demonstrated': 'Jenkins/GitLab CI, Docker, Kubernetes, Helm'},
        {'title': 'Infrastructure Monitoring System', 'description': 'Setup Prometheus and Grafana to monitor cluster metrics with alerting.', 'skills_demonstrated': 'Prometheus, Grafana, Alertmanager'},
        {'title': 'GitOps Deployment', 'description': 'Use ArgoCD to deploy and manage state of applications in Kubernetes.', 'skills_demonstrated': 'ArgoCD, Kubernetes, Git'},
        {'title': 'Automated Log Aggregation', 'description': 'ELK/EFK stack deployment for centralized logging across microservices.', 'skills_demonstrated': 'Elasticsearch, Fluentd/Logstash, Kibana'},
        {'title': 'Configuration Management', 'description': 'Ansible playbooks to provision and secure a fleet of Linux servers.', 'skills_demonstrated': 'Ansible, Linux, Security Auditing'}
    ],
    'Android Developer': [
        {'title': 'Fitness Tracking App', 'description': 'App utilizing sensors to track steps, run distance, and integrate with Google Fit.', 'skills_demonstrated': 'Kotlin, Android SDK, SensorManager, Room Database'},
        {'title': 'News Reader App', 'description': 'App fetching news from REST API with offline caching and MVVM architecture.', 'skills_demonstrated': 'Retrofit, Coroutines, LiveData/Flow, MVVM'},
        {'title': 'Social Networking App', 'description': 'Firebase-backed app with user profiles, post feed, and push notifications.', 'skills_demonstrated': 'Firebase Auth/Firestore, FCM, Glide'},
        {'title': 'E-commerce Android Client', 'description': 'Product catalog, shopping cart, and payment gateway integration.', 'skills_demonstrated': 'Jetpack Compose, Payment SDK, Dependency Injection (Dagger/Hilt)'},
        {'title': 'Media Player App', 'description': 'Audio/Video player with background playback and media controls.', 'skills_demonstrated': 'ExoPlayer, MediaSession, Foreground Services'}
    ],
    'Java Developer': [
        {'title': 'Banking System API', 'description': 'Core banking API with transaction management, concurrency control, and audit logs.', 'skills_demonstrated': 'Java 17, Spring Boot, Hibernate, MySQL'},
        {'title': 'Inventory Management System', 'description': 'Enterprise application with complex business rules, role-based access, and reporting.', 'skills_demonstrated': 'Spring Security, JPA, REST, JUnit'},
        {'title': 'Message Broker Producer/Consumer', 'description': 'Asynchronous processing system handling high throughput events.', 'skills_demonstrated': 'Java, Kafka/RabbitMQ, Multi-threading'},
        {'title': 'Legacy Migration Proxy', 'description': 'Strangler pattern implementation to slowly migrate from monolith to microservices.', 'skills_demonstrated': 'Spring Cloud Gateway, Resilience4j'},
        {'title': 'Batch Processing Engine', 'description': 'System to process millions of records from CSV to database nightly.', 'skills_demonstrated': 'Spring Batch, JDBC Optimization, Scheduling'}
    ],
    'Python Developer': [
        {'title': 'Social Media API', 'description': 'Robust API with Django Rest Framework handling users, followers, and feed generation.', 'skills_demonstrated': 'Django, DRF, PostgreSQL, Celery'},
        {'title': 'Automated Testing Framework', 'description': 'Custom wrapper around Pytest for E2E testing of web applications.', 'skills_demonstrated': 'Python, Pytest, Selenium, OOP'},
        {'title': 'Financial Data Aggregator', 'description': 'Async script fetching stock data from multiple APIs and normalizing it.', 'skills_demonstrated': 'Asyncio, Aiohttp, Pandas'},
        {'title': 'CLI Utility Tool', 'description': 'Command-line tool for developer productivity (e.g., scaffolding projects).', 'skills_demonstrated': 'Click/Argparse, File I/O, Subprocess'},
        {'title': 'Real-time Dashboard Backend', 'description': 'FastAPI application serving real-time data via WebSockets.', 'skills_demonstrated': 'FastAPI, WebSockets, Redis, Uvicorn'}
    ]
}

CERTIFICATION_DATABASE = [
    {'name': 'AWS Certified Solutions Architect', 'provider': 'Amazon Web Services', 'relevance': ['Cloud Engineer', 'DevOps Engineer', 'Backend Developer', 'Full Stack Developer']},
    {'name': 'AWS Certified Developer', 'provider': 'Amazon Web Services', 'relevance': ['Backend Developer', 'Full Stack Developer', 'Cloud Engineer']},
    {'name': 'Microsoft Certified: Azure Administrator', 'provider': 'Microsoft', 'relevance': ['Cloud Engineer', 'DevOps Engineer']},
    {'name': 'Google Cloud Professional Cloud Architect', 'provider': 'Google', 'relevance': ['Cloud Engineer', 'DevOps Engineer']},
    {'name': 'Certified Kubernetes Administrator (CKA)', 'provider': 'Cloud Native Computing Foundation', 'relevance': ['DevOps Engineer', 'Cloud Engineer']},
    {'name': 'Oracle Certified Professional: Java SE Developer', 'provider': 'Oracle', 'relevance': ['Java Developer', 'Backend Developer']},
    {'name': 'TensorFlow Developer Certificate', 'provider': 'Google', 'relevance': ['AI Engineer', 'Data Scientist']},
    {'name': 'Certified Ethical Hacker (CEH)', 'provider': 'EC-Council', 'relevance': ['Cloud Engineer', 'Backend Developer']},
    {'name': 'CompTIA Security+', 'provider': 'CompTIA', 'relevance': ['Cloud Engineer', 'DevOps Engineer']},
    {'name': 'Scrum Master Certified', 'provider': 'Scrum Alliance', 'relevance': ['Full Stack Developer', 'Backend Developer', 'Frontend Developer']},
    {'name': 'Cisco Certified Network Associate (CCNA)', 'provider': 'Cisco', 'relevance': ['Cloud Engineer']},
    {'name': 'Red Hat Certified Engineer (RHCE)', 'provider': 'Red Hat', 'relevance': ['DevOps Engineer', 'Cloud Engineer']},
    {'name': 'MongoDB Certified Developer', 'provider': 'MongoDB', 'relevance': ['Backend Developer', 'Full Stack Developer']},
    {'name': 'HashiCorp Certified: Terraform Associate', 'provider': 'HashiCorp', 'relevance': ['DevOps Engineer', 'Cloud Engineer']},
    {'name': 'Databricks Certified Data Engineer', 'provider': 'Databricks', 'relevance': ['Data Scientist', 'AI Engineer']},
    {'name': 'Google Data Analytics Professional Certificate', 'provider': 'Coursera', 'relevance': ['Data Scientist']},
    {'name': 'IBM Data Science Professional Certificate', 'provider': 'Coursera', 'relevance': ['Data Scientist']},
    {'name': 'Meta Front-End Developer Professional Certificate', 'provider': 'Coursera', 'relevance': ['Frontend Developer', 'Full Stack Developer']},
    {'name': 'Meta Back-End Developer Professional Certificate', 'provider': 'Coursera', 'relevance': ['Backend Developer', 'Python Developer', 'Full Stack Developer']},
    {'name': 'Android Associate Developer', 'provider': 'Google', 'relevance': ['Android Developer']}
]

def generate_recommendations(category: str, resume_skills: list, missing_skills: list, ats_score: float, resume_text: str) -> dict:
    """
    Generates rule-based recommendations for resume improvement.
    
    Args:
        category (str): The predicted job category.
        resume_skills (list): Skills found in the resume.
        missing_skills (list): Skills missing from the job requirements.
        ats_score (float): The calculated ATS score.
        resume_text (str): The raw text of the resume.
        
    Returns:
        dict: A comprehensive dictionary of recommendations, courses, projects, etc.
    """
    
    # 1. Missing Skills with Importance
    processed_missing_skills = []
    for i, skill in enumerate(missing_skills):
        importance = 'High' if i < len(missing_skills) * 0.3 else 'Medium' if i < len(missing_skills) * 0.7 else 'Low'
        processed_missing_skills.append({
            'skill': skill,
            'importance': importance
        })

    # 2. Courses Recommendations
    courses = []
    for skill in missing_skills:
        # Check exact or case-insensitive match in our database
        matched_course = next((data for key, data in COURSE_DATABASE.items() if key.lower() == skill.lower()), None)
        if matched_course:
            courses.append({
                'skill': skill,
                'course_name': matched_course['course_name'],
                'platform': matched_course['platform'],
                'url': matched_course['url']
            })
            
        # Limit to top 5 courses to not overwhelm
        if len(courses) >= 5:
            break

    # 3. Project Suggestions
    project_suggestions = []
    # Use exact match or default to Full Stack if category not found
    cat_projects = PROJECT_SUGGESTIONS.get(category)
    if cat_projects:
        project_suggestions = cat_projects[:3] # Suggest top 3

    # 4. Resume Section Analysis & Weaknesses
    sections = extract_sections(resume_text)
    expected_sections = ['Summary', 'Experience', 'Education', 'Skills', 'Projects']
    
    weak_sections = []
    for section in expected_sections:
        if not sections.get(section):
            weak_sections.append({
                'section': section,
                'issue': 'Missing completely',
                'suggestion': f'Add a dedicated "{section}" section to make your resume ATS-friendly and provide complete context.'
            })
        elif len(sections.get(section, '')) < 50 and section != 'Skills':
            weak_sections.append({
                'section': section,
                'issue': 'Too brief',
                'suggestion': f'Expand the "{section}" section with more details and specific achievements.'
            })
            
    # 5. Improvements
    improvements = []
    if ats_score < 70:
        improvements.append({
            'area': 'Overall ATS Compatibility',
            'suggestion': 'Tailor your resume more specifically to the job description by including exact keywords.',
            'priority': 'High'
        })
    if len(missing_skills) > 3:
        improvements.append({
            'area': 'Skill Gap',
            'suggestion': 'Focus on acquiring the missing high-priority skills or highlight equivalent experience if you already have it.',
            'priority': 'High'
        })
    if not sections.get('Summary'):
        improvements.append({
            'area': 'Professional Summary',
            'suggestion': 'Add a compelling 2-3 sentence summary highlighting your years of experience and key strengths.',
            'priority': 'Medium'
        })
        
    # 6. Missing Keywords Analysis (Action Verbs)
    action_verbs = ['developed', 'designed', 'optimized', 'led', 'managed', 'implemented', 'orchestrated', 'architected', 'reduced', 'increased', 'achieved']
    missing_keywords = [verb for verb in action_verbs if verb not in resume_text.lower()]
    
    # 7. Certifications
    certifications = [
        cert for cert in CERTIFICATION_DATABASE 
        if category in cert['relevance'] or 'Full Stack Developer' in cert['relevance']
    ][:3] # Limit to top 3

    return {
        'missing_skills': processed_missing_skills,
        'courses': courses,
        'improvements': improvements,
        'project_suggestions': project_suggestions,
        'missing_keywords': missing_keywords,
        'weak_sections': weak_sections,
        'certifications': certifications
    }
