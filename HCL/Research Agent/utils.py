# src/utils.py
import hashlib, json, os, time
from datetime import datetime

def id_from_url(url):
    h = hashlib.sha256(url.encode("utf-8")).hexdigest()[:16]
    return f"a_{h}"

def now_iso():
    return datetime.utcnow().isoformat() + "Z"

def safe_filename(s):
    return "".join(c if c.isalnum() or c in "-_." else "_" for c in s)[:120]
