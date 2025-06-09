import openai
from app.config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def generate_cover_letter(jd_text, resume_text, job_title):
    prompt = f"""
You are a professional career assistant. Using the following resume and job description,
write a personalized, formal cover letter for the role of {job_title}. Emphasize relevance 
and alignment between experience and job needs.

Resume:
{resume_text}

Job Description:
{jd_text}

Cover Letter:
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",  # or gpt-3.5-turbo if cost is a concern
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7  # Controls creativity
    )

    return response['choices'][0]['message']['content']
