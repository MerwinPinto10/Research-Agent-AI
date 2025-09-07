from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware

from backend.person1.articles import fetch_articles
from backend.person2.summarizer import summarize as summarizer_summarize

app = FastAPI(title="AI Research Agent Backend")

# allow frontend during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models (for validation / docs)
class Article(BaseModel):
    title: str
    url: str
    date: str
    source: str
    snippet: str
    content: str

class SummarizeRequest(BaseModel):
    query: str
    audience: str  # "child" | "student" | "professional"
    format: str    # "structured"
    top_k: int

@app.get("/api/articles", response_model=List[Article])
def api_get_articles(query: str = Query(..., min_length=1), n: int = Query(5, ge=1, le=20)):
    """
    Person1: implement this by returning fetched articles (or mock).
    Returns a JSON list with the required fields.
    """
    articles = fetch_articles(query, n=n)
    return articles

@app.post("/api/summarize")
def api_summarize(req: SummarizeRequest):
    """
    Person2: implement embeddings + summarizer here.
    This endpoint returns the exact JSON shape the frontend expects.
    """
    # Basic validation (Person2 should replace with richer logic)
    if req.audience not in {"child", "student", "professional"}:
        raise HTTPException(status_code=400, detail="audience must be 'child'|'student'|'professional'")
    if req.format != "structured":
        raise HTTPException(status_code=400, detail="format must be 'structured'")

    result = summarizer_summarize(req.query, req.audience, req.format, req.top_k)
    return result

# if you want to run with `python backend/main.py` during quick dev:
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)

import sys
import os
from backend.person1.articles import fetch_articles

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
