import streamlit as st
from google.generativeai import configure, GenerativeModel
from prompts import SCORING_PROMPT
from dotenv import load_dotenv
import re

# Load Gemini API

configure(api_key=st.secrets["GEMINI_API_KEY"])

model = GenerativeModel("gemini-2.5-flash")

# Set Page
st.set_page_config(page_title="FakeOut - AI Job Checker", page_icon="🧠")
st.title("🧠 FakeOut")
st.caption("AI-powered job posting checker to help you stay scam-free.")

# Input
st.subheader("📥 Job Description")
job_text = st.text_area("Paste a job description here 👇", height=250)

uploaded_file = st.file_uploader("Or upload a `.txt` job description", type=["txt"])
if uploaded_file:
    job_text = uploaded_file.read().decode("utf-8")

# Utility: Extract score from LLM text
def extract_score(text):
    match = re.search(r'(?i)confidence\s*[:=]?\s*(\d\.\d+)', text)
    if match:
        return float(match.group(1))
    return None

# Analyze Button
if st.button("🔍 Analyze Job"):
    if job_text:
        with st.spinner("Analyzing with Gemini AI... please wait."):
            prompt = SCORING_PROMPT.format(job=job_text)
            response = model.generate_content(prompt)
            analysis = response.text.strip()
            score = extract_score(analysis)

        # Output
        st.success("✅ Analysis Complete!")

        st.subheader("🧠 Gemini's Analysis")
        st.markdown(analysis)

        # Highlight score + verdict
        if score is not None:
            st.subheader("📊 Confidence Score")
            st.metric("Confidence (0.00 to 1.00)", f"{score}")

            st.subheader("✅ Should You Apply?")
            if score > 0.85:
                st.success("✔️ This job appears genuine. You may apply with standard caution.")
            elif score > 0.6:
                st.warning("⚠️ This job might be risky. Please verify details before applying.")
            else:
                st.error("❌ This job looks suspicious. Avoid or research it thoroughly.")
        else:
            st.info("⚠️ Couldn't extract a score. Please interpret Gemini's full analysis above.")

        # Disclaimer
        st.caption("🧠 *This is an AI-generated prediction. Always verify important job offers yourself.*")
    else:
        st.error("Please provide a job description by pasting or uploading.")
