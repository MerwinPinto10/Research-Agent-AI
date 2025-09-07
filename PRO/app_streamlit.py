# app_streamlit.py
import streamlit as st
import requests, json, io
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

# Config
BACKEND_BASE = "http://localhost:8000"   # backend should run here
CACHE_FILE = "data/cache_demo.json"

st.set_page_config(page_title="AI Research Agent", layout="wide")

# ---------- Helpers ----------
def call_backend_summarize(query, audience="student", fmt="summary"):
    url = f"{BACKEND_BASE}/api/summarize"
    try:
        resp = requests.post(url, json={"query": query, "audience": audience, "format": fmt}, timeout=20)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        st.warning(f"Backend call failed: {e}")
        return None

def load_cache():
    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Could not read cache file: {e}")
        return None

def generate_pdf_bytes(result):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    x_margin = 40
    y = height - 60
    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(x_margin, y, f"Research Brief: {result.get('query','')}")
    y -= 30
    # Simple summary
    c.setFont("Helvetica", 11)
    c.drawString(x_margin, y, "Simple summary:")
    y -= 16
    text = c.beginText(x_margin, y)
    text.setFont("Helvetica", 10)
    for line in result.get("simple_summary", "").split("\n"):
        text.textLine(line[:200])
    c.drawText(text)
    y = text.getY() - 20
    # Key points
    c.setFont("Helvetica-Bold", 11)
    c.drawString(x_margin, y, "Key points:")
    y -= 14
    c.setFont("Helvetica", 10)
    points = result.get("key_points", [])
    for p in points:
        c.drawString(x_margin + 10, y, "- " + (p[:200]))
        y -= 12
        if y < 80:
            c.showPage(); y = height - 60
    # Citations
    if y < 140:
        c.showPage(); y = height - 60
    c.setFont("Helvetica-Bold", 11)
    c.drawString(x_margin, y, "Citations:")
    y -= 14
    c.setFont("Helvetica", 9)
    for citem in result.get("citations", []):
        line = f"{citem.get('title','')} - {citem.get('source','')} ({citem.get('date','')})"
        c.drawString(x_margin + 10, y, line[:120])
        y -= 12
        if y < 60:
            c.showPage(); y = height - 60
    c.save()
    buffer.seek(0)
    return buffer.read()

# ---------- UI ----------
st.title("AI Research Agent — Interactive Research Briefs")
col1, col2 = st.columns([3,1])

with col1:
    query = st.text_input("Enter research topic or question", value="Quantum computing breakthroughs 2025")
    audience = st.selectbox("Audience level", ["child","student","expert"], index=1)
    fmt = st.selectbox("Output format", ["summary","table","detailed"], index=0)
    use_cache = st.checkbox("Use cached demo (safe demo)", value=False)
    generate = st.button("Search & Summarize")

with col2:
    st.markdown("**Quick demo tips**")
    st.write("- For reliable demo, toggle 'Use cached demo' if network is flaky.")
    st.write("- Export PDF at the end to show judges.")
    st.write("- Ask follow-up questions in the text box below results.")

st.markdown("---")
result = None

if generate:
    with st.spinner("Running pipeline..."):
        if use_cache:
            result = load_cache()
            if result is None:
                st.error("No cache available.")
        else:
            result = call_backend_summarize(query, audience, fmt)
            if result is None:
                st.info("Falling back to cached demo.")
                result = load_cache()

# If we already had result in session
if 'last_result' in st.session_state and not generate:
    result = st.session_state['last_result']

if result:
    st.session_state['last_result'] = result
    # Simple summary tab
    tabs = st.tabs(["Simple summary", "Key points & Table", "Flowchart", "Charts", "Citations", "Notes / Export"])
    # --- Simple summary
    with tabs[0]:
        st.header("Simple summary")
        st.write(result.get("simple_summary", "No simple summary available."))
        st.markdown("**Detailed:**")
        st.write(result.get("detailed_summary", "No detailed summary available."))
    # --- Key points & table
    with tabs[1]:
        st.header("Key points")
        kp = result.get("key_points", [])
        for i, p in enumerate(kp, start=1):
            st.write(f"{i}. {p}")
        st.markdown("**Structured table**")
        table = result.get("table", [])
        if table:
            df = pd.DataFrame(table)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No table available for this query.")
    # --- Flowchart
    with tabs[2]:
        st.header("Flowchart")
        flow = result.get("flow", [])
        if flow:
            # Build DOT from flow nodes; nodes may contain 'from' key indicating parent
            dot_lines = ["digraph G {"]
            for node in flow:
                node_id = node.get("id")
                label = node.get("label", node_id)
                dot_lines.append(f'{node_id} [label="{label}"];')
            for node in flow:
                if "from" in node:
                    parents = node["from"]
                    if isinstance(parents, str):
                        parents = [parents]
                    for p in parents:
                        dot_lines.append(f'{p} -> {node["id"]};')
            dot_lines.append("}")
            dot = "\n".join(dot_lines)
            st.graphviz_chart(dot)
        else:
            st.info("No flowchart data available.")
    # --- Charts
    with tabs[3]:
        st.header("Charts")
        charts = result.get("charts", {})
        if charts:
            for name, data in charts.items():
                labels = data.get("labels", [])
                values = data.get("values", [])
                if labels and values and len(labels) == len(values):
                    dfc = pd.DataFrame({"label": labels, "value": values})
                    dfc = dfc.set_index("label")
                    st.bar_chart(dfc)
                else:
                    st.write(f"No chartable data for {name}")
        else:
            st.info("No charts available.")
    # --- Citations
    with tabs[4]:
        st.header("Citations & Sources")
        citations = result.get("citations", [])
        if citations:
            for c in citations:
                title = c.get("title", "Untitled")
                src = c.get("source","")
                url = c.get("url", "")
                date = c.get("date","")
                st.markdown(f"- **{title}** — {src} ({date})  \n  {url}")
        else:
            st.info("No citations returned.")
    # --- Notes / Export
    with tabs[5]:
        st.header("Notes & Export")
        notes = st.text_area("Personal notes (saved locally in session)", height=150)
        if st.button("Download report as PDF"):
            pdf_data = generate_pdf_bytes(result)
            st.download_button("Click to download PDF", data=pdf_data, file_name="research_brief.pdf", mime="application/pdf")
        if st.button("Download notes (.txt)"):
            st.download_button("notes.txt", data=notes or "No notes.", file_name="notes.txt")
else:
    st.info("Enter a query and press 'Search & Summarize' to begin. You can toggle 'Use cached demo' if backend is not ready.")

import streamlit as st

# --- UI Polish: Brand Header ---
st.markdown("<h1 style='text-align: center; color: gray;'>YourBrand Demo</h1>", unsafe_allow_html=True)
# OR use this simpler version:
# st.title("🚀 YourBrand: Smart Caching Demo")

# --- UI Polish: Fallback Cache Info ---
st.info("ℹ️ Note: If live data is unavailable, the app uses a fallback from the cache.")

BACKEND_BASE = "http://localhost:8000"  # replace with actual base URL
ENDPOINT = "/get_data"                  # replace with actual endpoint

# ---------- Backend adapter ----------
def adapt_backend_response(backend_json):
    """
    Maps backend JSON keys to the keys expected by the Streamlit app.
    """
    return {
        "query": backend_json.get("query_text"),
        "simple_summary": backend_json.get("short_summary"),
        "detailed_summary": backend_json.get("full_summary"),
        "key_points": backend_json.get("points", []),
        "table": backend_json.get("data_table", []),
        "flow": backend_json.get("flow_chart", []),
        "charts": backend_json.get("charts", {}),
        "citations": backend_json.get("references", []),
        "raw_articles": backend_json.get("articles", [])
    }

def call_backend_summarize(query, audience="student", fmt="summary"):
    url = f"{BACKEND_BASE}/api/summarize"
    try:
        resp = requests.post(url, json={"query": query, "audience": audience, "format": fmt}, timeout=20)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        st.warning(f"Backend call failed: {e}")
        return None

def call_backend_summarize(query, audience="student", fmt="summary"):
    url = f"{BACKEND_BASE}/api/summarize"
    try:
        resp = requests.post(url, json={"query": query, "audience": audience, "format": fmt}, timeout=20)
        resp.raise_for_status()
        backend_json = resp.json()
        # Map backend keys
        return adapt_backend_response(backend_json)
    except Exception as e:
        st.warning(f"Backend call failed: {e}")
        return None

def adapt_backend_response(backend_json):
    return {
        "query": backend_json.get("query_text"),
        "simple_summary": backend_json.get("short_summary"),
        "detailed_summary": backend_json.get("full_summary"),
        "key_points": backend_json.get("points", []),
        "table": backend_json.get("data_table", []),
        "flow": backend_json.get("flow_chart", []),
        "charts": backend_json.get("charts", {}),
        "citations": backend_json.get("references", []),
        "raw_articles": backend_json.get("articles", [])
    }

def call_backend_summarize(query, audience="student", fmt="summary"):
    url = f"{BACKEND_BASE}/api/summarize"
    try:
        resp = requests.post(url, json={"query": query, "audience": audience, "format": fmt}, timeout=20)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        st.warning(f"Backend call failed: {e}")
        return None


if generate:
    with st.spinner("Running pipeline..."):
        if use_cache:
            result = load_cache()
            if result is None:
                st.error("No cache available.")
        else:
            result = call_backend_summarize(query, audience, fmt)
            if result is None:
                st.info("Falling back to cached demo.")
                result = load_cache()
