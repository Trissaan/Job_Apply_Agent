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
def tailor_resume_with_claude(base_resume: str, jd_text: str, job_title: str) -> str:
    prompt = f"""
Human: You are an expert resume editor. Given the base resume and job description, tailor the resume
to highlight the most relevant skills, experience, and keywords for the role of {job_title}.
Make sure to:

- Customize the summary/profile section if present
- Reorder and reword bullet points to match the job description
- Highlight keywords, tools, and accomplishments relevant to the JD
- Keep the resume concise, professional, and ATS-friendly
- Maintain the format (don't remove section headers like Education, Experience, etc.)

Base Resume:
{base_resume}

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
