import streamlit as st
import time
from langchain_groq import ChatGroq
from langchain_community.utilities import ArxivAPIWrapper, WikipediaAPIWrapper
from langchain_community.tools import ArxivQueryRun, WikipediaQueryRun, DuckDuckGoSearchRun
from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="AI Research Copilot",
    page_icon="🚀",
    layout="wide"
)

# =========================
# SIMPLE PREMIUM CSS (YOUR ORIGINAL)
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
# HEADER (YOUR ORIGINAL)
# =========================
st.markdown('<div class="main-title">🚀 AI Research Copilot</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Ask once. Get verified answers with citations from ArXiv, Wikipedia & Web.</div>',
    unsafe_allow_html=True
)

# =========================
# SIDEBAR (YOUR ORIGINAL)
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

# =========================
# LAYOUT (YOUR ORIGINAL + FIXED RIGHT SIDEBAR)
# =========================
left, right = st.columns([7, 3])

with right:
    # Card 1 - FIXED to be visible
    st.markdown('<div class="card"><b>Perfect For</b><br>🎓 Students<br>🔬 Researchers<br>👨‍💻 Developers</div>', unsafe_allow_html=True)
    
    # Card 2 - FIXED to be visible
    st.markdown('<div class="card"><b>Key Advantage</b><br>Not just answers — verified synthesis.</div>', unsafe_allow_html=True)

# =========================
# CHAT STATE (YOUR ORIGINAL)
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Ask a research question. I'll verify it across multiple sources and cite them."
        }
    ]

# =========================
# DISPLAY CHAT (YOUR ORIGINAL)
# =========================
with left:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_query = st.chat_input("Ask a research question…")

# =========================
# HANDLE QUERY (YOUR ORIGINAL LOGIC + WORKING AGENT)
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
                    time.sleep(1)

                demo_answer = """
### Answer
Quantum Computing uses qubits that leverage **superposition** and **entanglement** to perform certain computations exponentially faster than classical computers.

### Sources
- **[ArXiv]** Preskill, *Quantum Computing in the NISQ era*
- **[Wikipedia]** Quantum Computing
- **[Web]** IBM Quantum Research
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
    # REAL MODE - WORKING VERSION
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
                        with st.spinner("Researching across sources…"):
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
                                temperature=0.6
                            )

                            # Create prompt - NO EMOJIS (fixes encoding issue)
                            prompt = ChatPromptTemplate.from_messages([
                                ("system", """You are a research assistant.

Rules:
- Always verify information.
- Always cite sources.
- Never hallucinate.
- End with a Sources section.

Format:

### Answer
<clear structured explanation>

### Sources
- [ArXiv]
- [Wikipedia]
- [Web]"""),
                                MessagesPlaceholder(variable_name="chat_history", optional=True),
                                ("human", "{input}"),
                                MessagesPlaceholder(variable_name="agent_scratchpad")
                            ])

                            # Create agent
                            agent = create_openai_tools_agent(llm, tools, prompt)
                            executor = AgentExecutor(
                                agent=agent, 
                                tools=tools,
                                verbose=False,
                                handle_parsing_errors=True,
                                max_iterations=8
                            )

                            # Execute
                            result = executor.invoke({"input": user_query})

                        answer = result.get("output", "No response")
                        st.markdown(answer)

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
                        st.error(f"Error: {str(e)}")
                        if "401" in str(e):
                            st.info("Invalid API key. Get one from console.groq.com")
