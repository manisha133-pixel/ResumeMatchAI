from flask import Flask, render_template, request, send_file
from PyPDF2 import PdfReader

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

import io


app = Flask(__name__)


# ==========================================
# SKILLS DATABASE
# ==========================================

SKILLS = [
    "python",
    "sql",
    "excel",
    "power bi",
    "tableau",
    "machine learning",
    "data analysis",
    "data visualization",
    "pandas",
    "numpy",
    "matplotlib",
    "seaborn",
    "flask",
    "java",
    "c++",
    "html",
    "css",
    "javascript",
    "git",
    "github",
    "statistics",
    "scikit-learn",
    "tensorflow",
    "keras",
    "deep learning",
    "nlp",
    "artificial intelligence",
    "aws",
    "azure",
    "google cloud",
    "mongodb",
    "mysql",
    "postgresql",
    "powerpoint",
    "word",
    "communication",
    "problem solving"
]


# ==========================================
# JOB ROLES
# ==========================================

JOB_ROLES = {

    "Data Analyst": [
        "data analyst",
        "data analysis",
        "sql",
        "excel",
        "power bi",
        "tableau",
        "data visualization"
    ],

    "Python Developer": [
        "python",
        "flask",
        "django",
        "api",
        "git",
        "github"
    ],

    "Data Scientist": [
        "python",
        "machine learning",
        "pandas",
        "numpy",
        "scikit-learn",
        "statistics",
        "data analysis"
    ],

    "Machine Learning Engineer": [
        "python",
        "machine learning",
        "tensorflow",
        "keras",
        "scikit-learn",
        "deep learning"
    ],

    "Web Developer": [
        "html",
        "css",
        "javascript",
        "flask",
        "python"
    ]
}


# ==========================================
# PDF TEXT EXTRACTION
# ==========================================

def extract_text_from_pdf(file):

    reader = PdfReader(file)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


# ==========================================
# FIND SKILLS
# ==========================================

def find_skills(text):

    text = text.lower()

    found_skills = []

    for skill in SKILLS:

        if skill in text:
            found_skills.append(skill)

    return found_skills


# ==========================================
# DETECT JOB ROLE
# ==========================================

def detect_job_role(job_description):

    text = job_description.lower()

    role_scores = {}

    for role, keywords in JOB_ROLES.items():

        score = 0

        for keyword in keywords:

            if keyword in text:
                score += 1

        role_scores[role] = score

    if max(role_scores.values()) == 0:
        return "General / Other"

    return max(
        role_scores,
        key=role_scores.get
    )


# ==========================================
# TF-IDF SIMILARITY
# ==========================================

def calculate_similarity(
    resume_text,
    job_description
):

    documents = [
        resume_text.lower(),
        job_description.lower()
    ]

    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    tfidf_matrix = vectorizer.fit_transform(
        documents
    )

    similarity = cosine_similarity(
        tfidf_matrix[0:1],
        tfidf_matrix[1:2]
    )[0][0]

    return round(similarity * 100)


# ==========================================
# GENERATE SUGGESTIONS
# ==========================================

def generate_suggestions(
    missing_skills,
    matched_skills,
    detected_role
):

    strengths = []
    weaknesses = []
    suggestions = []


    # Strengths

    if matched_skills:

        strengths.append(
            f"Your resume matches {len(matched_skills)} key skill(s) from the job description."
        )

        strengths.append(
            "You already have some relevant technical skills for this position."
        )

    else:

        strengths.append(
            "Your resume currently has limited overlap with the required skills."
        )


    # Weaknesses

    if missing_skills:

        weaknesses.append(
            f"{len(missing_skills)} important skill(s) from the job description were not detected."
        )

        weaknesses.append(
            "Some job-specific technical skills may need to be highlighted more clearly."
        )

    else:

        weaknesses.append(
            "No major missing skills were detected from the current skill database."
        )


    # Role-specific suggestions

    if detected_role == "Data Analyst":

        suggestions.append(
            "Highlight SQL, Excel, Power BI, Tableau and data visualization projects."
        )

        suggestions.append(
            "Add measurable results to your data analysis projects whenever possible."
        )


    elif detected_role == "Python Developer":

        suggestions.append(
            "Highlight Python projects and backend development experience."
        )

        suggestions.append(
            "Mention Flask/Django, APIs and Git/GitHub if you have used them."
        )


    elif detected_role == "Data Scientist":

        suggestions.append(
            "Highlight Python, Pandas, NumPy, statistics and machine learning projects."
        )

        suggestions.append(
            "Include model evaluation results and datasets used in your projects."
        )


    elif detected_role == "Machine Learning Engineer":

        suggestions.append(
            "Highlight machine learning projects and model-building experience."
        )

        suggestions.append(
            "Mention Scikit-learn, TensorFlow or other ML frameworks you have used."
        )


    elif detected_role == "Web Developer":

        suggestions.append(
            "Highlight HTML, CSS and JavaScript projects."
        )

        suggestions.append(
            "Mention web frameworks and deployed applications if applicable."
        )


    # Missing skill suggestions

    for skill in missing_skills:

        suggestions.append(
            f"Consider adding '{skill}' to your resume if you have genuine experience with it."
        )


    return (
        strengths,
        weaknesses,
        suggestions
    )


# ==========================================
# ANALYZE RESUME
# ==========================================

def analyze_resume(
    resume_text,
    job_description
):

    resume_skills = find_skills(
        resume_text
    )

    job_skills = find_skills(
        job_description
    )


    matched_skills = list(
        set(resume_skills)
        &
        set(job_skills)
    )


    missing_skills = list(
        set(job_skills)
        -
        set(resume_skills)
    )


    # Skill score

    if len(job_skills) > 0:

        skill_score = (
            len(matched_skills)
            /
            len(job_skills)
        ) * 100

    else:

        skill_score = 0


    skill_score = round(skill_score)


    # Text similarity

    similarity_score = calculate_similarity(
        resume_text,
        job_description
    )


    # Final score

    final_score = round(
        (skill_score * 0.6)
        +
        (similarity_score * 0.4)
    )


    # Job role

    detected_role = detect_job_role(
        job_description
    )


    # Suggestions

    (
        strengths,
        weaknesses,
        suggestions
    ) = generate_suggestions(
        missing_skills,
        matched_skills,
        detected_role
    )


    return {

        "matched": matched_skills,

        "missing": missing_skills,

        "score": final_score,

        "skill_score": skill_score,

        "similarity": similarity_score,

        "role": detected_role,

        "strengths": strengths,

        "weaknesses": weaknesses,

        "suggestions": suggestions
    }


# ==========================================
# CREATE PDF REPORT
# ==========================================

def create_pdf_report(result):

    buffer = io.BytesIO()

    pdf = canvas.Canvas(
        buffer,
        pagesize=A4
    )

    width, height = A4

    y = height - 50


    # Title

    pdf.setFont(
        "Helvetica-Bold",
        22
    )

    pdf.drawString(
        50,
        y,
        "ResumeMatch AI"
    )

    y -= 30


    pdf.setFont(
        "Helvetica",
        12
    )

    pdf.drawString(
        50,
        y,
        "Resume Analysis Report"
    )

    y -= 40


    # Job Role

    pdf.setFont(
        "Helvetica-Bold",
        14
    )

    pdf.drawString(
        50,
        y,
        "Detected Job Role:"
    )

    pdf.setFont(
        "Helvetica",
        14
    )

    pdf.drawString(
        190,
        y,
        result["role"]
    )

    y -= 35


    # Scores

    pdf.setFont(
        "Helvetica-Bold",
        13
    )

    pdf.drawString(
        50,
        y,
        f"Overall Match Score: {result['score']}%"
    )

    y -= 25

    pdf.drawString(
        50,
        y,
        f"Skill Match: {result['skill_score']}%"
    )

    y -= 25

    pdf.drawString(
        50,
        y,
        f"Text Similarity: {result['similarity']}%"
    )

    y -= 40


    # Matched Skills

    pdf.setFont(
        "Helvetica-Bold",
        14
    )

    pdf.drawString(
        50,
        y,
        "Matched Skills"
    )

    y -= 25

    pdf.setFont(
        "Helvetica",
        11
    )

    if result["matched"]:

        for skill in result["matched"]:

            pdf.drawString(
                65,
                y,
                "• " + skill
            )

            y -= 18

    else:

        pdf.drawString(
            65,
            y,
            "No matched skills found."
        )

        y -= 18


    y -= 15


    # Missing Skills

    pdf.setFont(
        "Helvetica-Bold",
        14
    )

    pdf.drawString(
        50,
        y,
        "Missing Skills"
    )

    y -= 25

    pdf.setFont(
        "Helvetica",
        11
    )

    if result["missing"]:

        for skill in result["missing"]:

            pdf.drawString(
                65,
                y,
                "• " + skill
            )

            y -= 18

    else:

        pdf.drawString(
            65,
            y,
            "No major missing skills found."
        )

        y -= 18


    y -= 15


    # Strengths

    pdf.setFont(
        "Helvetica-Bold",
        14
    )

    pdf.drawString(
        50,
        y,
        "Resume Strengths"
    )

    y -= 25

    pdf.setFont(
        "Helvetica",
        11
    )

    for strength in result["strengths"]:

        pdf.drawString(
            65,
            y,
            "• " + strength
        )

        y -= 18


    y -= 15


    # Weaknesses

    pdf.setFont(
        "Helvetica-Bold",
        14
    )

    pdf.drawString(
        50,
        y,
        "Resume Weaknesses"
    )

    y -= 25

    pdf.setFont(
        "Helvetica",
        11
    )

    for weakness in result["weaknesses"]:

        pdf.drawString(
            65,
            y,
            "• " + weakness
        )

        y -= 18


    y -= 15


    # Recommendations

    pdf.setFont(
        "Helvetica-Bold",
        14
    )

    pdf.drawString(
        50,
        y,
        "Recommendations"
    )

    y -= 25

    pdf.setFont(
        "Helvetica",
        11
    )

    for suggestion in result["suggestions"]:

        # Create a simple new page if needed

        if y < 60:

            pdf.showPage()

            y = height - 50

            pdf.setFont(
                "Helvetica",
                11
            )


        pdf.drawString(
            65,
            y,
            "• " + suggestion
        )

        y -= 18


    pdf.save()

    buffer.seek(0)

    return buffer


# ==========================================
# HOME PAGE
# ==========================================

@app.route(
    "/",
    methods=["GET", "POST"]
)

def home():

    result = None


    if request.method == "POST":

        resume = request.files.get(
            "resume"
        )

        job_description = request.form.get(
            "job_description"
        )


        if resume and job_description:

            resume_text = extract_text_from_pdf(
                resume
            )

            result = analyze_resume(
                resume_text,
                job_description
            )


    return render_template(
        "index.html",
        result=result
    )


# ==========================================
# DOWNLOAD REPORT
# ==========================================

@app.route(
    "/download-report",
    methods=["POST"]
)

def download_report():

    result = {

        "role": request.form.get(
            "role",
            "General / Other"
        ),

        "score": request.form.get(
            "score",
            "0"
        ),

        "skill_score": request.form.get(
            "skill_score",
            "0"
        ),

        "similarity": request.form.get(
            "similarity",
            "0"
        ),

        "matched": request.form.getlist(
            "matched"
        ),

        "missing": request.form.getlist(
            "missing"
        ),

        "strengths": request.form.getlist(
            "strengths"
        ),

        "weaknesses": request.form.getlist(
            "weaknesses"
        ),

        "suggestions": request.form.getlist(
            "suggestions"
        )
    }


    pdf_file = create_pdf_report(
        result
    )


    return send_file(
        pdf_file,
        as_attachment=True,
        download_name="ResumeMatch_AI_Report.pdf",
        mimetype="application/pdf"
    )


# ==========================================
# RUN APPLICATION
# ==========================================

if __name__ == "__main__":

    app.run(
        debug=True
    )