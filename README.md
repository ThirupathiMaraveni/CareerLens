# JobMatch AI — Resume & Internship Skill Matcher

A beginner-friendly NLP portfolio project that compares resume text with an internship/job description. It estimates text similarity, identifies skills appearing in both texts, and highlights role skills not detected in the resume.

## Features
- Paste resume text or upload a text-based PDF
- Paste an internship/job description
- TF-IDF + cosine similarity score
- Skill overlap and missing-skill report
- Suggestions for skills to practise
- Unit tests for the core matching logic

## Tech stack
- Python
- Streamlit
- scikit-learn (TF-IDF and cosine similarity)
- pypdf
- unittest

## Run locally

```bash
# 1. Clone the repository
git clone https://github.com/YOUR-USERNAME/jobmatch-ai.git
cd jobmatch-ai

# 2. Create and activate a virtual environment
python -m venv .venv

# Windows PowerShell:
.venv\\Scripts\\Activate.ps1

# macOS/Linux:
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

Streamlit will show a local URL, usually http://localhost:8501.

## Run tests

```bash
python -m unittest discover -s tests -v
```

## How it works
1. TF-IDF converts each document into weighted word features.
2. Cosine similarity compares the two document vectors.
3. A small editable skill dictionary detects known technical and professional skills.
4. Set operations identify matched skills and skills mentioned in the role but not detected in the resume.

## Limitations
- The similarity score is a text similarity estimate, not a hiring probability or a measure of candidate quality.
- Skill detection is dictionary-based. It can miss synonyms, context, and skills not included in `SKILLS` in `matcher.py`.
- PDF extraction works best with selectable text; scanned image PDFs need OCR, which is not included.
- Resume text is processed locally by this app; do not upload private documents to a public demo unless you understand the hosting provider's privacy settings.

## Ideas for version 2
- Add synonym mapping and a larger curated skill taxonomy
- Export the report as PDF
- Add role-specific skill categories
- Deploy the app and add screenshots to the README

## Portfolio description
Built a resume-to-job-description matching application using Python, Streamlit, TF-IDF, and cosine similarity. Implemented skill extraction, matched/missing skill analysis, PDF text extraction, and unit tests.
