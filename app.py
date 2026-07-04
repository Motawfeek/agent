"""
Multi-Tool AI Agent — Streamlit UI
Run: streamlit run app.py
"""
import os
import datetime

import streamlit as st
from dotenv import load_dotenv

from agent.core import create_agent_executor
from config.settings import GROQ_MODELS, DEFAULT_MODEL

load_dotenv()

# ─── Page config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Multi-Tool AI Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CSS ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .banner {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem 2rem;
        border-radius: 14px;
        text-align: center;
        margin-bottom: 1.2rem;
        box-shadow: 0 4px 20px rgba(102,126,234,0.4);
    }
    .banner h1 { color: white; font-size: 1.85rem; margin: 0; font-weight: 700; letter-spacing: -0.5px; }
    .banner p  { color: #ddd7f5; margin: 0.35rem 0 0; font-size: 0.85rem; }

    .chip {
        display: inline-block;
        background: rgba(118,75,162,0.1);
        color: #764ba2;
        border: 1px solid rgba(118,75,162,0.4);
        padding: 1px 10px;
        border-radius: 20px;
        font-size: 0.72rem;
        margin: 2px;
        font-weight: 600;
    }

    .stat-box {
        background: #f8f4ff;
        border: 1px solid #e8e0f5;
        border-radius: 10px;
        padding: 0.55rem 0.8rem;
        text-align: center;
    }
    .stat-box .num  { font-size: 1.4rem; font-weight: 700; color: #764ba2; line-height: 1.2; }
    .stat-box .lbl  { font-size: 0.65rem; color: #999; text-transform: uppercase; letter-spacing: 0.5px; }

    .step-box {
        background: #f6f0ff;
        border-left: 3px solid #764ba2;
        padding: 0.5rem 1rem;
        margin: 0.25rem 0;
        border-radius: 0 8px 8px 0;
    }

    footer { visibility: hidden; }
    #MainMenu { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Settings")
    st.divider()

    api_key = st.text_input(
        "🔑 Groq API Key",
        value=os.getenv("GROQ_API_KEY", ""),
        type="password",
        placeholder="gsk_...",
        help="Free key at console.groq.com",
    )

    model = st.selectbox("🧠 Model", GROQ_MODELS, index=0)

    temperature = st.slider(
        "🎯 Creativity",
        min_value=0.0, max_value=1.0,
        value=0.7, step=0.05,
        help="0 = precise | 1 = creative",
    )

    max_steps = st.number_input(
        "🔄 Max Tool Steps",
        min_value=3, max_value=12,
        value=7,
        help="How many tool calls the agent can make per question",
    )

    st.divider()
    st.markdown("### 🛠️ Tools (7)")
    st.markdown("""
- 🔍 **web_search** — DuckDuckGo live search
- 🧮 **calculator** — Math + functions
- 🌤️ **weather** — Real-time weather
- 📖 **wikipedia** — Facts & knowledge
- 🕐 **datetime** — Current date/time
- 💱 **currency** — Live exchange rates
- 🐍 **python_repl** — Run Python code
    """)

    st.divider()

    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("🗑️ Clear", use_container_width=True):
            st.session_state.messages = []
            st.session_state.agent = None
            st.rerun()

    with col_b:
        if st.session_state.get("messages"):
            chat_lines = []
            for m in st.session_state.messages:
                prefix = "You" if m["role"] == "user" else "Agent"
                tools_note = f" [tools: {', '.join(m['tools_used'])}]" if m.get("tools_used") else ""
                chat_lines.append(f"{prefix}{tools_note}:\n{m['content']}")
            chat_export = "\n\n---\n\n".join(chat_lines)
            ts = datetime.datetime.now().strftime("%Y%m%d_%H%M")
            st.download_button(
                "💾 Export",
                chat_export,
                file_name=f"agent_chat_{ts}.txt",
                mime="text/plain",
                use_container_width=True,
            )
        else:
            st.button("💾 Export", disabled=True, use_container_width=True)

    st.markdown(
        "<div style='text-align:center;color:#bbb;font-size:0.7rem;margin-top:1.2rem'>"
        "Built by <b>Motawfeek</b> 🚀<br>LangChain · Groq · Streamlit"
        "</div>",
        unsafe_allow_html=True,
    )

# ─── Banner ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="banner">
    <h1>🤖 Multi-Tool AI Agent</h1>
    <p>7 Tools &nbsp;|&nbsp; Groq ⚡ &nbsp;|&nbsp;
       Search · Math · Weather · Currency · DateTime · Wikipedia · Python REPL</p>
</div>
""", unsafe_allow_html=True)

# ─── Session state ────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "agent" not in st.session_state:
    st.session_state.agent = None

# ─── Agent (re)init on settings change ───────────────────────────────────────
_cfg_key = (api_key, model, temperature, int(max_steps))
if api_key and st.session_state.get("_cfg") != _cfg_key:
    with st.spinner(f"Loading **{model}**…"):
        try:
            st.session_state.agent = create_agent_executor(
                api_key=api_key,
                model=model,
                temperature=temperature,
                max_iterations=int(max_steps),
            )
            st.session_state._cfg = _cfg_key
        except Exception as exc:
            st.error(f"Failed to initialize agent: {exc}")
            st.session_state.agent = None

# ─── Stats bar ────────────────────────────────────────────────────────────────
if st.session_state.messages:
    user_msgs = [m for m in st.session_state.messages if m["role"] == "user"]
    all_tools_used = [t for m in st.session_state.messages for t in m.get("tools_used", [])]
    top_tool = max(set(all_tools_used), key=all_tools_used.count) if all_tools_used else "—"

    c1, c2, c3, c4 = st.columns(4)
    for col, num, label in [
        (c1, len(user_msgs), "Questions"),
        (c2, len(all_tools_used), "Tool Calls"),
        (c3, len(set(all_tools_used)), "Unique Tools"),
        (c4, top_tool, "Top Tool"),
    ]:
        col.markdown(
            f'<div class="stat-box"><div class="num">{num}</div>'
            f'<div class="lbl">{label}</div></div>',
            unsafe_allow_html=True,
        )
    st.write("")

# ─── Quick-action buttons ─────────────────────────────────────────────────────
if not st.session_state.messages:
    st.markdown("##### 💡 جرّب دي:")
    _examples = [
        ("🌤️ الطقس", "What's the weather in Cairo and London right now?"),
        ("💱 العملة", "How much is 1000 SAR in EGP today?"),
        ("📰 الأخبار", "What are the latest AI news this week?"),
        ("🐍 كود", "Write Python to find all prime numbers up to 50"),
    ]
    btn_cols = st.columns(4)
    for i, (label, question) in enumerate(_examples):
        if btn_cols[i].button(label, use_container_width=True, key=f"q{i}"):
            st.session_state["_quick_q"] = question
            st.rerun()

# ─── Chat history ─────────────────────────────────────────────────────────────
for msg in st.session_state.messages:
    avatar = "🧑" if msg["role"] == "user" else "🤖"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])
        if msg.get("tools_used"):
            chips = "".join(f'<span class="chip">{t}</span>' for t in msg["tools_used"])
            st.markdown(f"<div style='margin-top:5px'>🛠️ {chips}</div>", unsafe_allow_html=True)

# ─── Welcome ──────────────────────────────────────────────────────────────────
if not st.session_state.messages:
    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(
            "مرحبا! 👋 أنا AI Agent مزوّد بـ **7 tools** — اسألني أي شيء:\n\n"
            "📰 أخبار | 🌤️ طقس | 💱 عملات | 🧮 حسابات | 🕐 تاريخ/وقت | 🐍 Python | 📖 ويكيبيديا\n\n"
            "اكتب سؤالك أو اختر مثال من الأعلاه ↑"
        )

# ─── Chat input ───────────────────────────────────────────────────────────────
_quick_q = st.session_state.pop("_quick_q", None)

if not api_key:
    st.info("👈 ضع **Groq API key** في الـ sidebar — مجاني من [console.groq.com](https://console.groq.com)")
else:
    user_input = st.chat_input("اسألني أي شيء…") or _quick_q

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user", avatar="🧑"):
            st.markdown(user_input)

        with st.chat_message("assistant", avatar="🤖"):
            if not st.session_state.agent:
                st.error("Agent not initialized. Check your API key.")
            else:
                with st.spinner("جاري التفكير…"):
                    try:
                        result = st.session_state.agent.invoke({"input": user_input})
                        answer = result["output"]
                        steps = result.get("intermediate_steps", [])
                        tools_used = list({s[0].tool for s in steps}) if steps else []

                        st.markdown(answer)

                        if tools_used:
                            chips = "".join(f'<span class="chip">{t}</span>' for t in tools_used)
                            st.markdown(
                                f"<div style='margin-top:5px'>🛠️ {chips}</div>",
                                unsafe_allow_html=True,
                            )

                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": answer,
                            "tools_used": tools_used,
                        })

                        if steps:
                            with st.expander("🔍 خطوات التفكير"):
                                for i, (action, obs) in enumerate(steps, 1):
                                    obs_str = str(obs)
                                    st.markdown(
                                        f'<div class="step-box">'
                                        f"<b>خطوة {i} — <code>{action.tool}</code></b><br>"
                                        f"<small>الإدخال: {action.tool_input}</small></div>",
                                        unsafe_allow_html=True,
                                    )
                                    if len(obs_str) > 30:
                                        st.code(
                                            obs_str[:800] + ("…" if len(obs_str) > 800 else ""),
                                            language="text",
                                        )

                    except Exception as exc:
                        err_msg = f"حصل خطأ: {exc}"
                        st.error(err_msg)
                        st.session_state.messages.append({"role": "assistant", "content": err_msg})
