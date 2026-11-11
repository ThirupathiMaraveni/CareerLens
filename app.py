import re
import streamlit as st
from matcher import analyze_match, extract_text_from_pdf

st.set_page_config(page_title="JobMatch AI", page_icon="🎯", layout="wide")

st.title("🎯 JobMatch AI")
st.caption("A simple NLP tool that compares your skills with an internship or job description.")

with st.sidebar:
    st.header("How it works")
    st.write("1. Add your resume as a PDF or paste its text.")
    st.write("2. Paste an internship/job description.")
    st.write("3. See matching skills and skills to learn.")
    st.info("This is a learning/portfolio tool, not a hiring decision system. Its score is a text-similarity estimate, not a probability of getting hired.")

left, right = st.columns(2)
with left:
    st.subheader("Your resume")
    uploaded = st.file_uploader("Upload a text-based PDF (optional)", type=["pdf"])
    resume_text = st.text_area("Or paste resume text", height=260, placeholder="Example: I know Python, SQL, Pandas, NumPy and basic machine learning...")
    if uploaded is not None:
        try:
            resume_text = extract_text_from_pdf(uploaded)
            st.success("PDF text extracted. You can still edit the text below.")
            resume_text = st.text_area("Extracted resume text", value=resume_text, height=260)
        except Exception as exc:
            st.error(f"Could not read this PDF: {exc}")

with right:
    st.subheader("Internship / job description")
    job_text = st.text_area("Paste the role description", height=260, placeholder="Example: We are looking for a Python intern with SQL, data analysis, Pandas, machine learning and communication skills...")

if st.button("Analyze my match", type="primary", use_container_width=True):
    if not resume_text.strip() or not job_text.strip():
        st.warning("Please provide both resume text and a job description.")
    else:
        result = analyze_match(resume_text, job_text)
        st.divider()
        st.subheader("Your match report")
        score_col, matched_col, missing_col = st.columns(3)
        score_col.metric("Text similarity", f"{result['similarity']:.1f}%")
        matched_col.metric("Matched skills", len(result["matched_skills"]))
        missing_col.metric("Skills to work on", len(result["missing_skills"]))

        st.progress(min(max(result["similarity"] / 100, 0.0), 1.0))
        a, b = st.columns(2)
        with a:
            st.markdown("#### ✅ Skills found in both")
            if result["matched_skills"]:
                st.write(", ".join(result["matched_skills"]))
            else:
                st.write("No skills from the built-in skill list were detected in both texts.")
        with b:
            st.markdown("#### 📚 Skills mentioned in the role but not your resume")
            if result["missing_skills"]:
                st.write(", ".join(result["missing_skills"]))
            else:
                st.write("No missing skills detected from the built-in list.")

        st.markdown("#### 💡 Suggested next steps")
        if result["missing_skills"]:
            for skill in result["missing_skills"][:5]:
                st.write(f"- Learn or practise **{skill}**, then add it to your resume only when you can demonstrate it.")
        else:
            st.write("- Review the role description and tailor your project examples to its requirements.")

        st.caption("Note: Keyword detection uses a small editable skill list. Similarity depends on wording and does not judge experience, project quality, or communication skills.")
