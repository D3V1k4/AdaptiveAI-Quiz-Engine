from dotenv import load_dotenv
from google import genai
import os
import json

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def generate_question(subject, difficulty):

    prompt = f"""
Generate ONE {difficulty} level MCQ from {subject}.

Return ONLY valid JSON.

Example:

{{
  "question": "What is Python?",
  "options": [
    "Language",
    "Database",
    "Browser",
    "OS"
  ],
  "answer": "Language",
  "difficulty": "{difficulty}",
  "topic": "{subject}"
}}

Return valid JSON only.
No markdown.
No explanations.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt
    )

    text = response.text.strip()

    # Remove markdown if Gemini adds it
    if text.startswith("```"):
        text = text.replace("```json", "")
        text = text.replace("```", "")
        text = text.strip()

    try:
        return json.loads(text)

    except Exception:

        return {
            "question": text,
            "options": [],
            "answer": "",
            "difficulty": difficulty,
            "topic": subject
        }