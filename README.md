# 🚀 Research Agent

A simple research agent that searches topics, fetches results, and summarizes them using OpenAI’s API.

---

## 📌 Features
- 🔍 Search for any topic  
- 📄 Collect results with links  
- ✍ Summarize results automatically  
- 🌐 Runs as a FastAPI backend  

---

## 🛠️ Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/MerwinPinto10/research_agent.git
   cd research_agent
   
2. Create & activate virtual environment

python -m venv venv
# Windows (PowerShell)

3. Install dependencies
pip install -r requirements.txt

4. Set your OpenAI API key
Create a .env file in the project root:

OPENAI_API_KEY=your_api_key_here

▶️ Running the App
Start the FastAPI server:
uvicorn main:app --reload


The app will run at:
👉 http://127.0.0.1:8000

📡 API Endpoints

GET / → Root (health check)
POST /search → Search and summarize a topic

Example request:
{
  "topic": "Quantum Computing advancements"
}

⚠️ Notes

Ensure your OpenAI API key has quota (free or paid).
If you see quota exceeded, check your billing page.
Works best with OpenAI Python package version 0.28.

