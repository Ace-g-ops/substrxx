import re

def contains_keyword(text: str, keyword: str) -> bool:
    """Word-start boundary match: catches 'whisper'/'whispers' but not
    'car' inside 'scar'."""
    return re.search(rf"\b{re.escape(keyword)}\w*", text) is not None