from flask import Flask, request, render_template_string
from matcher import analyze_match
from pypdf import PdfReader
from io import BytesIO

app = Flask(__name__)

PAGE = """
<!DOCTYPE html>
<html>
<head>
<title>CareerLens - Career Match Assistant</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
* { box-sizing: border-box; }
body {
    margin: 0;
    font-family: Arial, sans-serif;
    background: #10131f;
    color: white;
}
header {
    padding: 28px 8%;
    background: #191e30;
    border-bottom: 1px solid #30374d;
}
header h1 { color: #ff7795; margin: 0; }
header p { color: #aab2c5; }
main { max-width: 1100px; margin: 35px auto; padding: 20px; }
.columns {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 22px;
}
.panel {
    background: #1b2133;
    padding: 22px;
    border-radius: 14px;
    border: 1px solid #30374d;
}
textarea {
    width: 100%;
    height: 210px;
    padding: 14px;
    margin-top: 12px;
    border-radius: 9px;
    background: #282f43;
    color: white;
    border: 1px solid #414a61;
    resize: vertical;
}
input[type=file] { margin: 12px 0; }
button {
    width: 100%;
    padding: 15px;
    margin-top: 22px;
    border: none;
    border-radius: 9px;
    background: #ff7795;
    color: #171421;
    font-weight: bold;
    cursor: pointer;
}
.result {
    margin-top: 25px;
    padding: 22px;
    background: #1b2133;
    border-radius: 14px;
}
.metric { color: #ff91aa; font-size: 28px; font-weight: bold; }
li { margin: 9px 0; }
.error { color: #ff8b8b; }
footer { text-align: center; padding: 25px; color: #929bb0; }
@media(max-width:700px) {
    .columns { grid-template-columns: 1fr; }
}
</style>
</head>
<body>
<header>
<h1>🎯 CareerLens</h1>
<p>Your AI-Powered Career Match Assistant</p>
</header>
<main>
<h2>Find Your Career Match</h2>
<p>Compare your resume with an internship or job description.</p>

<form method="POST" enctype="multipart/form-data">
<div class="columns">
<div class="panel">
<h3>Your Resume</h3>
<label>Upload a text-based PDF (optional)</label>
<input type="file" name="resume_pdf" accept=".pdf">
<textarea name="resume_text"
placeholder="Paste your resume text here...">{{ resume_text }}</textarea>
</div>

<div class="panel">
<h3>Internship / Job Description</h3>
<textarea name="job_text"
placeholder="Paste the job description here...">{{ job_text }}</textarea>
</div>
</div>
<button type="submit">Analyze My Match →</button>
</form>

{% if error %}
<p class="error">{{ error }}</p>
{% endif %}

{% if result %}
<div class="result">
<h2>Your Match Report</h2>
<p>Text Similarity</p>
<div class="metric">{{ "%.1f"|format(result.similarity) }}%</div>
<p>Matched skills: <b>{{ result.matched_skills|length }}</b></p>
<p>Skills to work on: <b>{{ result.missing_skills|length }}</b></p>
<hr>
<h3>✅ Skills found in both</h3>
<ul>
{% for skill in result.matched_skills %}
<li>{{ skill }}</li>
{% else %}
<li>No common skills detected.</li>
{% endfor %}
</ul>
<h3>📚 Skills to improve</h3>
<ul>
{% for skill in result.missing_skills %}
<li>{{ skill }}</li>
{% else %}
<li>No missing skills detected.</li>
{% endfor %}
</ul>
<p>Note: Similarity is a text-matching estimate, not a probability of getting hired.</p>
</div>
{% endif %}
</main>
<footer>© 2026 CareerLens | Your Career Match Assistant</footer>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    error = ""
    resume_text = ""
    job_text = ""

    if request.method == "POST":
        resume_text = request.form.get("resume_text", "").strip()
        job_text = request.form.get("job_text", "").strip()

        uploaded = request.files.get("resume_pdf")

        if uploaded and uploaded.filename.lower().endswith(".pdf"):
            try:
                reader = PdfReader(BytesIO(uploaded.read()))
                extracted = "\n".join(
                    page.extract_text() or ""
                    for page in reader.pages
                )
                if not extracted.strip():
                    raise ValueError("PDF contains no selectable text.")
                if not resume_text:
                    resume_text = extracted
            except Exception as exc:
                error = f"Could not read PDF: {exc}"

        if not error:
            try:
                result = analyze_match(resume_text, job_text)
            except ValueError as exc:
                error = str(exc)
            except Exception:
                error = "Unable to analyze the documents. Please check your text."

    return render_template_string(
        PAGE,
        result=result,
        error=error,
        resume_text=resume_text,
        job_text=job_text
    )