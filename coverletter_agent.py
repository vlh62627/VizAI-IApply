import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-pro")

def generate_cover(job_post):

    prompt = f"""
Write a concise professional cover letter
for the following job post.

{job_post}

Keep it under 120 words.
"""

    response = model.generate_content(prompt)

    return response.text