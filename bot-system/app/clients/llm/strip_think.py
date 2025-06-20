import re

def strip_think_tags(text: str) -> str:
    """
    Remove all <think>...</think> tags and their content from the given text.
    """
    return re.sub(r'<think>[\s\S]*?</think>', '', text, flags=re.IGNORECASE).strip()
