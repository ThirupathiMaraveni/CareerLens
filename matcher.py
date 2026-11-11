import re
from io import BytesIO
from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Extend this list as you learn more technologies.
SKILLS = [
    "python", "java", "c++", "c", "sql", "html", "css", "javascript",
    "flask", "django", "streamlit", "react", "git", "github",
    "machine learning", "deep learning", "artificial intelligence",
    "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch",
    "data analysis", "data visualization", "excel", "power bi",
    "tableau", "nlp", "computer vision", "statistics", "matplotlib",
    "problem solving", "communication", "rest api", "mongodb", "sqlite"
]

def normalize(text: str) -> str:
    """Normalize whitespace while preserving useful technical punctuation."""
    return re.sub(r"\s+", " ", text.lower()).strip()

def find_skills(text: str) -> set[str]:
    """Return known skills found as whole phrases in the supplied text."""
    normalized = normalize(text)
    found = set()
    for skill in SKILLS:
        pattern = r"(?<![a-z0-9])" + re.escape(skill) + r"(?![a-z0-9])"
        if re.search(pattern, normalized):
            found.add(skill)
    return found

def similarity_score(resume_text: str, job_text: str) -> float:
    """Calculate TF-IDF cosine similarity between two text documents."""
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    matrix = vectorizer.fit_transform([resume_text, job_text])
    return float(cosine_similarity(matrix[0:1], matrix[1:2])[0][0] * 100)

def analyze_match(resume_text: str, job_text: str) -> dict:
    if not resume_text.strip() or not job_text.strip():
        raise ValueError("Both resume text and job description are required.")

    resume_skills = find_skills(resume_text)
    job_skills = find_skills(job_text)
    return {
        "similarity": similarity_score(resume_text, job_text),
        "resume_skills": sorted(resume_skills),
        "job_skills": sorted(job_skills),
        "matched_skills": sorted(resume_skills & job_skills),
        "missing_skills": sorted(job_skills - resume_skills),
    }

def extract_text_from_pdf(uploaded_file) -> str:
    """Extract text from a text-based PDF uploaded through Streamlit."""
    reader = PdfReader(BytesIO(uploaded_file.getvalue()))
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    if not text.strip():
        raise ValueError("No selectable text found. Try pasting your resume text instead.")
    return text
