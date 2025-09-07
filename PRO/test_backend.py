import requests

# Step 2a: Set your backend base URL
BACKEND_BASE = "http://localhost:8000"  # replace if different

# Step 2b: Choose the endpoint to test
ENDPOINT = "/api/summarize"  # or "/api/search"

"""""
payload = {
    "query": "Quantum computing breakthroughs 2025",  # your research topic
    "audience": "student",                            # audience level: child | student | expert
    "format": "summary"                               # output format: summary | table | detailed
}


try:
    response = requests.post(BACKEND_BASE + ENDPOINT, json=payload, timeout=10)
    print("Status code:", response.status_code)
    print("Response JSON:", response.json())
except Exception as e:
    print("Error:", e)

    """