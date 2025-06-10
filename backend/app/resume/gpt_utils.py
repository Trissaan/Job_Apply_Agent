import os
import anthropic
from app.config import ANTHROPIC_API_KEY

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

def generate_cover_letter(jd_text, resume_text, job_title):
    prompt = f"""
Human: You are a professional career assistant. Using the following resume and job description,
write a personalized, formal cover letter for the role of {job_title}. Emphasize relevance 
and alignment between experience and job needs.

Resume:
{resume_text}

Job Description:
{jd_text}

Assistant:"""

    response = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=1024,
        temperature=0.7,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.content[0].text