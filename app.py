import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.utilities import ArxivAPIWrapper, WikipediaAPIWrapper
from langchain_community.tools import ArxivQueryRun, WikipediaQueryRun, DuckDuckGoSearchRun
from langchain.agents import initialize_agent, AgentType
from langchain.callbacks import StreamlitCallbackHandler
import os

# Page configuration
st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
    }
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: 600;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🔬 AI Research Assistant</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Powered by Groq AI, ArXiv, Wikipedia & Web Search</p>', unsafe_allow_html=True)

# Sidebar configuration
with st.sidebar:
    st.image("https://via.placeholder.com/300x100/667eea/ffffff?text=Research+AI", use_container_width=True)
    st.markdown("### ⚙️ Configuration")
    
    api_key = st.text_input(
        "🔑 Enter your Groq API Key:",
        type="password",
        help="Get your free API key from https://console.groq.com/keys"
    )
    
    if not api_key:
        st.warning("⚠️ Please enter your Groq API key to start")
        st.markdown("---")
        st.markdown("### 📌 How to get API Key:")
        st.markdown("""
        1. Go to [Groq Console](https://console.groq.com/keys)
        2. Sign up / Log in
        3. Create new API key
        4. Copy and paste here
        """)
    else:
        st.success("✅ API Key configured!")
    
    st.markdown("---")
    
    # Model selection
    model_choice = st.selectbox(
        "🤖 Select Model:",
        ["llama-3.3-70b-versatile", "llama-3.1-70b-versatile", "mixtral-8x7b-32768"],
        index=0,
        help="Choose the AI model for research"
    )
    
    st.markdown("---")
    
    # Search sources
    st.markdown("### 🔍 Active Search Sources:")
    st.markdown("""
    - ✅ **ArXiv** (Research Papers)
    - ✅ **Wikipedia** (Encyclopedia)
    - ✅ **Web Search** (Real-time)
    """)
    
    st.markdown("---")
    
    # Example queries
    st.markdown("### 💡 Example Queries:")
    example_queries = [
        "Latest research on Quantum Computing",
        "Explain Machine Learning",
        "What is LangChain?",
        "Transformer architecture in NLP",
        "Climate change recent findings"
    ]
    
    for query in example_queries:
        if st.button(f"📄 {query}", key=query, use_container_width=True):
            st.session_state.example_query = query
    
    st.markdown("---")
    
    # Statistics
    if "messages" in st.session_state:
        msg_count = len([m for m in st.session_state.messages if m["role"] == "user"])
        st.metric("📊 Questions Asked", msg_count)
    
    st.markdown("---")
    st.markdown("### 👨‍💻 Developer")
    st.markdown("[LinkedIn](https://www.linkedin.com/in/fm61/) | [Email](mailto:farazmubeen902@gmail.com)")

# Main content area
col1, col2 = st.columns([2, 1])

with col2:
    st.markdown("### 📊 Features")
    st.markdown("""
    - 🔬 Research Papers
    - 📚 Wikipedia Facts
    - 🌐 Web Search
    - 🤖 AI Summarization
    - ⚡ Real-time Results
    """)
    
    st.markdown("### 🎯 Best For:")
    st.markdown("""
    - Academic Research
    - Quick Facts
    - Tech Trends
    - Scientific Papers
    - General Knowledge
    """)

with col1:
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "👋 Hi! I'm your AI Research Assistant. I can search ArXiv papers, Wikipedia, and the web to help you find information. What would you like to know?"
            }
        ]
    
    # Check if example query was clicked
    if "example_query" in st.session_state:
        prompt = st.session_state.example_query
        del st.session_state.example_query
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.rerun()
    
    # Display chat messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
    
    # Chat input
    if prompt := st.chat_input(
        placeholder="Ask me anything about research, science, or technology...",
        disabled=not api_key
    ):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.write(prompt)
        
        # Check if API key is provided
        if not api_key:
            with st.chat_message("assistant"):
                st.error("❌ Please enter your Groq API key in the sidebar first!")
        else:
            try:
                # Initialize tools
                arxiv_wrapper = ArxivAPIWrapper(top_k_results=1, doc_content_chars_max=500)
                arxiv = ArxivQueryRun(api_wrapper=arxiv_wrapper)
                
                wiki_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=500)
                wiki = WikipediaQueryRun(api_wrapper=wiki_wrapper)
                
                search = DuckDuckGoSearchRun(name="Search")
                
                # Initialize LLM
                llm = ChatGroq(
                    groq_api_key=api_key,
                    model_name=model_choice,
                    streaming=True,
                    temperature=0.7
                )
                
                # Initialize agent
                tools = [search, arxiv, wiki]
                search_agent = initialize_agent(
                    tools,
                    llm,
                    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                    handling_parsing_errors=True,
                    verbose=True
                )
                
                # Generate response
                with st.chat_message("assistant"):
                    with st.spinner("🔍 Searching across multiple sources..."):
                        st_callback = StreamlitCallbackHandler(
                            st.container(),
                            expand_new_thoughts=False
                        )
                        
                        response = search_agent.run(
                            prompt,
                            callbacks=[st_callback]
                        )
                        
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": response
                        })
                        
                        st.write(response)
                        
                        # Success message
                        st.success("✅ Search complete!")
                        
            except Exception as e:
                with st.chat_message("assistant"):
                    st.error(f"❌ Error: {str(e)}")
                    
                    if "API key" in str(e) or "401" in str(e):
                        st.warning("💡 Your API key might be invalid. Please check and try again.")
                    elif "rate limit" in str(e).lower():
                        st.warning("💡 Rate limit exceeded. Please wait a moment and try again.")
                    else:
                        st.warning("💡 An unexpected error occurred. Please try again.")
                    
                    # Add error to messages
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": f"I encountered an error: {str(e)}"
                    })

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 🚀 About")
    st.markdown("AI-powered research assistant using LangChain and Groq")

with col2:
    st.markdown("### 📚 Sources")
    st.markdown("ArXiv • Wikipedia • DuckDuckGo")

with col3:
    st.markdown("### 🔗 Links")
    st.markdown("[GitHub](https://github.com/your-repo) • [Docs](https://docs.groq.com)")
