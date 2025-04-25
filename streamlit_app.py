import streamlit as st
import requests
import json

# URL of your FastAPI quiz-generation endpoint
API_URL = "http://127.0.0.1:8000/upload-pdf/"
# Utility to reset session state
def reset_state():
    for key in ["quiz", "answers", "submitted"]:
        if key in st.session_state:
            del st.session_state[key]

# Main application
st.set_page_config(page_title="PDF to Quiz", layout="centered")
st.title("📄 ➡️ 📝 PDF → Quiz Generator")

# Initialize session state
if "quiz" not in st.session_state:
    st.session_state.quiz = None

if st.session_state.quiz is None:
    # Step 1: File upload
    pdf_file = st.file_uploader("Upload a PDF", type=["pdf"] )
    if pdf_file:
        with st.spinner("Generating quiz..."):
            try:
                files = {"file": (pdf_file.name, pdf_file, "application/pdf")}
                response = requests.post(API_URL, files=files)
                response.raise_for_status()
                data = response.json()
                # Parse the quiz JSON
                st.session_state.quiz = json.loads(data.get("quiz", "[]"))
                st.session_state.submitted = False
                st.session_state.answers = {}
            except Exception as e:
                st.error(f"Error generating quiz: {e}")

else:
    quiz = st.session_state.quiz
    st.header("📝 Your Quiz")
    # Display each question with radio inputs
    for idx, q in enumerate(quiz):
        st.subheader(f"Question {idx+1}: {q['question']}")
        choice = st.radio(label="", options=q.get('options', []), key=f"q_{idx}")
        st.session_state.answers[idx] = choice

    # Submit or show score
    if not st.session_state.submitted:
        if st.button("Submit Answers"):
            st.session_state.submitted = True
    else:
        # Calculate score
        score = sum(
            1 for i, q in enumerate(quiz)
            if st.session_state.answers.get(i) == q.get('answer')
        )
        st.success(f"Your score: {score} / {len(quiz)}")
        if st.button("Try Another PDF"):
            reset_state()

# Footer
st.markdown("---")
st.caption("Built with Streamlit + FastAPI + OpenAI GPT")
