# src/searcher.py
import os, requests, tldextract
SERPAPI_KEY = os.getenv("SERPAPI_KEY")
BING_KEY   = os.getenv("BING_KEY")

def search_serpapi(query, num=5):
    url = "https://serpapi.com/search.json"
    params = {"q": query, "num": num, "api_key": SERPAPI_KEY, "engine":"google"}
    r = requests.get(url, params=params, timeout=12)
    r.raise_for_status()
    data = r.json()
    out = []
    for item in data.get("organic_results", [])[:num]:
        link = item.get("link") or item.get("url")
        out.append({"title": item.get("title"), "link": link, "snippet": item.get("snippet"),
                    "source": tldextract.extract(link).registered_domain if link else None})
    return out

def search_bing(query, num=5):
    headers = {"Ocp-Apim-Subscription-Key": BING_KEY}
    params = {"q": query, "count": num, "mkt": "en-US"}
    r = requests.get("https://api.bing.microsoft.com/v7.0/search", headers=headers, params=params, timeout=12)
    r.raise_for_status()
    data = r.json()
    out = []
    for item in data.get("webPages", {}).get("value", [])[:num]:
        link = item.get("url")
        out.append({"title": item.get("name"), "link": link, "snippet": item.get("snippet"),
                    "source": tldextract.extract(link).registered_domain if link else None})
    return out

def get_search_results(query, num=5):
    try:
        return search_serpapi(query, num=num)
    except Exception:
        return search_bing(query, num=num)
