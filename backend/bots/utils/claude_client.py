import anthropic
import os
from dotenv import load_dotenv
import json 

load_dotenv()

client = anthropic.Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

def claude_ask(prompt: str, model: str = "claude-3-haiku-20240307", temperature: float = 0.2) -> str:
    """
    General-purpose Claude query function.
    Returns plain text response from the model.
    """
    response = client.messages.create(
        model=model,
        max_tokens=1000,
        temperature=temperature,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.content[0].text.strip()


def get_best_apply_button(button_texts: list[str]) -> str:
    """
    Given a list of visible button texts, ask Claude which one
    should be clicked to apply directly with resume/email.
    """
    prompt = f"""
You are an AI agent helping a job application bot. Given a list of button texts on a job page, pick the **exact button text** the bot should click to apply directly using resume or email, avoiding logins via Seek, LinkedIn, or others.

Buttons:
{button_texts}

Respond with the **exact button text only**. Do not add explanations or punctuation. Just return the label exactly as shown.
"""
    return claude_ask(prompt, temperature=0).strip('"')


def get_best_resume_upload_target(possible_targets):
    prompt = f"""
You're helping identify a resume upload element from a job application webpage.

Here are possible visible HTML elements. Each contains:
- index (its position)
- tag name (e.g. 'div', 'span', 'button')
- text content
- aria-label (if present)
- CSS classes

Choose the most likely element that opens or triggers a resume upload input.

⚠️ Respond with **ONLY** the index number, like: `"3"`  
If none clearly match, respond with `"none"` and nothing else.

Elements:
{json.dumps(possible_targets, indent=2)}
"""
    try:
        response = claude_ask(prompt).strip()
        print(f"🤖 Claude fallback upload suggestion: {response}")
        return response
    except Exception as e:
        print(f"❌ Claude failed to pick upload element: {e}")
        return "none"

def extract_tags_from_jd(job_description: str) -> list[str]:
    prompt = f"""
You are helping tag job descriptions for a job application bot. From the following job description, extract 3–5 relevant tags that can help classify or filter jobs.

Tags can include:
- Level (e.g., junior, senior)
- Location (e.g., remote, hybrid, on-site)
- Contract type (e.g., contract, full-time)
- Skills or tools (e.g., python, aws, sql, power bi)

Return the tags in a simple comma-separated list. No explanations.

JOB DESCRIPTION:
{job_description}
"""

    try:
        response = claude_ask(prompt)
        return [tag.strip().lower() for tag in response.split(",") if tag.strip()]
    except Exception as e:
        print("❌ Claude failed to extract tags:", e)
        return []
