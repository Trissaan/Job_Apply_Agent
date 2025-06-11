import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

def get_best_apply_button(button_texts: list[str]) -> str:
    prompt = f"""
You are an AI agent helping a job application bot. Given a list of button texts on a job page, pick the **exact button text** the bot should click to apply directly using resume or email, avoiding logins via Seek, LinkedIn, or others.

Buttons:
{button_texts}

Respond with the **exact button text only**. Do not add explanations or punctuation. Just return the label exactly as shown.
"""

    response = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=100,
        temperature=0,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text.strip().strip('"')
