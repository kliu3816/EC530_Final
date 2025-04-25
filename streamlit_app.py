import streamlit as st
import requests
import json
import os

# URL of your FastAPI quiz-generation endpoint
API_URL = "http://127.0.0.1:8000/upload-pdf/"

# Utility to reset session state
def reset_state():
    for key in ["quiz", "answers", "submitted", "num_questions"]:
        if key in st.session_state:
            del st.session_state[key]

# Main application setup
st.set_page_config(page_title="PDF to Quiz", layout="centered")
st.title("📄 ➡️ 📝 PDF → Quiz Generator")

# Let user choose number of questions
num_questions = st.number_input(
    "Number of questions to generate", min_value=1, max_value=20, value=5, step=1
)
st.session_state.num_questions = num_questions

# If quiz not yet generated
if "quiz" not in st.session_state or st.session_state.quiz is None:
    pdf_file = st.file_uploader("Upload a PDF", type=["pdf"] )
    if pdf_file:
        if st.button("Generate Quiz"):
            with st.spinner("Generating quiz..."):
                try:
                    # Send PDF and number of questions to backend
                    files = {"file": (pdf_file.name, pdf_file, "application/pdf")}
                    data = {"num_questions": st.session_state.num_questions}
                    response = requests.post(API_URL, files=files, data=data)
                    response.raise_for_status()
                    quiz = json.loads(response.json().get("quiz", "[]"))
                    st.session_state.quiz = quiz
                    st.session_state.answers = {}
                    st.session_state.submitted = False
                except Exception as e:
                    st.error(f"Error generating quiz: {e}")

# If quiz exists, display questions and collect answers
else:
    quiz = st.session_state.quiz
    st.header("📝 Your Quiz")
    for idx, q in enumerate(quiz):
        st.subheader(f"Question {idx+1}: {q['question']}")
        st.session_state.answers[idx] = st.radio(
            "", q.get('options', []), key=f"q_{idx}"
        )

    # Submit answers
    if not st.session_state.submitted:
        if st.button("Submit Answers"):
            st.session_state.submitted = True
    else:
        # Score calculation
        score = sum(
            1 for i, q in enumerate(quiz)
            if st.session_state.answers.get(i) == q.get('answer')
        )
        st.success(f"Your score: {score} / {len(quiz)}")

        # Detailed feedback for wrong answers
        st.subheader("🛠️ Feedback")
        for idx, q in enumerate(quiz):
            user_ans = st.session_state.answers.get(idx)
            correct_ans = q.get('answer')
            if user_ans != correct_ans:
                st.markdown(f"**Q{idx+1}. {q['question']}**")
                st.markdown(f"- Your answer: {user_ans}")
                st.markdown(f"- Correct answer: {correct_ans}")
                explanation = q.get('explanation', 'No explanation provided.')
                st.markdown(f"- Explanation: {explanation}")

        # Option to reset
        if st.button("Try Another PDF"):
            reset_state()

# Footer
st.markdown("---")
st.caption("Built with Streamlit + FastAPI + OpenAI GPT")
