import re


def clean_title(title: str) -> str:
    # Remove anything inside () or []
    cleaned = re.sub(r"[\(\[].*?[\)\]]", "", title)
    # Collapse multiple spaces and strip leading/trailing
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned
