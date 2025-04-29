# PDF Quiz Generator

This project allows educators to upload a PDF file, automatically generate multiple-choice quiz questions based on its content using OpenAI's GPT API, and then allow users to take the quiz and receive immediate feedback. The application is split into two main parts:

- A **FastAPI** backend that processes PDFs and generates quiz questions.
- A **Streamlit** frontend that allows user interaction with the quiz system.

## Features

- Upload PDF files for processing
- Generate customizable quizzes using GPT
- Multiple-choice quiz interface in the browser
- Real-time grading with explanations for incorrect answers
- User-defined number of quiz questions
- Deployed with AWS App Runner for cloud access

---

## Technologies Used

### Backend
- Python 3.11
- FastAPI
- OpenAI API
- PyMuPDF (for PDF parsing)
- Uvicorn (for running the FastAPI server)

### Frontend
- Streamlit (Python-based UI)

### Cloud
- AWS App Runner (for backend and frontend deployment)
- AWS ECR (for container storage)
- Docker (for containerization)

---

## Local Setup Instructions

### Prerequisites

- Python 3.11
- Docker
- An OpenAI API Key
- AWS CLI (for deployment)

### 1. Clone the repository
- git clone https://github.com/yourusername/EC530_final.git
- cd EC530_final
- uvicorn app:app --reload --port 8000
- streamlit run streamlit_app.py
