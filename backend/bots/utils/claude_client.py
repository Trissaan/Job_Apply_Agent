import anthropic
import os
from dotenv import load_dotenv

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
