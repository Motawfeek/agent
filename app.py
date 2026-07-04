"""
Streamlit web interface for the Multi-Tool AI Agent.

Run:
    streamlit run app.py
"""
import os

import streamlit as st
from dotenv import load_dotenv

from agent.core import create_agent_executor
from config.settings import GROQ_MODELS, DEFAULT_MODEL

load_dotenv()

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Multi-Tool AI Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Header gradient banner */
    .banner {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.6rem 2rem;
        border-radius: 14px;
        text-align: center;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 15px rgba(102,126,234,0.35);
    }
    .banner h1 { color: white; font-size: 1.9rem; margin: 0; font-weight: 700; }
    .banner p  { color: #ddd7f5; margin: 0.4rem 0 0; font-size: 0.9rem; }

    /* Tool chip badges */
    .chip {
        display: inline-block;
        background: rgba(118,75,162,0.12);
        color: #764ba2;
        border: 1px solid #764ba2;
        padding: 2px 11px;
        border-radius: 20px;
        font-size: 0.73rem;
        margin: 2px;
        font-weight: 600;
    }

    /* Reasoning step box */
    .step-box {
        background: #f6f0ff;
        border-left: 3px solid #764ba2;
        padding: 0.55rem 1rem;
        margin: 0.3rem 0;
        border-radius: 0 8px 8px 0;
        font-size: 0.83rem;
    }

    /* Hide default Streamlit footer */
    footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("⚙️ Settings")
    st.divider()

    api_key = st.text_input(
        "🔑 Groq API Key",
        value=os.getenv("GROQ_API_KEY", ""),
        type="password",
        placeholder="gsk_...",
        help="Free key at [console.groq.com](https://console.groq.com)",
    )

    model = st.selectbox(
        "🧠 Model",
        options=GROQ_MODELS,
        index=GROQ_MODELS.index(DEFAULT_MODEL),
        help="llama3-70b-8192 gives the best results",
    )

    st.divider()
    st.markdown("### 🛠️ Available Tools")
    st.markdown("""
- 🔍 **Web Search** — DuckDuckGo
- 🧮 **Calculator** — Math & functions
- 🌤️ **Weather** — Real-time data
- 📖 **Wikipedia** — Knowledge base
    """)

    st.divider()
    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.agent = None
        st.rerun()

    st.markdown(
        "<div style='text-align:center;color:#aaa;font-size:0.72rem;margin-top:1rem'>"
        "Built with LangChain + Groq ⚡</div>",
        unsafe_allow_html=True,
    )

# ── Main header ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="banner">
    <h1>🤖 Multi-Tool AI Agent</h1>
    <p>Powered by Groq ⚡ &nbsp;|&nbsp; Web Search · Calculator · Weather · Wikipedia</p>
</div>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "agent" not in st.session_state:
    st.session_state.agent = None

# ── Agent (re)initialization ──────────────────────────────────────────────────
needs_init = (
    st.session_state.agent is None
    or st.session_state.get("current_api_key") != api_key
    or st.session_state.get("current_model") != model
)

if api_key and needs_init:
    with st.spinner(f"Initializing **{model}**…"):
        try:
            st.session_state.agent = create_agent_executor(api_key=api_key, model=model)
            st.session_state.current_api_key = api_key
            st.session_state.current_model = model
        except Exception as exc:
            st.error(f"Failed to initialize agent: {exc}")
            st.session_state.agent = None

# ── Render existing chat history ──────────────────────────────────────────────
for msg in st.session_state.messages:
    avatar = "🧑" if msg["role"] == "user" else "🤖"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])
        if msg.get("tools_used"):
            chips = "".join(f'<span class="chip">{t}</span>' for t in msg["tools_used"])
            st.markdown(f"<div style='margin-top:6px'>🛠️ {chips}</div>", unsafe_allow_html=True)

# ── Welcome message (first open) ──────────────────────────────────────────────
if not st.session_state.messages:
    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(
            "Hi there! 👋 I'm your **Multi-Tool AI Agent**. I can help you with:\n\n"
            "- 🔍 **Web search** — latest news, prices, events\n"
            "- 🧮 **Calculations** — math expressions & functions\n"
            "- 🌤️ **Weather** — live conditions for any city\n"
            "- 📖 **Wikipedia** — facts, history, science\n\n"
            "Just type your question below!"
        )

# ── Chat input ────────────────────────────────────────────────────────────────
if not api_key:
    st.info(
        "👈 Enter your **Groq API key** in the sidebar to start. "
        "Get a free key at [console.groq.com](https://console.groq.com)."
    )
else:
    user_input = st.chat_input("Ask me anything…")

    if user_input:
        # Append & display user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user", avatar="🧑"):
            st.markdown(user_input)

        # Agent response
        with st.chat_message("assistant", avatar="🤖"):
            if st.session_state.agent is None:
                st.error("Agent is not initialized. Check your API key.")
            else:
                with st.spinner("Thinking…"):
                    try:
                        result = st.session_state.agent.invoke({"input": user_input})
                        answer = result["output"]
                        steps = result.get("intermediate_steps", [])
                        tools_used = list({s[0].tool for s in steps}) if steps else []

                        st.markdown(answer)

                        if tools_used:
                            chips = "".join(
                                f'<span class="chip">{t}</span>' for t in tools_used
                            )
                            st.markdown(
                                f"<div style='margin-top:6px'>🛠️ {chips}</div>",
                                unsafe_allow_html=True,
                            )

                        st.session_state.messages.append(
                            {"role": "assistant", "content": answer, "tools_used": tools_used}
                        )

                        # Collapsible reasoning trace
                        if steps:
                            with st.expander("🔍 Agent reasoning steps"):
                                for i, (action, observation) in enumerate(steps, 1):
                                    obs_str = str(observation)
                                    truncated = obs_str[:600] + ("…" if len(obs_str) > 600 else "")
                                    st.markdown(
                                        f"<div class='step-box'>"
                                        f"<b>Step {i} — <code>{action.tool}</code></b><br>"
                                        f"<b>Input:</b> {action.tool_input}</div>",
                                        unsafe_allow_html=True,
                                    )
                                    st.code(truncated, language="text")

                    except Exception as exc:
                        err = f"Sorry, I encountered an error: {exc}"
                        st.error(err)
                        st.session_state.messages.append(
                            {"role": "assistant", "content": err}
                        )
