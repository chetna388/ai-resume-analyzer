# AI Resume Analyzer

> Machine Learning Powered Resume Classification & ATS Evaluation System

A production-ready full-stack web application that analyzes resumes using **Machine Learning** and **Natural Language Processing**. Upload a PDF resume, select a target role, paste a job description — and get instant feedback on your ATS compatibility score, skill gaps, improvement recommendations, and interview prep questions.

---

## Features

- **ML Resume Classification** — Logistic Regression model classifies resumes into 10+ job domains
- **ATS Score (0–100)** — Weighted scoring across 5 dimensions (similarity, skills, structure, projects, keywords)
- **Skill Extraction** — Detects 150+ technical skills across 8 categories
- **Missing Skill Detection** — Compares your skills against job description requirements
- **Improvement Recommendations** — Courses, certifications, project ideas, resume tips
- **Interview Question Generator** — 5 rule-based questions tailored to your detected skills
- **PDF Report Download** — Export analysis results as a text-based PDF
- **Resume History** — Track all past analyses with ATS scores and categories
- **JWT Authentication** — Secure user registration, login, and protected routes
- **Dark Mode UI** — Premium glassmorphism design with Recharts data visualization

---

## Tech Stack

| Layer | Technologies |
|-------|-------------|
| Frontend | React 18, Tailwind CSS v3 (CDN), Recharts, Axios, React Router v6 |
| Backend | Python, Flask, Flask-CORS, PyJWT |
| ML/NLP | scikit-learn, spaCy, TF-IDF, Cosine Similarity, Logistic Regression |
| PDF | PyMuPDF (fitz) |
| Database | SQLite |
| Auth | JWT + Werkzeug password hashing |

---

## Project Structure

```
ai-resume-analyzer/
├── client/                      # React Frontend
│   ├── src/
│   │   ├── components/          # Reusable UI components
│   │   ├── pages/               # Page components (8 pages)
│   │   ├── services/            # API service layer
│   │   ├── hooks/               # Custom React hooks
│   │   ├── context/             # Auth context provider
│   │   ├── App.jsx              # Main app with routing
│   │   └── index.css            # Design system
│   ├── package.json
│   └── vite.config.js
│
├── server/                      # Flask Backend
│   ├── ml/                      # ML training & prediction
│   │   ├── train_model.py       # Training pipeline
│   │   ├── predictor.py         # Model loading & inference
│   │   └── evaluator.py         # Metrics & evaluation
│   ├── nlp/                     # NLP processing
│   │   ├── preprocessor.py      # Text cleaning pipeline
│   │   ├── skill_extractor.py   # Skill detection (150+ skills)
│   │   └── similarity.py        # Cosine similarity
│   ├── utils/                   # Utility modules
│   │   ├── pdf_parser.py        # PDF text extraction
│   │   ├── ats_scorer.py        # Weighted ATS scoring
│   │   ├── recommendations.py   # Recommendation engine
│   │   ├── interview_questions.py # Question generator
│   │   └── auth_helpers.py      # JWT & password utilities
│   ├── routes/                  # API route blueprints
│   ├── controllers/             # Business logic
│   ├── models/                  # Database schema
│   ├── dataset/                 # Training dataset (CSV)
│   ├── trained_model/           # Saved .pkl model files
│   ├── uploads/                 # Uploaded resume PDFs
│   ├── app.py                   # Flask entry point
│   ├── config.py                # Configuration
│   └── requirements.txt
└── README.md
```

---

## Getting Started

### Prerequisites

- **Python 3.9+**
- **Node.js 18+**
- **npm 9+**

### 1. Clone & Setup Backend

```bash
cd server

# Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# Install Python dependencies
pip install -r requirements.txt

# Download spaCy language model
python -m spacy download en_core_web_sm
```

### 2. Download Dataset & Train Model

1. Download the **Updated Resume Dataset** from Kaggle:
   https://www.kaggle.com/datasets/gauravduttakiit/resume-dataset

2. Place `UpdatedResumeDataSet.csv` in `server/dataset/`

3. Train the model:
```bash
cd server
python ml/train_model.py
```

> The model will be saved to `server/trained_model/`. Without training, the app still works but category prediction will show "Unknown".

### 3. Start Backend Server

```bash
cd server
python app.py
```

The Flask API will start on `http://localhost:5000`.

### 4. Setup & Start Frontend

```bash
cd client

# Install dependencies
npm install

# Start dev server
npm run dev
```

The React app will start on `http://localhost:5173` with API proxy to port 5000.

---

## API Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/api/register` | No | User registration |
| POST | `/api/login` | No | User login → JWT token |
| POST | `/api/upload-resume` | Yes | Upload PDF, extract text |
| POST | `/api/predict-category` | Yes | Classify resume category |
| POST | `/api/analyze-resume` | Yes | Full analysis pipeline |
| POST | `/api/compare-job-description` | Yes | Resume vs JD comparison |
| GET | `/api/history` | Yes | Past analyses |
| GET | `/api/profile` | Yes | User profile & stats |

---

## ML Pipeline

```
Dataset (CSV) → Text Preprocessing (spaCy) → TF-IDF Vectorization
→ Logistic Regression → Model Evaluation → Save Model (.pkl)
```

**Preprocessing**: Lowercase → Remove URLs/emails → Tokenize → Remove stopwords → Lemmatize → Clean

**Model**: Logistic Regression with TF-IDF features (max_features=5000, ngram_range=(1,2))

---

## ATS Scoring Formula

| Component | Weight | Method |
|-----------|--------|--------|
| Resume-JD Similarity | 50% | Cosine similarity of TF-IDF vectors |
| Skill Match | 25% | matched_skills / required_skills |
| Resume Structure | 10% | Presence of key sections |
| Project Relevance | 10% | JD keyword overlap in projects |
| Keyword Presence | 5% | Action verbs and power words |

Final score: 0–100 with letter grade (A+ to F)

---

## Key Concepts for Interview

- **TF-IDF**: Term Frequency–Inverse Document Frequency for text vectorization
- **Cosine Similarity**: Measures angle between two text vectors (0=different, 1=identical)
- **Logistic Regression**: Linear classifier with softmax for multi-class prediction
- **NLP Pipeline**: Tokenization → Lemmatization → Stopword removal
- **JWT Authentication**: Stateless token-based auth with expiration
- **REST API Design**: Proper HTTP methods, status codes, error handling
- **Component Architecture**: Reusable React components with hooks and context

---

## License

This project is for educational purposes. Built as a portfolio project for technical interviews.
