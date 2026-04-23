import re

def sanitize_input(prompt: str):
    """
    Cleans and validates user input
    """

    # Strip HTML tags
    clean_prompt = re.sub(r'<.*?>', '', prompt)

    # Basic prompt injection detection
    suspicious_patterns = [
        "ignore previous instructions",
        "disregard above",
        "act as",
        "system prompt",
        "reveal secrets",
        "bypass"
    ]

    for pattern in suspicious_patterns:
        if pattern.lower() in clean_prompt.lower():
            return None, "Potential prompt injection detected"

    return clean_prompt, None