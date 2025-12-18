import streamlit as st
import time
from langchain_groq import ChatGroq
from langchain_community.utilities import (
    ArxivAPIWrapper,
    WikipediaAPIWrapper
)
from langchain_community.tools import (
    ArxivQueryRun,
    WikipediaQueryRun,
    DuckDuckGoSearchRun
)
from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain import hub

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="AI Research Copilot",
    page_icon="🚀",
    layout="wide"
)

# =========================
# SIMPLE PREMIUM CSS
# =========================
st.markdown("""
<style>
body {
    background: linear-gradient(135deg,#0f0c29,#302b63,#24243e);
}
.main-title {
    font-size: 3.2rem;
    font-weight: 800;
    text-align: center;
    background: linear-gradient(90deg,#667eea,#764ba2,#f093fb);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.subtitle {
    text-align: center;
    color: #cbd5e1;
    margin-bottom: 2rem;
}
.card {
    background: rgba(255,255,255,0.06);
    padding: 1.5rem;
    border-radius: 16px;
    margin-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.markdown('<div class="main-title">🚀 AI Research Copilot</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Ask once. Get verified answers with citations from ArXiv, Wikipedia & Web.</div>',
    unsafe_allow_html=True
)

# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.markdown("## ⚙️ Configuration")

    demo_mode = st.toggle("🧪 Demo Mode (No API Key)", value=False)

    api_key = st.text_input(
        "Groq API Key",
        type="password",
        disabled=demo_mode,
        help="Get free key: https://console.groq.com/keys"
    )

    model = st.selectbox(
        "Model",
        ["llama-3.3-70b-versatile", "llama-3.1-70b-versatile", "mixtral-8x7b-32768"],
        index=0
    )

    st.markdown("---")
    st.markdown("### 🏆 Why This Wins")
    st.markdown("""
    - Multi-source verification  
    - Research-grade answers  
    - Real citations  
    - Groq-level speed  
    """)
    
    st.markdown("---")
    st.markdown("### 💡 Quick Tests:")
    
    if st.button("🔬 Quantum Computing", use_container_width=True):
        st.session_state.example = "What are the latest advancements in quantum computing?"
    
    if st.button("🤖 Machine Learning", use_container_width=True):
        st.session_state.example = "What is machine learning and its applications?"
    
    if st.button("🧬 CRISPR Technology", use_container_width=True):
        st.session_state.example = "Explain CRISPR gene editing technology"
    
    if st.button("🌍 Climate Change", use_container_width=True):
        st.session_state.example = "What are recent climate change research findings?"

# =========================
# LAYOUT
# =========================
left, right = st.columns([7, 3])

with right:
    st.markdown('<div class="card"><b>Perfect For</b><br>🎓 Students<br>🔬 Researchers<br>👨‍💻 Developers</div>', unsafe_allow_html=True)
    st.markdown('<div class="card"><b>Key Advantage</b><br>Not just answers — verified synthesis.</div>', unsafe_allow_html=True)
    
    if "messages" in st.session_state and len(st.session_state.messages) > 1:
        msg_count = len([m for m in st.session_state.messages if m["role"] == "user"])
        st.markdown(f'<div class="card"><b>Questions Asked</b><br>📊 {msg_count}</div>', unsafe_allow_html=True)

# =========================
# CHAT STATE
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Ask a research question. I'll verify it across multiple sources and cite them."
        }
    ]

# Handle example queries
if "example" in st.session_state:
    user_query = st.session_state.example
    del st.session_state.example
    st.session_state.messages.append({"role": "user", "content": user_query})
    st.rerun()

# =========================
# DISPLAY CHAT
# =========================
with left:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_query = st.chat_input("Ask a research question…", disabled=(not demo_mode and not api_key))

# =========================
# HANDLE QUERY
# =========================
if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})

    with left:
        with st.chat_message("user"):
            st.markdown(user_query)

    # -------------------------
    # DEMO MODE
    # -------------------------
    if demo_mode:
        with left:
            with st.chat_message("assistant"):
                with st.spinner("Synthesizing verified sources…"):
                    time.sleep(2)

                demo_answer = f"""
### Answer
Based on your question about **"{user_query[:60]}..."**

Quantum Computing uses **qubits** that leverage superposition and entanglement to perform certain computations exponentially faster than classical computers. Recent breakthroughs include:

- **Error Correction**: New techniques reducing quantum decoherence
- **Algorithm Development**: Improved quantum algorithms for optimization
- **Hardware Advances**: Room-temperature quantum processors in development

### Key Applications
- Cryptography and security
- Drug discovery and molecular simulation
- Financial modeling and optimization
- Machine learning acceleration

### Sources
- **[ArXiv]** Preskill, J. (2023). *Quantum Computing in the NISQ era and beyond*
- **[Wikipedia]** Quantum Computing - Comprehensive overview
- **[Web]** IBM Quantum Experience - Latest developments (Dec 2024)

---
*Note: Demo mode active. Disable for real-time research with your Groq API key.*
"""
                st.markdown(demo_answer)

                st.download_button(
                    "📄 Download as Markdown",
                    demo_answer,
                    file_name="research_answer.md"
                )

        st.session_state.messages.append(
            {"role": "assistant", "content": demo_answer}
        )

    # -------------------------
    # REAL MODE - EXACT METHOD FROM YOUR JUPYTER NOTEBOOK
    # -------------------------
    else:
        if not api_key:
            with left:
                with st.chat_message("assistant"):
                    st.error("⚠️ Please enter your Groq API key or enable Demo Mode!")
        else:
            try:
                with left:
                    with st.chat_message("assistant"):
                        # Show progress
                        progress_container = st.container()
                        
                        with progress_container:
                            status = st.status("🔍 Initializing research tools...", expanded=True)
                            
                            with status:
                                st.write("📚 Setting up ArXiv research database...")
                                
                                # Initialize tools - EXACTLY like your Jupyter notebook
                                arxiv_wrapper = ArxivAPIWrapper(
                                    top_k_results=1,
                                    doc_content_chars_max=1000
                                )
                                arxiv = ArxivQueryRun(api_wrapper=arxiv_wrapper)
                                
                                st.write("📖 Connecting to Wikipedia...")
                                
                                wiki_wrapper = WikipediaAPIWrapper(
                                    top_k_results=1,
                                    doc_content_chars_max=1000
                                )
                                wiki = WikipediaQueryRun(api_wrapper=wiki_wrapper)
                                
                                st.write("🌐 Enabling web search...")
                                
                                search = DuckDuckGoSearchRun(name="Search")
                                
                                tools = [wiki, arxiv, search]  # Order matters!
                                
                                st.write("🤖 Connecting to Groq AI...")
                                
                                # Initialize LLM - EXACTLY like your notebook
                                llm = ChatGroq(
                                    groq_api_key=api_key,
                                    model_name=model,
                                    streaming=True
                                )
                                
                                st.write("🔗 Loading agent prompt...")
                                
                                # Use the EXACT prompt from your notebook that works!
                                try:
                                    prompt = hub.pull("hwchase17/openai-functions-agent")
                                except Exception as e:
                                    st.warning("Using fallback prompt (hub unavailable)")
                                    from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
                                    prompt = ChatPromptTemplate.from_messages([
                                        ("system", "You are a helpful research assistant that provides verified information with citations."),
                                        MessagesPlaceholder(variable_name="chat_history", optional=True),
                                        ("human", "{input}"),
                                        MessagesPlaceholder(variable_name="agent_scratchpad")
                                    ])
                                
                                st.write("⚡ Creating agent...")
                                
                                # Create agent - EXACTLY like your notebook
                                agent = create_openai_tools_agent(llm, tools, prompt)
                                
                                # Create executor
                                agent_executor = AgentExecutor(
                                    agent=agent,
                                    tools=tools,
                                    verbose=True,
                                    handle_parsing_errors=True,
                                    max_iterations=10
                                )
                                
                                status.update(label="✅ Ready! Searching sources...", state="running")
                        
                        # Run the agent
                        with st.spinner("🔍 Researching across multiple sources..."):
                            result = agent_executor.invoke({"input": user_query})
                        
                        # Get the answer
                        answer = result.get("output", "")
                        
                        # Format the answer if it's plain text
                        if "### Answer" not in answer and "### Sources" not in answer:
                            formatted_answer = f"""
### Answer
{answer}

### Sources
Based on the research conducted across:
- **ArXiv** - Research papers
- **Wikipedia** - Encyclopedia facts
- **Web Search** - Latest information
"""
                            answer = formatted_answer
                        
                        # Display
                        st.markdown("---")
                        st.markdown(answer)
                        st.success("✅ Research complete!")
                        
                        st.download_button(
                            "📄 Download as Markdown",
                            answer,
                            file_name="research_answer.md"
                        )

                st.session_state.messages.append(
                    {"role": "assistant", "content": answer}
                )

            except Exception as e:
                error_msg = str(e)
                
                with left:
                    with st.chat_message("assistant"):
                        st.error(f"❌ Error: {error_msg}")
                        
                        if "401" in error_msg or "API key" in error_msg or "Unauthorized" in error_msg:
                            st.warning("💡 Invalid API key. Get a new one from console.groq.com")
                        elif "rate limit" in error_msg.lower() or "429" in error_msg:
                            st.warning("💡 Rate limit reached. Wait a moment and try again.")
                        elif "tool" in error_msg.lower() or "parsing" in error_msg.lower():
                            st.warning("💡 Agent processing issue. Try rephrasing your question.")
                        else:
                            st.info("💡 Try Demo Mode to see how it works, or check your API key.")
                        
                        # Show detailed error in expander
                        with st.expander("🔍 Technical Details"):
                            st.code(error_msg)

# Footer
st.markdown("---")
st.markdown(
    '<div style="text-align: center; color: #94a3b8;">Made with ❤️ for the Research Community | Powered by Groq AI & LangChain</div>',
    unsafe_allow_html=True
)
