import anthropic
import os
import json

claude = anthropic.Anthropic(api_key=os.getenv("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"))

def generate_form_plan_with_claude(html: str, job_title: str, resume_text: str) -> dict:
    """
    Uses Claude to analyze a job application form (HTML) and suggest how to fill it dynamically.
    Returns a dictionary with input selectors + values and a list of checkboxes to tick.
    """
    prompt = f"""
You are an AI assistant that fills out job application forms.

Here is the HTML of a job application page:
---
{html[:10000]}
---

The job title is: {job_title}

The applicant's name is: Trissaan Anandhanayki Shanmugasundaram  
Email: trissaan@gmail.com  
Phone: 0434549364

Here is the applicant's resume:
---
{resume_text[:3000]}
---

Based on the HTML form, the job title, and the resume, output a JSON like this:
{{
  "click_button_text": "Apply Now",
  "resume_upload_selector": "input[type='file']",
  "cover_letter_selector": "textarea[name='coverLetter']",
  "submit_button_text": "Submit",
  "inputs": {{
    "input[name='email']": "trissaan@gmail.com",
    "textarea[name='whyYou']": "I’m excited about this role because..."
  }},
  "checkboxes": [
    "input[name='terms']",
    "input[name='workAuth']"
  ]
}}

Only include visible, fillable fields. Skip hidden or irrelevant ones. Return ONLY a JSON object.
"""

    response = claude.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=800,
        temperature=0.4,
        messages=[{"role": "user", "content": prompt}]
    )

    try:
        raw_text = response.content[0].text.strip()
        return json.loads(raw_text)
    except Exception as e:
        print("⚠️ Failed to parse Claude's form response:", e)
        print("Claude raw output:\n", response.content[0].text)
        return {
            "click_button_text": "Apply",
            "resume_upload_selector": "input[type='file']",
            "cover_letter_selector": "textarea",
            "submit_button_text": "Submit",
            "inputs": {},
            "checkboxes": []
        }
