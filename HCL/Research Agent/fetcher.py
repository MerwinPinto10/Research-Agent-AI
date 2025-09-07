# src/fetcher.py
import requests
from newspaper import Article
from bs4 import BeautifulSoup
import trafilatura
from .utils import id_from_url
HEADERS = {"User-Agent":"Mozilla/5.0 (compatible; HackathonBot/1.0)"}

def fetch_with_newspaper(url, timeout=12):
    try:
        a = Article(url, language='en')
        a.download()
        a.parse()
        return {"title": a.title, "text": a.text, "authors": a.authors or [], "published": (a.publish_date.isoformat() if a.publish_date else None)}
    except Exception as e:
        return {"error": str(e)}

def fetch_with_trafilatura(url):
    try:
        doc = trafilatura.fetch_url(url, timeout=12)
        if not doc:
            return {"error": "trafilatura fetch failed"}
        text = trafilatura.extract(doc, favor_precision=True)
        return {"title": None, "text": text, "authors": [], "published": None}
    except Exception as e:
        return {"error": str(e)}

def fallback_meta(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "lxml")
        desc = None
        meta = soup.find('meta', attrs={'property':'og:description'}) or soup.find('meta', attrs={'name':'description'})
        if meta and meta.get('content'):
            desc = meta.get('content')
        title = soup.title.string.strip() if soup.title else None
        return {"title": title, "text": desc or "", "authors": [], "published": None}
    except Exception as e:
        return {"error": str(e)}

def fetch_article(url):
    # Try newspaper -> trafilatura -> meta fallback
    res = fetch_with_newspaper(url)
    if res.get("text"):
        return res
    res2 = fetch_with_trafilatura(url)
    if res2.get("text"):
        if not res2.get("title"):
            res2["title"] = res.get("title")
        return res2
    return fallback_meta(url)
