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

    demo_mode = st.toggle("🧪 Demo Mode (No API Key)", value=True)

    api_key = st.text_input(
        "Groq API Key",
        type="password",
        disabled=demo_mode
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
# LAYOUT
# =========================
left, right = st.columns([7, 3])

with right:
    st.markdown('<div class="card"><b>Perfect For</b><br>🎓 Students<br>🔬 Researchers<br>👨‍💻 Developers</div>', unsafe_allow_html=True)
    st.markdown('<div class="card"><b>Key Advantage</b><br>Not just answers — verified synthesis.</div>', unsafe_allow_html=True)

# =========================
# CHAT STATE
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Ask a research question. I’ll verify it across multiple sources and cite them."
        }
    ]

# =========================
# DISPLAY CHAT
# =========================
with left:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_query = st.chat_input("Ask a research question…")

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
    # REAL MODE
    # -------------------------
    else:
        try:
            arxiv = ArxivQueryRun(
                api_wrapper=ArxivAPIWrapper(top_k_results=1)
            )
            wiki = WikipediaQueryRun(
                api_wrapper=WikipediaAPIWrapper(top_k_results=1)
            )
            web = DuckDuckGoSearchRun(name="WebSearch")

            tools = [arxiv, wiki, web]

            llm = ChatGroq(
                groq_api_key=api_key,
                model_name=model,
                temperature=0.6
            )

            prompt = PromptTemplate.from_template("""
You are a research assistant.

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
- [Web]

Question: {input}
{agent_scratchpad}
""")

            agent = create_react_agent(llm, tools, prompt)
            executor = AgentExecutor(agent=agent, tools=tools)

            with left:
                with st.chat_message("assistant"):
                    with st.spinner("Researching across sources…"):
                        result = executor.invoke({"input": user_query})

                    answer = result["output"]
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
                st.error(f"Error: {e}")
