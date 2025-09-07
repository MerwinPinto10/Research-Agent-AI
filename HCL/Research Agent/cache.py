# src/cache.py
import os, json
from .utils import safe_filename
CACHE_DIR = "cached_results"
os.makedirs(CACHE_DIR, exist_ok=True)

def save_cache(name, data):
    fn = os.path.join(CACHE_DIR, safe_filename(name) + ".json")
    with open(fn, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_cache(name):
    fn = os.path.join(CACHE_DIR, safe_filename(name) + ".json")
    if not os.path.exists(fn):
        return None
    with open(fn, "r", encoding="utf-8") as f:
        return json.load(f)
