📖 Overview
This project is an AI-powered search engine that combines LLMs, Retrieval-Augmented Generation (RAG), and autonomous agents to deliver accurate, real-time answers from multiple sources.

✨ Features:
✅ Retrieval-Augmented Generation (RAG) – AI fetches real-time data before responding.
✅ Multi-Source Search – Wikipedia, Arxiv (academic papers), and DuckDuckGo (live web).
✅ LangChain Agents – AI decides the best tool for each query.
✅ Interactive UI – Built with Streamlit for easy access.
✅ Fast & Scalable – Uses FAISS vector storage for efficient retrieval.

🔗 Live Demo: [Coming Soon]
📂 GitHub Repository: [Your GitHub Link]

🛠️ Tech Stack
Category	Technologies Used
LLM	Groq Llama3-8b-8192, OpenAI GPT
Search APIs	Wikipedia API, Arxiv API, DuckDuckGo Search
Frameworks	LangChain, Streamlit
Vector DB	FAISS, ChromaDB
Database	MySQL, SQLAlchemy
Others	Python, Hugging Face, dotenv
🚀 Installation & Setup
1️⃣ Clone the Repository
sh
Copy
Edit
git clone https://github.com/yourusername/ai-search-engine.git
cd ai-search-engine
2️⃣ Create a Virtual Environment
sh
Copy
Edit
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
3️⃣ Install Dependencies
sh
Copy
Edit
pip install -r requirements.txt
4️⃣ Set Up API Keys
Create a .env file in the root directory and add:

sh
Copy
Edit
GROQ_API_KEY=your_groq_api_key
OPENAI_API_KEY=your_openai_api_key
5️⃣ Run the Application
sh
Copy
Edit
streamlit run app.py
💡 Open localhost:8501 in your browser to access the AI search engine UI.

🖥️ How It Works
1️⃣ User asks a question.
2️⃣ AI agent decides which tool to use (Wikipedia, Arxiv, DuckDuckGo).
3️⃣ Tool fetches real-time data.
4️⃣ AI processes the results and generates an answer.
5️⃣ Response is displayed in the Streamlit UI.

🔍 Example Query:

arduino
Copy
Edit
"What is the latest research on Quantum Computing?"
🧠 Agent Uses: Arxiv API → Finds relevant research papers → Returns a summary.
