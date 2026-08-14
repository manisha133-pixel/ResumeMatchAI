# 🚀 ResumeMatch AI

ResumeMatch AI is a web-based Resume Analyzer and Job Matcher built using Python and Flask.

It analyzes a candidate's resume against a target job description and provides a Resume Match Score, matched skills, missing skills, detected job role, strengths, weaknesses, and improvement recommendations.

---

## ✨ Features

- 📄 Upload resume in PDF format
- 📝 Enter target job description
- 🔍 Extract text from PDF resumes
- 🛠️ Detect technical skills
- 🟢 Identify matched skills
- 🔴 Identify missing skills
- 🎯 Detect the target job role
- 📊 Calculate Resume Match Score
- 🧠 Calculate text similarity using TF-IDF
- 💪 Identify resume strengths
- ⚠️ Identify resume weaknesses
- 💡 Generate improvement recommendations
- 📥 Download Resume Analysis Report as PDF

---

## 🛠️ Tech Stack

- Python
- Flask
- PyPDF2
- Scikit-learn
- TF-IDF
- Cosine Similarity
- ReportLab
- HTML
- CSS
- Git
- GitHub

---

## 🧠 How It Works

The application follows this workflow:

Resume PDF
        ↓
PDF Text Extraction
        ↓
Text Processing
        ↓
Skill Detection
        ↓
Job Description Analysis
        ↓
Matched & Missing Skills
        ↓
TF-IDF Text Similarity
        ↓
Overall Match Score
        ↓
Resume Recommendations
        ↓
PDF Analysis Report

---

## 📊 Scoring

The current version calculates the overall score using:

- 60% Skill Match
- 40% Text Similarity

### Formula

Overall Score =

(Skill Match × 0.60) +
(Text Similarity × 0.40)

---

## 🎯 Supported Job Roles

The current version can identify roles such as:

- Data Analyst
- Python Developer
- Data Scientist
- Machine Learning Engineer
- Web Developer

---

## 📁 Project Structure

```text
ResumeMatchAI/
│
├── app.py
├── requirements.txt
├── README.md
│
├── templates/
│   └── index.html
│
└── static/
    └── style.css