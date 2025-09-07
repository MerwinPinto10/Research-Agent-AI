from typing import List, Dict

def fetch_articles(query: str, n: int = 5) -> List[Dict]:
    """
    Person1: implement real fetching here. This stub returns mock articles
    matching the API contract shape.
    """
    articles = []
    for i in range(1, n+1):
        title = f"{query.title()} example article {i}"
        url = f"https://example.com/{query.replace(' ', '_')}/{i}"
        date = f"2025-05-{i:02d}"
        source = "Nature" if i % 2 == 0 else "ArXiv"
        content = ("Full content for " + title + ". ") * 30
        snippet = content[:200]
        articles.append({
            "title": title,
            "url": url,
            "date": date,
            "source": source,
            "snippet": snippet,
            "content": content[:2000]
        })
    return articles

import requests
from datetime import datetime

def fetch_articles_real(query: str, n: int = 5):
    url = f"https://api.example.com/search?q={query}&limit={n}"
    resp = requests.get(url)
    data = resp.json()

    results = []
    for item in data["articles"]:
        results.append({
            "title": item["title"],
            "url": item["url"],
            "date": datetime.now().strftime("%Y-%m-%d"),  # or parse real date
            "source": item.get("source", "Unknown"),
            "snippet": item["content"][:200],
            "content": item["content"][:2000],
        })
    return results

def fetch_articles(query: str, n: int = 5, use_mock: bool = True) -> List[Dict]:
    if use_mock:
        return fetch_articles(query, n)
    else:
        return fetch_articles_real(query, n)
