Intelligent Research Assistant powered by Groq AI, LangChain, ArXiv, Wikipedia & Web Search

Transform the way you research with AI that searches multiple sources, synthesizes information, and provides instant, accurate answers to your questions.

🎯 Problem Statement
Researchers, students, and professionals waste hours searching through:

📄 Research papers on ArXiv
📚 Wikipedia articles
🌐 Scattered web results
📖 Multiple databases

Pain Points:

Information overload
Time-consuming manual searches
Difficulty synthesizing data from multiple sources
No centralized research tool


✨ Solution: AI Research Assistant
A unified platform that:

🔍 Searches 3 sources simultaneously (ArXiv + Wikipedia + Web)
🤖 AI-powered synthesis of research findings
⚡ Instant results in conversational format
💬 Interactive chat interface for follow-up questions
🎯 Smart source selection based on query type


🏆 Key Features
🔬 Multi-Source Intelligence

ArXiv Integration: Access 2M+ research papers
Wikipedia: Comprehensive encyclopedia knowledge
Web Search: Real-time information from DuckDuckGo

🤖 AI-Powered Analysis

Powered by Groq's lightning-fast inference
Uses Llama 3.3 70B for superior understanding
Synthesizes information from all sources

💬 Conversational Interface

Natural language queries
Follow-up questions
Context-aware responses
Chat history maintained

⚡ Lightning Fast

Results in seconds (not minutes)
Parallel source searching
Optimized for speed

🎨 Beautiful UI

Modern Streamlit interface
Responsive design
Easy to use
Professional appearance


🚀 Live Demo
Try it now: Live Demo Link
Demo Video: Watch on YouTube

🛠️ Tech Stack
CategoryTechnologyFrontendStreamlitAI/LLMGroq (Llama 3.3 70B)FrameworkLangChainSearch APIsArXiv, Wikipedia, DuckDuckGoLanguagePython 3.10+

📦 Installation
Prerequisites

Python 3.10 or higher
Groq API key (Get free key)

Quick Start

Clone Repository

bashgit clone https://github.com/your-username/ai-research-assistant.git
cd ai-research-assistant

Install Dependencies

bashpip install -r requirements.txt

Run Application

bashstreamlit run app.py

Enter API Key


Open the app in your browser
Enter your Groq API key in the sidebar
Start researching!


🎮 Usage
Example Queries
Academic Research:
"Latest research on Quantum Computing"
"Explain the Transformer architecture"
"What is CRISPR gene editing?"
Technology:
"What is LangChain?"
"How does GPT-4 work?"
"Explain blockchain technology"
Science:
"Recent climate change findings"
"What is dark matter?"
"Explain photosynthesis"
General Knowledge:
"Who invented the telephone?"
"History of the Internet"
"What is machine learning?"

📊 How It Works
mermaidgraph LR
    A[User Query] --> B[LangChain Agent]
    B --> C[ArXiv Search]
    B --> D[Wikipedia Search]
    B --> E[Web Search]
    C --> F[Groq AI]
    D --> F
    E --> F
    F --> G[Synthesized Answer]
    G --> H[User]

User asks question via chat interface
LangChain agent analyzes query
Parallel search across ArXiv, Wikipedia, Web
Groq AI synthesizes results
Formatted answer displayed to user


🎯 Use Cases
👨‍🎓 Students

Quick research for assignments
Understanding complex topics
Finding credible sources

👨‍🔬 Researchers

Literature reviews
Finding recent papers
Cross-referencing information

👨‍💼 Professionals

Market research
Industry trends
Competitive analysis

👨‍💻 Developers

Technical documentation
API references
Framework comparisons


🌟 Unique Selling Points

Multi-Source: Only tool combining ArXiv + Wikipedia + Web
AI-Powered: Smart synthesis, not just search results
Free to Use: No subscription required (bring your own API key)
Privacy-First: No data stored, all processing real-time
Open Source: Fully customizable and extensible


🚀 Deployment
Deploy to Streamlit Cloud

Push code to GitHub
Go to share.streamlit.io
Connect your GitHub repo
Deploy!

Deploy to Vercel (Alternative)
bash# Install Vercel CLI
npm install -g vercel

# Deploy
vercel

📈 Roadmap
Phase 1 (Current) ✅

 Multi-source search
 AI synthesis
 Chat interface
 Streamlit deployment

Phase 2 (Next 3 Months)

 PDF upload & analysis
 Citation generation
 Export to different formats
 More research databases (IEEE, PubMed)

Phase 3 (6 Months)

 Voice input/output
 Mobile app
 Collaborative research
 API for developers


🤝 Contributing
We welcome contributions! Here's how:

Fork the repository
Create feature branch (git checkout -b feature/AmazingFeature)
Commit changes (git commit -m 'Add AmazingFeature')
Push to branch (git push origin feature/AmazingFeature)
Open Pull Request


📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

👨‍💻 Developer
Faraz Mubeen

🔗 LinkedIn
📧 Email
🐙 GitHub


🙏 Acknowledgments

Groq for lightning-fast inference
LangChain for the agent framework
Streamlit for the amazing UI framework
ArXiv for research paper access
Wikipedia for encyclopedia data
