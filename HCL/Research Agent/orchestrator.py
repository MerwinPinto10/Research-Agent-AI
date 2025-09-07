# src/orchestrator.py
from .searcher import get_search_results
from .fetcher import fetch_article
from .cleaner import clean_text, chunk_text
from .utils import id_from_url, now_iso
from .cache import save_cache, load_cache

def build_article_obj(url, title_hint=None, snippet_hint=None):
    fetched = fetch_article(url)
    title = fetched.get("title") or title_hint or ""
    text  = clean_text(fetched.get("text") or "")
    if len(text) < 200:
        # skip tiny extracts if they have no substance
        return None
    article_id = id_from_url(url)
    chunks = chunk_text(article_id, text)
    return {
        "article_id": article_id,
        "url": url,
        "title": title,
        "source": url.split("/")[2] if url else None,
        "published": fetched.get("published"),
        "authors": fetched.get("authors", []),
        "snippet": snippet_hint or (text[:240] + ("..." if len(text)>240 else "")),
        "text": text,
        "chunks": chunks,
        "fetched_at": now_iso()
    }

def get_articles(query, num=5, use_cache=True):
    # Check cache
    if use_cache:
        cached = load_cache(query)
        if cached:
            return cached

    results = get_search_results(query, num=num)
    articles = []
    for r in results:
        url = r.get("link") or r.get("url")
        if not url:
            continue
        art = build_article_obj(url, title_hint=r.get("title"), snippet_hint=r.get("snippet"))
        if art:
            articles.append(art)

    # Save cache for demo fallback
    save_cache(query, articles)
    return articles
