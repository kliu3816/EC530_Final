import openai
import os
import json
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env", override=True) 
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key


def generate_quiz(text: str, num_questions: int = 5):
    prompt = f"""
Based on the following text, generate {num_questions} multiple-choice questions. 
For each question, provide exactly 4 options, mark the correct one, and include a brief "explanation" explaining why that answer is correct.

Format your output as valid JSON, for example:
[
  {{
    "question": "What is …?",
    "options": ["A", "B", "C", "D"],
    "answer": "B",
    "explanation": "Because …"
  }},
  …
]

Text:
\"\"\"
{text[:4000]}
\"\"\"
"""
    resp = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    # Parse the JSON string into Python
    return json.loads(resp.choices[0].message.content)