import re

def tokenize(text):
    """Tokenize and normalize text"""
    text = text.lower()  # Convert to lowercase
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    tokens = text.split()  # Split into words
    return tokens


def highlight_query_terms(text, query_tokens):
    """Highlight query terms in results"""
    for token in query_tokens:
        text = re.sub(f"\\b{token}\\b", f"**{token}**", text, flags=re.IGNORECASE)
    return text 