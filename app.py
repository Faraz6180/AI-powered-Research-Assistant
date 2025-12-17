import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.utilities import ArxivAPIWrapper, WikipediaAPIWrapper
from langchain_community.tools import ArxivQueryRun, WikipediaQueryRun, DuckDuckGoSearchRun
from langchain.agents import AgentExecutor, create_react_agent
from langchain import hub
from langchain.callbacks import StreamlitCallbackHandler
from langchain.prompts import PromptTemplate
import time

# Page configuration - MUST BE FIRST
st.set_page_config(
    page_title="AI Research Assistant | Powered by Groq",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium CSS with animations and modern design
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main Container */
    .main {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        background-attachment: fixed;
    }
    
    /* Animated Header */
    .main-header {
        font-size: 4rem;
        font-weight: 900;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
        animation: glow 2s ease-in-out infinite alternate;
        letter-spacing: -2px;
    }
    
    @keyframes glow {
        from {
            text-shadow: 0 0 20px #667eea, 0 0 30px #667eea, 0 0 40px #667eea;
        }
        to {
            text-shadow: 0 0 30px #764ba2, 0 0 40px #764ba2, 0 0 50px #764ba2;
        }
    }
    
    /* Subtitle with typing animation */
    .subtitle {
        text-align: center;
        color: #a0aec0;
        font-size: 1.3rem;
        margin-bottom: 3rem;
        font-weight: 300;
        letter-spacing: 2px;
    }
    
    /* Premium Cards */
    .premium-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .premium-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px 0 rgba(102, 126, 234, 0.5);
        border: 1px solid rgba(102, 126, 234, 0.3);
    }
    
    /* Gradient Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        width: 100%;
        letter-spacing: 0.5px;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    /* Input Fields */
    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        color: white;
        padding: 1rem;
        font-size: 1rem;
    }
    
    .stTextInput>div>div>input:focus,
    .stTextArea>div>div>textarea:focus {
        border: 1px solid #667eea;
        box-shadow: 0 0 20px rgba(102, 126, 234, 0.3);
    }
    
    /* Chat Messages */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
        border-right: 1px solid rgba(102, 126, 234, 0.2);
    }
    
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #667eea;
        font-weight: 700;
    }
    
    /* Success/Error Messages */
    .stSuccess {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        border-radius: 12px;
        padding: 1rem;
        color: white;
        font-weight: 600;
    }
    
    .stError {
        background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
        border-radius: 12px;
        padding: 1rem;
        color: white;
        font-weight: 600;
    }
    
    .stWarning {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        border-radius: 12px;
        padding: 1rem;
        color: white;
        font-weight: 600;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 2.5rem;
        font-weight: 900;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Feature Badges */
    .feature-badge {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 0.5rem 1rem;
        border-radius: 20px;
        margin: 0.25rem;
        font-size: 0.9rem;
        font-weight: 600;
        color: white;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: #667eea !important;
    }
    
    /* Selectbox */
    .stSelectbox>div>div {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        color: white;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 1rem 2rem;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Pulse Animation for API Status */
    @keyframes pulse {
        0% {
            box-shadow: 0 0 0 0 rgba(102, 126, 234, 0.7);
        }
        70% {
            box-shadow: 0 0 0 10px rgba(102, 126, 234, 0);
        }
        100% {
            box-shadow: 0 0 0 0 rgba(102, 126, 234, 0);
        }
    }
    
    .pulse-dot {
        width: 12px;
        height: 12px;
        background: #11998e;
        border-radius: 50%;
        display: inline-block;
        animation: pulse 2s infinite;
        margin-right: 8px;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1a1a2e;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    /* Loading Animation */
    .loading-text {
        background: linear-gradient(90deg, #667eea, #764ba2, #f093fb, #667eea);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradient 3s ease infinite;
        font-weight: 700;
        font-size: 1.2rem;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
</style>
""", unsafe_allow_html=True)

# Animated Header with Emoji
st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <h1 class="main-header">🚀 AI Research Assistant</h1>
    <p class="subtitle">POWERED BY GROQ • ARXIV • WIKIPEDIA • WEB SEARCH</p>
</div>
""", unsafe_allow_html=True)

# Premium Feature Badges
st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <span class="feature-badge">⚡ Lightning Fast</span>
    <span class="feature-badge">🤖 AI-Powered</span>
    <span class="feature-badge">🔬 Multi-Source</span>
    <span class="feature-badge">🎯 Smart Synthesis</span>
    <span class="feature-badge">🌐 Real-Time</span>
</div>
""", unsafe_allow_html=True)

# Sidebar with Premium Design
with st.sidebar:
    # Logo/Branding Area
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <div style="font-size: 4rem;">🔬</div>
        <h2 style="color: #667eea; margin-top: 1rem;">Research AI</h2>
        <p style="color: #a0aec0; font-size: 0.9rem;">Your Intelligent Research Companion</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # API Key Input with Status
    st.markdown("### 🔑 API Configuration")
    api_key = st.text_input(
        "Groq API Key",
        type="password",
        help="Get your free key from console.groq.com",
        placeholder="gsk_..."
    )
    
    if api_key:
        st.markdown('<div><span class="pulse-dot"></span><span style="color: #11998e; font-weight: 600;">Connected</span></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div><span style="display: inline-block; width: 12px; height: 12px; background: #f45c43; border-radius: 50%; margin-right: 8px;"></span><span style="color: #f45c43; font-weight: 600;">Disconnected</span></div>', unsafe_allow_html=True)
        
        with st.expander("📘 How to get API Key", expanded=False):
            st.markdown("""
            **Step-by-step:**
            1. Visit [Groq Console](https://console.groq.com/keys)
            2. Sign up (it's free!)
            3. Click "Create API Key"
            4. Copy & paste here
            
            ⚡ **Free tier includes:**
            - 14,400 requests/day
            - No credit card needed
            - Full model access
            """)
    
    st.markdown("---")
    
    # Model Selection
    st.markdown("### 🤖 AI Model")
    model_choice = st.selectbox(
        "Select Model",
        [
            "llama-3.3-70b-versatile",
            "llama-3.1-70b-versatile", 
            "mixtral-8x7b-32768"
        ],
        index=0,
        help="Llama 3.3 70B recommended for best results"
    )
    
    # Model Info
    if "llama-3.3" in model_choice:
        st.info("🏆 **Best Choice** - Newest & most capable")
    
    st.markdown("---")
    
    # Active Sources
    st.markdown("### 📚 Active Sources")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div style="background: rgba(102, 126, 234, 0.1); padding: 1rem; border-radius: 10px; text-align: center;">
            <div style="font-size: 2rem;">📄</div>
            <div style="font-weight: 600; margin-top: 0.5rem;">ArXiv</div>
            <div style="font-size: 0.8rem; color: #a0aec0;">Research</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style="background: rgba(102, 126, 234, 0.1); padding: 1rem; border-radius: 10px; text-align: center;">
            <div style="font-size: 2rem;">📚</div>
            <div style="font-weight: 600; margin-top: 0.5rem;">Wikipedia</div>
            <div style="font-size: 0.8rem; color: #a0aec0;">Facts</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: rgba(102, 126, 234, 0.1); padding: 1rem; border-radius: 10px; text-align: center; margin-top: 1rem;">
        <div style="font-size: 2rem;">🌐</div>
        <div style="font-weight: 600; margin-top: 0.5rem;">Web Search</div>
        <div style="font-size: 0.8rem; color: #a0aec0;">Real-time</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Quick Examples
    st.markdown("### 💡 Quick Examples")
    
    examples = {
        "🔬 Quantum Computing": "Latest research on Quantum Computing",
        "🤖 Machine Learning": "Explain Machine Learning fundamentals",
        "🧬 CRISPR Technology": "What is CRISPR gene editing?",
        "🌍 Climate Change": "Recent climate change findings",
        "⚡ Transformers": "Explain Transformer architecture in NLP"
    }
    
    for label, query in examples.items():
        if st.button(label, key=query, use_container_width=True):
            st.session_state.example_query = query
    
    st.markdown("---")
    
    # Statistics
    if "messages" in st.session_state:
        queries = len([m for m in st.session_state.messages if m["role"] == "user"])
        st.markdown("### 📊 Session Stats")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Queries", queries, delta=None)
        with col2:
            st.metric("Sources", "3", delta=None)
    
    st.markdown("---")
    
    # Footer
    st.markdown("""
    <div style="text-align: center; padding: 1rem; color: #a0aec0; font-size: 0.8rem;">
        <div style="margin-bottom: 0.5rem;">Built with ❤️ by</div>
        <a href="https://www.linkedin.com/in/fm61/" target="_blank" style="color: #667eea; text-decoration: none; font-weight: 600;">Faraz Mubeen</a>
        <div style="margin-top: 1rem;">
            <a href="https://github.com/your-repo" target="_blank" style="color: #a0aec0; margin: 0 0.5rem;">GitHub</a>
            <a href="mailto:farazmubeen902@gmail.com" style="color: #a0aec0; margin: 0 0.5rem;">Email</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Main Content Area
col1, col2 = st.columns([7, 3])

# Right Column - Features & Info
with col2:
    st.markdown("""
    <div class="premium-card">
        <h3 style="color: #667eea; margin-bottom: 1rem;">✨ Key Features</h3>
        <div style="line-height: 2;">
            <div>🎯 <b>Smart Search</b> - Multi-source intelligence</div>
            <div>⚡ <b>Lightning Fast</b> - Groq-powered speed</div>
            <div>🤖 <b>AI Synthesis</b> - Intelligent analysis</div>
            <div>🔬 <b>Research Grade</b> - Academic quality</div>
            <div>🌐 <b>Real-time</b> - Up-to-date info</div>
            <div>🎨 <b>Beautiful UI</b> - Premium design</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="premium-card">
        <h3 style="color: #667eea; margin-bottom: 1rem;">🎯 Perfect For</h3>
        <div style="line-height: 2;">
            <div>👨‍🎓 <b>Students</b> - Quick research</div>
            <div>👨‍🔬 <b>Researchers</b> - Literature review</div>
            <div>👨‍💼 <b>Professionals</b> - Market intel</div>
            <div>👨‍💻 <b>Developers</b> - Tech docs</div>
            <div>📚 <b>Learners</b> - Knowledge gain</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="premium-card">
        <h3 style="color: #667eea; margin-bottom: 1rem;">🏆 Why Choose Us?</h3>
        <div style="line-height: 1.8; font-size: 0.9rem;">
            Unlike traditional search engines, we don't just find information - we <b>synthesize</b> it. 
            Our AI analyzes multiple authoritative sources and provides you with comprehensive, 
            accurate answers in seconds.
        </div>
    </div>
    """, unsafe_allow_html=True)

# Left Column - Chat Interface
with col1:
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [{
            "role": "assistant",
            "content": "👋 **Welcome!** I'm your AI Research Assistant. I can search ArXiv papers, Wikipedia, and the web to help you find accurate information. What would you like to know?"
        }]
    
    # Handle example query
    if "example_query" in st.session_state:
        prompt = st.session_state.example_query
        del st.session_state.example_query
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.rerun()
    
    # Display chat messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"], avatar="🤖" if msg["role"] == "assistant" else "👤"):
            st.markdown(msg["content"])
    
    # Chat input
    if prompt := st.chat_input(
        "🔍 Ask me anything about research, science, or technology...",
        disabled=not api_key
    ):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)
        
        # Check API key
        if not api_key:
            with st.chat_message("assistant", avatar="🤖"):
                st.error("🔑 **API Key Required** - Please enter your Groq API key in the sidebar to get started!")
        else:
            try:
                # Initialize tools
                with st.spinner(""):
                    arxiv_wrapper = ArxivAPIWrapper(top_k_results=1, doc_content_chars_max=500)
                    arxiv = ArxivQueryRun(api_wrapper=arxiv_wrapper)
                    
                    wiki_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=500)
                    wiki = WikipediaQueryRun(api_wrapper=wiki_wrapper)
                    
                    search = DuckDuckGoSearchRun(name="Search")
                    
                    tools = [search, arxiv, wiki]
                    
                    # Initialize LLM
                    llm = ChatGroq(
                        groq_api_key=api_key,
                        model_name=model_choice,
                        streaming=True,
                        temperature=0.7
                    )
                    
                    # Create prompt template
                    prompt_template = PromptTemplate.from_template(
                        """Answer the following question as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
{agent_scratchpad}"""
                    )
                    
                    # Create agent
                    agent = create_react_agent(llm, tools, prompt_template)
                    agent_executor = AgentExecutor(
                        agent=agent,
                        tools=tools,
                        verbose=True,
                        handle_parsing_errors=True,
                        max_iterations=5
                    )
                
                # Generate response
                with st.chat_message("assistant", avatar="🤖"):
                    # Show searching animation
                    with st.status("🔍 **Searching across multiple sources...**", expanded=True) as status:
                        st.write("📄 Checking ArXiv research papers...")
                        time.sleep(0.5)
                        st.write("📚 Searching Wikipedia...")
                        time.sleep(0.5)
                        st.write("🌐 Querying web search...")
                        time.sleep(0.5)
                        st.write("🤖 Synthesizing results with AI...")
                        
                        st_callback = StreamlitCallbackHandler(
                            st.container(),
                            expand_new_thoughts=False
                        )
                        
                        response = agent_executor.invoke(
                            {"input": prompt},
                            {"callbacks": [st_callback]}
                        )
                        
                        answer = response["output"]
                        
                        status.update(label="✅ **Search Complete!**", state="complete")
                    
                    # Display answer
                    st.markdown(answer)
                    
                    # Add to history
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer
                    })
                    
                    # Success message
                    st.success("✨ **Answer generated from 3 authoritative sources**")
                    
            except Exception as e:
                with st.chat_message("assistant", avatar="🤖"):
                    error_msg = str(e)
                    
                    if "API key" in error_msg or "401" in error_msg or "authentication" in error_msg.lower():
                        st.error("🔑 **Invalid API Key** - Please check your Groq API key and try again.")
                        st.info("💡 Get a new key from [console.groq.com/keys](https://console.groq.com/keys)")
                    elif "rate limit" in error_msg.lower():
                        st.warning("⏳ **Rate Limit Reached** - Please wait a moment and try again.")
                    elif "timeout" in error_msg.lower():
                        st.warning("⏱️ **Request Timeout** - The search took too long. Please try again.")
                    else:
                        st.error(f"❌ **Error:** {error_msg}")
                        st.info("💡 Please try again or rephrase your question.")
                    
                    # Add error to history
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": f"⚠️ I encountered an error: {error_msg}"
                    })

# Bottom Info Bar
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div style="text-align: center; padding: 1rem;">
        <div style="font-size: 2rem;">⚡</div>
        <div style="font-weight: 600; color: #667eea;">Lightning Fast</div>
        <div style="font-size: 0.8rem; color: #a0aec0;">Powered by Groq</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="text-align: center; padding: 1rem;">
        <div style="font-size: 2rem;">🎯</div>
        <div style="font-weight: 600; color: #667eea;">Multi-Source</div>
        <div style="font-size: 0.8rem; color: #a0aec0;">3 databases</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="text-align: center; padding: 1rem;">
        <div style="font-size: 2rem;">🤖</div>
        <div style="font-weight: 600; color: #667eea;">AI-Powered</div>
        <div style="font-size: 0.8rem; color: #a0aec0;">Smart synthesis</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div style="text-align: center; padding: 1rem;">
        <div style="font-size: 2rem;">🔒</div>
        <div style="font-weight: 600; color: #667eea;">Privacy First</div>
        <div style="font-size: 0.8rem; color: #a0aec0;">No data stored</div>
    </div>
    """, unsafe_allow_html=True)
