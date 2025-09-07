

from typing import Dict, List
from backend.person1.articles import fetch_articles
from openai import OpenAI
import os
import json

# Load OpenAI client (assuming you have OPENAI_API_KEY in env)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def summarize(query: str, audience: str = "professional", fmt: str = "structured", top_k: int = 3) -> Dict:
    """
    Summarize the given query by fetching articles, creating embeddings, and
    calling an LLM to produce structured JSON summaries tailored for different audiences.

    Args:
        query (str): The topic or query to summarize.
        audience (str): Target audience (e.g., "professional", "child").
        fmt (str): Format type, default "structured".
        top_k (int): Number of top articles to fetch.

    Returns:
        Dict: JSON object with summary_child, summary_professional, key_points, tables, flow_nodes, chart_data, citations.
    """
    # 1. Fetch relevant articles
    articles = fetch_articles(query, n=top_k)
    if not articles:
        return {
            "query": query,
            "summary_child": "No articles found.",
            "summary_professional": "",
            "key_points": [],
            "tables": [],
            "flow_nodes": [],
            "chart_data": {"labels": [], "values": [], "title": ""},
            "citations": []
        }

    # 2. Create embeddings (optional, can be used for ranking or clustering)
    embeddings = [
        client.embeddings.create(
            model="text-embedding-3-small",
            input=article["content"]
        ) for article in articles
    ]

    # 3. Build a prompt for the LLM
    def build_prompt(query: str, articles: List[dict]) -> str:
        articles_text = "\n\n".join(
            [f"Title: {a['title']}\nSource: {a['source']}\nDate: {a['date']}\nContent: {a['content']}" for a in articles]
        )
        prompt = (
            f"Summarize the following articles about '{query}' for different audiences.\n"
            "Respond ONLY with a JSON object containing:\n"
            "- summary_child\n"
            "- summary_professional\n"
            "- key_points (list of strings)\n"
            "- tables (list with title, headers, rows)\n"
            "- flow_nodes (list of strings)\n"
            "- chart_data (labels, values, title)\n"
            "- citations (list with title, url, date, excerpt)\n\n"
            f"Articles:\n{articles_text}\n"
        )
        return prompt

    prompt = build_prompt(query, articles)

    # 4. Call the OpenAI chat completion API (e.g., GPT-4)
    completion = client.chat.completions.create(
        model="gpt-4",  # or "gpt-3.5-turbo"
        messages=[
            {"role": "system", "content": "You are an expert research assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    result = completion.choices[0].message.content.strip()

    # 5. Parse the returned JSON from the model
    try:
        parsed = json.loads(result)
    except json.JSONDecodeError:
        # fallback to returning raw text in professional summary if JSON parse fails
        parsed = {
            "summary_child": "Summary could not be parsed.",
            "summary_professional": result,
            "key_points": [],
            "tables": [],
            "flow_nodes": [],
            "chart_data": {"labels": [], "values": [], "title": ""},
            "citations": []
        }

    # 6. Return the structured summary
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
