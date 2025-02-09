# 🚀 AI-Powered Research Assistant

## 📌 Project Overview
The **AI-Powered Research Assistant** is an intelligent search and summarization tool designed to simplify information retrieval. It leverages **LangChain, Groq API, FAISS Vector Database, and Streamlit** to fetch, summarize, and present research data from multiple sources like **ArXiv, Wikipedia, and DuckDuckGo**.

## 🔥 Features
- **🔍 Multi-Source Search**: Retrieves information from ArXiv (research papers), Wikipedia, and DuckDuckGo (web).
- **📑 AI-Powered Summarization**: Extracts concise insights from long research papers.
- **📊 Comparative Analysis**: Provides structured tables for side-by-side comparisons.
- **🎙️ Voice-Powered Assistance**: Enables voice-based queries & text-to-speech summaries.
- **📡 Real-Time Information Retrieval**: Fetches the latest insights from trusted sources.

## 🛠️ Tech Stack
- **Programming Language**: Python
- **Frameworks/Libraries**: LangChain, Groq API, FAISS, OpenAI, Streamlit
- **APIs**: ArXiv API, Wikipedia API, DuckDuckGo Search API

## 🚀 Installation & Setup
### Prerequisites:
- Python 3.9+
- API keys for **Groq API** & **OpenAI API**

### Steps:
1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/ai-research-assistant.git
   cd ai-research-assistant
   ```
2. **Create & Activate Virtual Environment**
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`
   ```
3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Set Up Environment Variables**
   Create a `.env` file and add:
   ```env
   GROQ_API_KEY=your_groq_api_key
   OPENAI_API_KEY=your_openai_api_key
   ```
5. **Run the Streamlit App**
   ```bash
   streamlit run app.py
   ```

## 🎯 How It Works
1. User enters a search query (e.g., *"Latest research on Quantum Computing"*).
2. The system searches multiple sources & fetches relevant research papers & web data.
3. AI **summarizes key insights** from the retrieved documents.
4. Users receive a **concise answer, direct research links, and comparative data**.

## 📌 Example Input & Output
### **Input Query:**
```plaintext
Tell me about Langsmith
```
### **Output:**
```plaintext
LangSmith is an advanced AI tool for...
Here is a summary from ArXiv: ...
Here is a Wikipedia summary: ...
Here are web search results: ...
```

## 🔮 Future Enhancements
✅ **Integration with Real-Time News Updates**
✅ **Support for More Research Databases (Google Scholar, IEEE Xplore)**
✅ **Chatbot Functionality for Interactive Conversations**

## 🤝 Contributing
1. Fork the repo
2. Create a new branch (`feature-branch`)
3. Commit your changes
4. Push to your branch
5. Create a pull request

## 📬 Contact
🔗 **LinkedIn**: [Your Profile](https://linkedin.com/in/your-profile)  
📧 **Email**: your.email@example.com

💡 **Let's revolutionize research with AI! 🚀**
