

from typing import Dict, List
from backend.person1.articles import fetch_articles
from openai import OpenAI
import os
import json
from dotenv import load_dotenv

load_dotenv()  # Load environment variables

# Initialize OpenAI client once
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def build_prompt(query: str, articles: List[Dict]) -> str:
    prompt = f"Summarize the following articles about '{query}':\n\n"
    for i, article in enumerate(articles, 1):
        prompt += f"Article {i} Title: {article['title']}\n"
        prompt += f"Content: {article['content'][:500]}...\n\n"  # limit content length for prompt
    prompt += (
        "Please provide:\n"
        "- A child-friendly summary\n"
        "- A professional summary\n"
        "- Key points\n"
        "- Relevant tables\n"
        "- Flow nodes\n"
        "- Chart data\n"
        "- Citations\n\n"
        "Format the response as JSON with keys: summary_child, summary_professional, "
        "key_points, tables, flow_nodes, chart_data, citations."
    )
    return prompt


def summarize(query: str, audience: str = "professional", fmt: str = "structured", top_k: int = 3) -> Dict:
    # 1. Fetch relevant articles
    articles = fetch_articles(query, n=top_k)

    # 2. Create embeddings (optional, can be used for ranking or clustering)
    embeddings = [
        client.embeddings.create(
            model="text-embedding-3-small",
            input=article["content"]
        ) for article in articles
    ]

    # 3. Build prompt
    prompt = build_prompt(query, articles)

    # 4. Call LLM (GPT-4 or GPT-3.5)
    completion = client.chat.completions.create(
        model="gpt-4",  # or "gpt-3.5-turbo"
        messages=[
            {"role": "system", "content": "You are an expert research assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    result = completion.choices[0].message.content.strip()

    # 5. Parse JSON result
    try:
        parsed = json.loads(result)
    except json.JSONDecodeError:
        parsed = {
            "summary_child": "Summary could not be parsed.",
            "summary_professional": result,
            "key_points": [],
            "tables": [],
            "flow_nodes": [],
            "chart_data": {"labels": [], "values": [], "title": ""},
            "citations": []
        }

    # 6. Return structured response
    return {
        "query": query,
        "summary_child": parsed.get("summary_child", ""),
        "summary_professional": parsed.get("summary_professional", ""),
        "key_points": parsed.get("key_points", []),
        "tables": parsed.get("tables", []),
        "flow_nodes": parsed.get("flow_nodes", []),
        "chart_data": parsed.get("chart_data", {"labels": [], "values": [], "title": ""}),
        "citations": parsed.get("citations", [])
    }
