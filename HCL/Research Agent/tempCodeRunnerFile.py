
    return results

# --- FETCH & CLEAN ARTICLE ---
def fetch_article(url):
    try:
        art = Article(url, language='en')
        art.download()
        art.parse()
        return {
            "title": art.title,
            "authors": art.authors,
            "published": art.publish_date.isoformat() if art.publish_date else None,
            "text": art.text
        }
    except Exception as e:
        return {"error": str(e)}

# --- CHUNKING FUNCTION ---
def chunk_text(text, max_len=500):
    chunks = []
    start = 0
    while start < len(text):
        end = start + max_len
        chunks.append({
            "chunk_id": f"{start}_{end}",
            "text": text[start:end],
            "start_char": start,