import os
import requests
import json
import hashlib
import tldextract
from newspaper import Article

# --- CONFIG ---
SERPAPI_KEY = os.getenv("SERPAPI_KEY")   # put your key in .env or set directly

# --- HELPER: create stable ID from URL ---
def make_id(url):
    return hashlib.md5(url.encode()).hexdigest()[:10]

# --- SEARCH (using SerpAPI) ---
def search_articles(query, num=5):
    url = "https://serpapi.com/search.json"
    params = {"q": query, "num": num, "api_key": SERPAPI_KEY, "engine":"google"}
    r = requests.get(url, params=params, timeout=15)
    r.raise_for_status()
    data = r.json()

    results = []
    for item in data.get("organic_results", [])[:num]:
        link = item.get("link") or item.get("url")
        if not link: 
            continue
        results.append({
            "title": item.get("title"),
            "url": link,
            "snippet": item.get("snippet"),
            "source": tldextract.extract(link).registered_domain
        })
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
            "end_char": min(end, len(text))
        })
        start = end
    return chunks

# --- MAIN FUNCTION ---
def get_articles(query, num_results=5):
    search_results = search_articles(query, num=num_results)
    articles = []

    for res in search_results:
        data = fetch_article(res["url"])
        if "error" in data: 
            continue

        aid = make_id(res["url"])
        chunks = chunk_text(data["text"], max_len=800)

        article_obj = {
            "article_id": aid,
            "url": res["url"],
            "title": data["title"] or res["title"],
            "source": res["source"],
            "published": data["published"],
            "authors": data.get("authors", []),
            "snippet": res.get("snippet", ""),
            "text": data["text"],
            "chunks": chunks
        }
        articles.append(article_obj)

    return articles


# --- RUN EXAMPLE ---
if __name__ == "__main__":
    results = get_articles("Quantum computing breakthroughs 2025", num_results=3)
    print(json.dumps(results, indent=2))
