import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.utilities import ArxivAPIWrapper, WikipediaAPIWrapper
from langchain_community.tools import ArxivQueryRun, WikipediaQueryRun, DuckDuckGoSearchRun
from langchain.agents import AgentExecutor, create_react_agent
from langchain import hub
from langchain.callbacks import StreamlitCallbackHandler
import os

# Page configuration
st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
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
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🔬 AI Research Assistant</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Powered by Groq AI, ArXiv, Wikipedia & Web Search</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
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
    
    model_choice = st.selectbox(
        "🤖 Select Model:",
        ["llama-3.3-70b-versatile", "llama-3.1-70b-versatile", "mixtral-8x7b-32768"],
        index=0
    )
    
    st.markdown("---")
    st.markdown("### 🔍 Active Sources:")
    st.markdown("- ✅ ArXiv (Research Papers)")
    st.markdown("- ✅ Wikipedia (Encyclopedia)")
    st.markdown("- ✅ Web Search (Real-time)")
    
    st.markdown("---")
    st.markdown("### 💡 Example Queries:")
    
    examples = [
        "Latest quantum computing research",
        "Explain machine learning",
        "What is LangChain?",
        "Transformer architecture",
        "Climate change findings"
    ]
    
    for example in examples:
        if st.button(f"📄 {example}", key=example, use_container_width=True):
            st.session_state.example_query = example

# Main content
col1, col2 = st.columns([2, 1])

with col2:
    st.markdown("### 📊 Features")
    st.markdown("""
    - 🔬 Research Papers
    - 📚 Wikipedia Facts
    - 🌐 Web Search
    - 🤖 AI Synthesis
    - ⚡ Fast Results
    """)

with col1:
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [{
            "role": "assistant",
            "content": "👋 Hi! I'm your AI Research Assistant. Ask me anything about research, science, or technology!"
        }]
    
    # Handle example query
    if "example_query" in st.session_state:
        prompt = st.session_state.example_query
        del st.session_state.example_query
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.rerun()
    
    # Display messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
    
    # Chat input
    if prompt := st.chat_input(
        placeholder="Ask me anything...",
        disabled=not api_key
    ):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.write(prompt)
        
        if not api_key:
            with st.chat_message("assistant"):
                st.error("❌ Please enter your Groq API key first!")
        else:
            try:
                # Initialize tools
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
                
                # Get prompt template
                try:
                    prompt_template = hub.pull("hwchase17/react")
                except:
                    # Fallback if hub doesn't work
                    from langchain.prompts import PromptTemplate
                    prompt_template = PromptTemplate.from_template(
                        """Answer the following questions as best you can. You have access to the following tools:

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
                with st.chat_message("assistant"):
                    with st.spinner("🔍 Searching..."):
                        st_callback = StreamlitCallbackHandler(
                            st.container(),
                            expand_new_thoughts=False
                        )
                        
                        response = agent_executor.invoke(
                            {"input": prompt},
                            {"callbacks": [st_callback]}
                        )
                        
                        answer = response["output"]
                        
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": answer
                        })
                        
                        st.write(answer)
                        st.success("✅ Search complete!")
                        
            except Exception as e:
                with st.chat_message("assistant"):
                    error_msg = str(e)
                    
                    if "API key" in error_msg or "401" in error_msg:
                        st.error("❌ Invalid API key. Please check your Groq API key.")
                    elif "rate limit" in error_msg.lower():
                        st.error("❌ Rate limit reached. Please wait a moment.")
                    else:
                        st.error(f"❌ Error: {error_msg}")
                    
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": f"Error: {error_msg}"
                    })

# Footer
st.markdown("---")
st.markdown("**Made with ❤️ for the Research Community** | [GitHub](https://github.com/your-repo)")
