import anthropic
import os
from reportlab.lib.pagesizes import LETTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.units import inch

# Claude API setup
#CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY", "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")
claude = anthropic.Anthropic(api_key=os.getenv("CLAUDE_API_KEY", "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"))

def tailor_resume_with_claude(base_resume_text: str, job_description: str) -> str:
    prompt = f"""
You are an expert resume writer.

Here is a base resume:
---
{base_resume_text}
---

Here is a job description:
---
{job_description}
---

💡 Your task: Rewrite the resume to tailor it for this job. Maintain structure, make it ATS-friendly, and emphasize skills/achievements relevant to the job description.

Return only the full tailored resume, no explanation.
"""
    response = claude.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=3000,
        temperature=0.5,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.content[0].text.strip()

def generate_cover_letter_with_claude(base_resume_text: str, job_description: str, company: str) -> str:
    prompt = f"""
You are an expert cover letter writer.

Here is the applicant's resume:
---
{base_resume_text}
---

Here is the job description:
---
{job_description}
---

💡 Your task: Write a professional, concise (max 250 words) cover letter addressed to the hiring manager at {company}. Make it warm but direct. Include specific reasons why the applicant is a good fit based on the job description.

Return only the final letter, no preamble.
"""
    response = claude.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=800,
        temperature=0.6,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.content[0].text.strip()

def export_tailored_resume_to_pdf(tailored_text: str, output_path: str = "tailored_resume.pdf"):
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Heading', fontSize=14, leading=16, spaceAfter=10, spaceBefore=12, alignment=TA_LEFT, fontName='Helvetica-Bold'))
    styles.add(ParagraphStyle(name='Body', fontSize=11, leading=14, spaceAfter=6, alignment=TA_LEFT))
    styles.add(ParagraphStyle(name='TitleCenter', fontSize=16, leading=18, alignment=TA_CENTER, spaceAfter=12, fontName='Helvetica-Bold'))

    doc = SimpleDocTemplate(output_path, pagesize=LETTER,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=72)

    content = []

    for i, section in enumerate(tailored_text.split("\n\n")):
        section = section.strip()
        if not section:
            continue
        if i == 0:
            content.append(Paragraph(section, styles['TitleCenter']))
        elif section.isupper() or section.endswith(":"):
            content.append(Paragraph(section, styles['Heading']))
        else:
            content.append(Paragraph(section.replace("\n", "<br/>"), styles['Body']))

        content.append(Spacer(1, 0.1 * inch))

    doc.build(content)