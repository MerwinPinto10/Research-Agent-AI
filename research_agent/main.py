import os
import requests
from fastapi import FastAPI
from pydantic import BaseModel
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import openai

# Load API keys from .env file
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

openai.api_key = OPENAI_API_KEY

app = FastAPI()

# Request body model
class ResearchRequest(BaseModel):
    topic: str

# 1. Perform a web search using SerpAPI
def web_search(query: str):
    url = "https://serpapi.com/search"
    params = {
        "q": query,
        "api_key": SERPAPI_KEY,
        "engine": "google"
    }
    response = requests.get(url, params=params)
    results = response.json()
    links = []
    for item in results.get("organic_results", [])[:5]:
        links.append(item.get("link"))
    return links

# 2. Extract content from each link
def extract_content(url: str):
    try:
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
        paragraphs = " ".join([p.get_text() for p in soup.find_all("p")])
        return paragraphs[:3000]  # limit text size
    except Exception as e:
        return f"Error extracting content: {str(e)}"

# 3. Summarize using GPT
def summarize_text(text: str, topic: str):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",   # or gpt-4 if you have access
            messages=[
                {"role": "system", "content": "You are a research assistant. Summarize clearly and concisely."},
                {"role": "user", "content": f"Summarize this text about {topic}:\n{text}"}
            ],
            max_tokens=300
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error summarizing: {str(e)}"

# 4. Main research endpoint
@app.post("/research")
def research(req: ResearchRequest):
    links = web_search(req.topic)
    summaries = []
    for link in links:
        content = extract_content(link)
        summary = summarize_text(content, req.topic)
        summaries.append({"link": link, "summary": summary})
    return {"topic": req.topic, "results": summaries}
