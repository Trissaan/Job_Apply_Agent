from bots.utils.claude_client import claude_ask
import json
import re
from html import unescape

def strip_html_tags(html_text):
    text = re.sub(r"<[^>]+>", "", html_text)
    return unescape(text.strip())

def extract_job_details_ai(page):
    # Grab visible text blocks
    all_elements = page.locator("body *:visible")
    content_blocks = []

    for i in range(min(100, all_elements.count())):
        try:
            text = all_elements.nth(i).text_content().strip()
            if text and len(text) > 30:
                content_blocks.append(text)
        except:
            continue

    full_text = "\n\n".join(content_blocks)

    prompt = f"""
You're analyzing a job application page.

Extract the following from the provided visible text content:
1. Job title
2. Company name
3. A plain text version of the job description (no HTML)
4. Up to 5 relevant tags (e.g., "remote", "azure", "contract")

⚠️ Output must be **valid JSON only**. Do not include any markdown, explanation, or commentary.

Example format:
{{
  "job_title": "...",
  "company": "...",
  "job_description": "...",
  "tags": ["...", "..."]
}}

Here is the page content:
{full_text}
"""

    try:
        response = claude_ask(prompt).strip()
        print("🧠 Claude raw response:", response)

        parsed = json.loads(response)

        jd_raw = parsed.get("job_description", "")
        job_description = strip_html_tags(jd_raw)

        return (
            parsed.get("job_title", "Job Title").strip(),
            parsed.get("company", "Unknown Company").strip(),
            job_description,
            parsed.get("tags", [])
        )
    except Exception as e:
        print(f"❌ Claude failed to extract structured job details: {e}")
        return "Job Title", "Unknown Company", "", []
