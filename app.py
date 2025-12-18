import streamlit as st
import time
from datetime import datetime
import json

from langchain_groq import ChatGroq
from langchain_community.utilities import ArxivAPIWrapper, WikipediaAPIWrapper
from langchain_community.tools import ArxivQueryRun, WikipediaQueryRun, DuckDuckGoSearchRun
from langchain.agents import create_openai_tools_agent, AgentExecutor
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="AI Research Mentor",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# GLOBAL STYLES
# =========================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

body {
    font-family: 'Inter', sans-serif;
    background: linear-gradient(135deg,#0f0c29,#302b63,#24243e);
}

.main-title {
    font-size: 3.3rem;
    font-weight: 900;
    text-align: center;
    background: linear-gradient(90deg,#667eea,#764ba2,#f093fb,#4facfe);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.subtitle {
    text-align: center;
    color: #cbd5e1;
    font-size: 1.1rem;
    margin-bottom: 2rem;
}
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.markdown('<div class="main-title">🧠 AI Research Mentor</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Think Better • Ask Better • Research Faster</div>',
    unsafe_allow_html=True
)

# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.markdown("## ⚙️ Configuration")

    demo_mode = st.toggle("🧪 Demo Mode", value=True)

    api_key = st.text_input(
        "Groq API Key",
        type="password",
        disabled=demo_mode
    )

    model = st.selectbox(
        "Model",
        ["llama-3.3-70b-versatile", "llama-3.1-70b-versatile"],
        index=0
    )

    st.markdown("---")
    st.markdown("### 🧭 Mentor Tip")
    st.info(
        "Start broad → identify patterns → zoom into one insight.\n\n"
        "Bad questions waste compute.\nGood questions create leverage."
    )

# =========================
# LAYOUT
# =========================
left, right = st.columns([7, 3])

# =========================
# RIGHT: MENTOR UI
# =========================
with right:
    st.markdown("""
    <div style="background: rgba(102,126,234,0.18);
                padding: 1.6rem; border-radius: 14px; margin-bottom: 1rem;
                border: 1px solid rgba(102,126,234,0.35);">
        <h3>🧠 Research Mentor</h3>
        <p>
        This app doesn't fetch answers.<br>
        It <b>trains your thinking.</b>
        </p>
        <p style="font-size:0.85rem;color:#a5b4fc;">
        Ask like a researcher, not a Googler.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="background: rgba(240,147,251,0.18);
                padding: 1.6rem; border-radius: 14px; margin-bottom: 1rem;
                border: 1px solid rgba(240,147,251,0.35);">
        <h3>📌 How To Win With This</h3>
        <ol style="font-size:0.9rem;">
            <li>Ask a high-level question</li>
            <li>Scan synthesized insights</li>
            <li>Identify one weak point</li>
            <li>Re-ask, but sharper</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="background: rgba(16,185,129,0.18);
                padding: 1.6rem; border-radius: 14px; margin-bottom: 1rem;
                border: 1px solid rgba(16,185,129,0.35);">
        <h3>❓ Question Framework</h3>
        <ul style="font-size:0.85rem;">
            <li>What exists today?</li>
            <li>What changed recently?</li>
            <li>Why does it matter?</li>
            <li>What still doesn’t work?</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    if "messages" in st.session_state:
        q = len([m for m in st.session_state.messages if m["role"] == "user"])
        st.markdown(f"""
        <div style="background: rgba(168,85,247,0.18);
                    padding: 1.6rem; border-radius: 14px; text-align:center;
                    border: 1px solid rgba(168,85,247,0.35);">
            <div style="font-size:2.4rem;font-weight:800;">{q}</div>
            <div style="font-size:0.8rem;">QUESTIONS EXPLORED</div>
        </div>
        """, unsafe_allow_html=True)

# =========================
# CHAT STATE
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": (
            "👋 **Welcome.**\n\n"
            "I’m your research mentor.\n\n"
            "If you don’t know what to ask, start with:\n"
            "- *What are the latest breakthroughs in X?*\n"
            "- *What problems remain unsolved?*\n"
            "- *Why is progress slow?*\n\n"
            "Ask your first question."
        )
    }]

# =========================
# CHAT UI
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

        with st.chat_message("assistant"):
            if demo_mode:
                st.info("🔍 Researching across multiple sources…")
                time.sleep(1)

                demo_answer = f"""
## 🧠 Synthesized Insight

**Question:** {user_query}

### What Exists
Current research shows steady progress, but most solutions optimize symptoms—not root causes.

### What Changed Recently
Recent papers indicate better scaling, but new bottlenecks emerged around cost and reliability.

### Why It Matters
This gap defines where innovation and funding will concentrate next.

### What’s Still Broken
- Scalability
- Real-world deployment
- Long-term validation

### Mentor Takeaway
> The opportunity isn’t improving what works — it’s fixing what fails quietly.
"""
                st.markdown(demo_answer)
                st.session_state.messages.append(
                    {"role": "assistant", "content": demo_answer}
                )
            else:
                if not api_key:
                    st.error("Add Groq API key or enable Demo Mode.")
                else:
                    arxiv = ArxivQueryRun(
                        api_wrapper=ArxivAPIWrapper(top_k_results=1)
                    )
                    wiki = WikipediaQueryRun(
                        api_wrapper=WikipediaAPIWrapper(top_k_results=1)
                    )
                    search = DuckDuckGoSearchRun()

                    llm = ChatGroq(
                        groq_api_key=api_key,
                        model_name=model,
                        temperature=0.5
                    )

                    prompt = ChatPromptTemplate.from_messages([
                        ("system",
                         "You are a research mentor. "
                         "Synthesize insights, highlight gaps, "
                         "and guide the user’s thinking."),
                        ("human", "{input}"),
                        MessagesPlaceholder(variable_name="agent_scratchpad")
                    ])

                    agent = create_openai_tools_agent(
                        llm, [arxiv, wiki, search], prompt
                    )

                    executor = AgentExecutor(
                        agent=agent,
                        tools=[arxiv, wiki, search],
                        verbose=False
                    )

                    result = executor.invoke({"input": user_query})
                    st.markdown(result["output"])
                    st.session_state.messages.append(
                        {"role": "assistant", "content": result["output"]}
                    )

# =========================
# FOOTER
# =========================
st.markdown("---")
st.markdown(
    "<center style='font-size:0.85rem;color:#94a3b8;'>"
    "Built for Hackathons • Powered by Groq • Designed to Teach Thinking"
    "</center>",
    unsafe_allow_html=True
)
