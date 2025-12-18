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
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain.callbacks import StreamlitCallbackHandler

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
        ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"]
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
    st.markdown("### 💡 Try These:")
    
    if st.button("🔬 Quantum Computing", use_container_width=True):
        st.session_state.example = "What are the latest breakthroughs in quantum computing?"
    
    if st.button("🤖 Transformer Models", use_container_width=True):
        st.session_state.example = "How do transformer models work in NLP?"
    
    if st.button("🧬 CRISPR Technology", use_container_width=True):
        st.session_state.example = "What is CRISPR and its applications?"
    
    if st.button("🌍 Climate Solutions", use_container_width=True):
        st.session_state.example = "What are effective climate change solutions?"

# =========================
# LAYOUT
# =========================
left, right = st.columns([7, 3])

with right:
    st.markdown('<div class="card"><b>Perfect For</b><br>🎓 Students<br>🔬 Researchers<br>👨‍💻 Developers</div>', unsafe_allow_html=True)
    st.markdown('<div class="card"><b>Key Advantage</b><br>Not just answers — verified synthesis.</div>', unsafe_allow_html=True)
    
    # Show stats if messages exist
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

# Handle example button clicks
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
    # DEMO MODE RESPONSE
    # -------------------------
    if demo_mode:
        with left:
            with st.chat_message("assistant"):
                with st.spinner("Synthesizing verified sources…"):
                    time.sleep(2)

                demo_answer = f"""
### Answer
Based on your question about **{user_query[:50]}...**, here's a comprehensive answer:

Quantum Computing represents a paradigm shift in computational power. Unlike classical computers that use bits (0 or 1), quantum computers use **qubits** that can exist in superposition—simultaneously representing both 0 and 1. This property, combined with quantum entanglement, allows quantum computers to solve certain problems exponentially faster than classical systems.

Key applications include:
- **Cryptography**: Breaking traditional encryption
- **Drug Discovery**: Simulating molecular interactions
- **Optimization**: Solving complex logistics problems
- **Machine Learning**: Processing vast datasets

### Sources
- **[ArXiv]** Preskill, J. (2018). *Quantum Computing in the NISQ era and beyond*
- **[Wikipedia]** Quantum Computing - Comprehensive overview
- **[Web]** IBM Quantum Experience - Latest developments (2024)

---
*Note: This is demo mode. Toggle it off and add your Groq API key for real-time research.*
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
    # REAL MODE WITH FIXED AGENT
    # -------------------------
    else:
        if not api_key:
            with left:
                with st.chat_message("assistant"):
                    st.error("⚠️ Please enter your Groq API key in the sidebar or enable Demo Mode!")
        else:
            try:
                # Initialize tools
                arxiv = ArxivQueryRun(
                    api_wrapper=ArxivAPIWrapper(
                        top_k_results=1,
                        doc_content_chars_max=1000
                    )
                )
                wiki = WikipediaQueryRun(
                    api_wrapper=WikipediaAPIWrapper(
                        top_k_results=1,
                        doc_content_chars_max=1000
                    )
                )
                web = DuckDuckGoSearchRun(name="WebSearch")

                tools = [arxiv, wiki, web]

                # Initialize LLM
                llm = ChatGroq(
                    groq_api_key=api_key,
                    model_name=model,
                    temperature=0.6,
                    max_tokens=2000
                )

                # FIXED PROMPT TEMPLATE - This is the key fix!
                prompt = PromptTemplate.from_template("""
You are a research assistant that provides verified, cited answers.

You have access to these tools:
{tools}

Tool names: {tool_names}

ALWAYS use tools to verify information. Never rely on memory alone.

Use this format:

Question: the input question
Thought: think about what sources to check
Action: the tool to use (must be one of [{tool_names}])
Action Input: the search query
Observation: the tool's result
... (repeat Thought/Action/Observation as needed)
Thought: I now have verified information
Final Answer: 

### Answer
<comprehensive explanation with specific facts from sources>

### Sources
- [ArXiv] <specific paper if found>
- [Wikipedia] <article title>
- [Web] <relevant findings>

Begin!

Question: {input}
{agent_scratchpad}
""")

                # Create agent
                agent = create_react_agent(llm, tools, prompt)
                executor = AgentExecutor(
                    agent=agent,
                    tools=tools,
                    verbose=True,
                    handle_parsing_errors=True,
                    max_iterations=10
                )

                with left:
                    with st.chat_message("assistant"):
                        # Create status container for tool usage
                        status_container = st.status("🔍 Researching across sources...", expanded=True)
                        
                        with status_container:
                            st.write("📚 Checking ArXiv for research papers...")
                            st.write("📖 Searching Wikipedia for verified facts...")
                            st.write("🌐 Scanning web for latest information...")
                            
                            # Create callback for showing agent's thinking
                            callback_container = st.container()
                            st_callback = StreamlitCallbackHandler(
                                callback_container,
                                expand_new_thoughts=True
                            )
                            
                            # Run agent with callbacks
                            result = executor.invoke(
                                {"input": user_query},
                                {"callbacks": [st_callback]}
                            )
                            
                            status_container.update(
                                label="✅ Research complete!",
                                state="complete"
                            )

                        answer = result["output"]
                        
                        # Display the answer
                        st.markdown("---")
                        st.markdown(answer)

                        # Download button
                        st.download_button(
                            "📄 Download as Markdown",
                            answer,
                            file_name="research_answer.md"
                        )

                st.session_state.messages.append(
                    {"role": "assistant", "content": answer}
                )

            except Exception as e:
                with left:
                    with st.chat_message("assistant"):
                        st.error(f"❌ Error: {str(e)}")
                        
                        if "401" in str(e) or "API key" in str(e):
                            st.warning("💡 Your API key might be invalid. Get a new one from console.groq.com")
                        elif "rate limit" in str(e).lower():
                            st.warning("💡 Rate limit reached. Wait a moment and try again.")
                        else:
                            st.info("💡 Try Demo Mode to see how the app works!")
                        
                        st.session_state.messages.append(
                            {"role": "assistant", "content": f"Error: {str(e)}"}
                        )

# Footer
st.markdown("---")
st.markdown(
    '<div style="text-align: center; color: #94a3b8;">Made with ❤️ for the Research Community | Powered by Groq AI</div>',
    unsafe_allow_html=True
)
