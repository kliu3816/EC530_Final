import streamlit as st
import requests
import json

# URL of your FastAPI quiz-generation endpoint
API_URL = "http://127.0.0.1:8000/upload-pdf/"

# Utility to reset session state
def reset_state():
    for key in ["quiz", "answers", "submitted", "num_questions"]:
        if key in st.session_state:
            del st.session_state[key]

# Page configuration
st.set_page_config(page_title="PDF to Quiz", layout="centered")
st.title("📄 ➡️ 📝 PDF → Quiz Generator")

# Initialize session state defaults
st.session_state.setdefault("quiz", None)
st.session_state.setdefault("answers", {})
st.session_state.setdefault("submitted", False)

# If no quiz yet, show upload form
if st.session_state.quiz is None:
    with st.form("generate_form"):
        num_questions = st.number_input(
            "Number of questions to generate", min_value=1, max_value=20, value=5, step=1
        )
        pdf_file = st.file_uploader("Upload a PDF", type=["pdf"] )
        generate = st.form_submit_button("Generate Quiz")

    if generate and pdf_file:
        st.session_state.num_questions = num_questions
        with st.spinner("Generating quiz..."):
            try:
                files = {"file": (pdf_file.name, pdf_file, "application/pdf")}
                data = {"num_questions": st.session_state.num_questions}
                response = requests.post(API_URL, files=files, data=data)
                response.raise_for_status()
                st.session_state.quiz = json.loads(response.json().get("quiz", "[]"))
                st.session_state.submitted = False
                st.session_state.answers = {}
                # Initialize checkbox states
                for idx, q in enumerate(st.session_state.quiz):
                    opts = q.get('options', [])
                    for opt_idx in range(len(opts)):
                        st.session_state.setdefault(f"q_{idx}_{opt_idx}", False)
            except Exception as e:
                st.error(f"Error generating quiz: {e}")

# If quiz exists, display questions with checkboxes
else:
    quiz = st.session_state.quiz
    st.header("📝 Your Quiz")

    # Display each question
    for idx, q in enumerate(quiz):
        st.subheader(f"Question {idx+1}: {q['question']}")
        options = q.get('options', [])
        # Ensure answer slot exists
        st.session_state.answers.setdefault(idx, None)

        for opt_idx, opt in enumerate(options):
            key = f"q_{idx}_{opt_idx}"
            # Capture local variables in callback
            def make_callback(i=idx, oi=opt_idx, opts=options, my_key=key):
                def cb():
                    # Uncheck all other options
                    for j in range(len(opts)):
                        st.session_state[f"q_{i}_{j}"] = False
                    # Check this option
                    st.session_state[my_key] = True
                    # Record the answer
                    st.session_state.answers[i] = opts[oi]
                return cb

            # Render checkbox
            st.checkbox(opt, key=key, on_change=make_callback())

    # Submit answers or show feedback
    if not st.session_state.submitted:
        if st.button("Submit Answers"):
            unanswered = [i for i, ans in st.session_state.answers.items() if ans is None]
            if unanswered:
                st.warning(f"Please answer all questions: {', '.join(str(i+1) for i in unanswered)}")
            else:
                st.session_state.submitted = True
    else:
        # Calculate score
        score = sum(
            1 for i, q in enumerate(quiz)
            if st.session_state.answers.get(i) == q.get('answer')
        )
        st.success(f"Your score: {score} / {len(quiz)}")

        # Detailed feedback
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

        if st.button("Try Another PDF"):
            reset_state()

# Footer
st.markdown("---")
st.caption("Built with Streamlit + FastAPI + OpenAI GPT")
