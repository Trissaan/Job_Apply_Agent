from utils.claude_client import claude_ask

def get_field_mapping_from_claude(user_info, field_list):
    prompt = f"""
You are a smart assistant helping to fill job application forms.

User info:
{user_info}

Visible form fields (index + label + type):
{field_list}

Map the field index to the correct user_info key.

Only respond with valid JSON. Example:
{{ "0": "first_name", "2": "email", "4": "linkedin" }}
"""
    response = claude_ask(prompt)
    try:
        return eval(response) if isinstance(response, str) else response
    except Exception as e:
        print(f"❌ Error parsing Claude response: {e}")
        return {}
