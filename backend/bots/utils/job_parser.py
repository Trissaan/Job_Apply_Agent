from bots.utils.claude_client import claude_ask

def extract_job_details_ai(page):
    # Extract all visible text from the page (grouped)
    all_elements = page.locator("body *:visible")
    content_blocks = []

    for i in range(min(100, all_elements.count())):  # limit for speed
        try:
            text = all_elements.nth(i).text_content().strip()
            if text and len(text) > 30:  # skip empty or tiny text
                content_blocks.append(text)
        except Exception:
            continue

    all_text = "\n\n".join(content_blocks)

    prompt = f"""
You are helping extract job information from a job posting webpage.

Below is all the visible content from the job page:

{all_text}

From this, identify and extract only the **Job Title** and **Job Description**.
Respond in the following JSON format:

{{
  "job_title": "...",
  "job_description": "..."
}}
"""

    response = claude_ask(prompt)

    try:
        parsed = eval(response) if isinstance(response, str) else response
        job_title = parsed.get("job_title", "Job Title")
        job_description = parsed.get("job_description", "")
        return job_title.strip(), job_description.strip()
    except Exception as e:
        print(f"❌ Failed to parse Claude JD response: {e}")
        return "Job Title", ""
