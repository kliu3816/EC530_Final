import openai
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env", override=True) 
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key


def generate_quiz(text, num_questions=5):
    prompt = f"""
    Based on the following text, generate {num_questions} multiple-choice questions. 
    Provide 4 options per question and mark the correct one.

    Text:
    {text[:4000]}  # limit to avoid token overrun

    Format the response as JSON like this:
    [
      {{
        "question": "What is...",
        "options": ["A", "B", "C", "D"],
        "answer": "A"
      }}
    ]
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )

    return response.choices[0].message.content
