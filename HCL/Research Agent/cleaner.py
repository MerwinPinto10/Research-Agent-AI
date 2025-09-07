# src/cleaner.py
import re
from .utils import id_from_url

def clean_text(text: str) -> str:
    if not text:
        return ""
    s = text.replace("\r", "\n")
    s = re.sub(r"\n{3,}", "\n\n", s)          # collapse multiple newlines
    s = re.sub(r"[ \t]{2,}", " ", s)         # collapse spaces/tabs
    s = s.strip()
    return s

def chunk_text(article_id, text, max_chars=1200, overlap=200):
    # char-based chunking (fast). Person 2 can replace with token-based if needed.
    chunks = []
    n = len(text)
    start = 0
    idx = 0
    while start < n:
        end = min(start + max_chars, n)
        snippet = text[start:end].strip()
        if not snippet:
            break
        chunk_id = f"{article_id}_c{idx}"
        chunks.append({"chunk_id": chunk_id, "text": snippet, "start_char": start, "end_char": end})
        idx += 1
        start = end - overlap
        if start < 0: start = 0
    return chunks
