import streamlit as st
import pandas as pd

st.set_page_config(page_title="AI Research Agent (Demo)", layout="centered")
st.title("AI Research Agent — Starter Demo")
st.write("This is a minimal starter Streamlit app.")

if st.button("Show sample data"):
    df = pd.DataFrame({"id": [1,2,3], "name": ["alice","bob","carol"]})
    st.dataframe(df)

import os
import requests
import streamlit as st
from dotenv import load_dotenv

# Load .env variables
load_dotenv()
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.title("AI Research Agent")

# Input query
query = st.text_input("Enter your research query")

# Dropdown for audience type
audience = st.selectbox("Audience", ["child", "student", "professional"])

if st.button("Summarize"):
    # Prepare JSON payload
    payload = {
        "query": query,
        "audience": audience,
        "format": "structured",
        "top_k": 3
    }
    # Call backend summarize endpoint
    try:
        resp = requests.post(f"{BACKEND_URL}/api/summarize", json=payload)
        resp.raise_for_status()
        data = resp.json()
        st.json(data)  # Show raw JSON response for now
    except requests.exceptions.RequestException as e:
        st.error(f"Error calling backend: {e}")

import streamlit as st
st.title("This should be in Dark Mode")
