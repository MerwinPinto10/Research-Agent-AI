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

# **Outputs:**

![pic1](https://github.com/user-attachments/assets/307e2ba3-be7d-4bca-b0df-98e7847a40db)
![pic2](https://github.com/user-attachments/assets/25da9cd6-83d1-419b-bb96-850a5805e9ff)
![pic3](https://github.com/user-attachments/assets/9a16aeaa-5d21-442c-88fb-5ebd28451ee0)
![pic4](https://github.com/user-attachments/assets/a31448d8-ec9a-4314-bc07-3ab7e22993ba)
![pic5](https://github.com/user-attachments/assets/e3d9ad7a-3ae1-4ed4-a0be-cc79ea02f308)
![pic5](https://github.com/user-attachments/assets/c92968e9-007e-49d9-b3a9-c39e34a5f6af)
![pic5](https://github.com/user-attachments/assets/3d61bab1-90a7-4fe6-825c-331e1f82f17f)
![pic9](https://github.com/user-attachments/assets/093fa80d-9d91-4d64-825b-90b96ddcbbce)
![pic10](https://github.com/user-attachments/assets/4c836f9e-79cb-4a49-9919-083d9e1e6fde)
![pic11](https://github.com/user-attachments/assets/48db92ee-e7d7-46d2-a3a0-150f0bef35d7)
![pic12](https://github.com/user-attachments/assets/0e74bec8-6811-477b-95a7-ee019eedd622)
![pic13](https://github.com/user-attachments/assets/53bcef44-6521-4490-8b36-55e6dfc08b8b)

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

