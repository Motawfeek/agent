<div align="center">

# Multi-Tool AI Agent

**LangChain · Groq · Streamlit — 7 tools, zero paid APIs**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![LangChain](https://img.shields.io/badge/LangChain-1.x-1C3C3C?style=flat-square)](https://langchain.com)
[![Groq](https://img.shields.io/badge/Groq-Llama_3.3_70B-F55036?style=flat-square)](https://groq.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.58-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-22c55e?style=flat-square)](LICENSE)

</div>

---

## What is this?

An AI agent that uses the **ReAct (Reasoning + Acting)** framework to answer questions by calling
the right tool at the right time — web search, calculations, live weather, currency conversions,
and even executing Python code — all in one chat interface.

I built it to understand how LLM agents actually *think* and *act*, not just generate text.
The result turned out useful enough that I turned it into a full project.

---

## Tools (7)

| Tool | What it does | API Key? |
|------|-------------|---------|
| 🔍 `web_search` | Live DuckDuckGo search | No |
| 🧮 `calculator` | Math — `sqrt`, `sin`, `log`, `factorial`… | No |
| 🌤️ `weather` | Real-time conditions for any city | No |
| 📖 `wikipedia` | Facts, history, science | No |
| 🕐 `datetime` | Current date & time in any timezone | No |
| 💱 `currency` | Live exchange rates — 170+ currencies incl. EGP, SAR, AED | No |
| 🐍 `python_repl` | Safe Python sandbox — runs code, returns output | No |

All 7 tools are **completely free** — no API keys, no credit cards.

---

## How the agent thinks

```
User: "What's 1000 SAR in EGP, and what time is it in Riyadh?"

Agent thought process:
  Thought → I need currency rates AND time for two different things
  Action  → currency("1000 SAR to EGP")
  Observe → 1000 SAR = 10,847 EGP
  Action  → datetime("Riyadh")
  Observe → Sunday, 05 July 2026 at 12:53 AM (UTC+03:00)
  Thought → I have everything I need
  Answer  → "1000 SAR equals approximately 10,847 EGP.
              It is currently 12:53 AM in Riyadh (UTC+03:00)."
```

Every step is visible in the **"خطوات التفكير"** expander in the UI.

---

## Quick start

```bash
git clone https://github.com/Motawfeek/multi-tool-ai-agent.git
cd multi-tool-ai-agent
pip install -r requirements.txt
cp .env.example .env        # add your free Groq key
streamlit run app.py
```

Get a free Groq key at [console.groq.com](https://console.groq.com) — takes 30 seconds.

---

## Project structure

```
agent/
├── app.py                    # Streamlit UI (stats, export, quick actions)
├── main.py                   # CLI interface
│
├── agent/
│   ├── core.py               # AgentExecutor with adjustable temperature & steps
│   └── tools/
│       ├── search.py         # DuckDuckGo
│       ├── calculator.py     # Safe math eval
│       ├── weather.py        # wttr.in
│       ├── wikipedia_tool.py # Wikipedia API
│       ├── datetime_tool.py  # zoneinfo-based datetime
│       ├── currency_tool.py  # fawazahmed0 currency API
│       └── code_tool.py      # Python sandbox
│
└── config/settings.py        # Models list, defaults
```

---

## UI features

- **4 quick-action buttons** — one click to try weather, currency, news, or code
- **Session stats** — question count, tool calls, most-used tool
- **Reasoning trace** — expand to see every step the agent took
- **Export chat** — download the full conversation as `.txt`
- **Adjustable creativity** — slider from 0 (precise) to 1 (creative)
- **Model switcher** — Llama 3.3 70B, 8B, Mixtral, Gemma 2

---

## Stack

| Layer | Technology |
|-------|-----------|
| Agent framework | LangChain (ReAct) + langchain-classic |
| LLM inference | [Groq](https://groq.com) — fastest inference available |
| Language model | Llama 3.3 70B by Meta |
| Web interface | Streamlit |
| Search | DuckDuckGo (via ddgs) |
| Weather | [wttr.in](https://wttr.in) |
| Currency | [fawazahmed0 currency API](https://github.com/fawazahmed0/exchange-api) |

---

## Things I learned building this

- LangChain 1.x moved `AgentExecutor` to `langchain-classic` — the migration guide is sparse
- Groq deprecated several models mid-development (llama3-70b-8192 is gone)
- The ReAct prompt needs explicit "you can answer directly without a tool" instructions, otherwise the agent loops
- DuckDuckGo changed its internal API and now requires the `ddgs` package separately
- Streamlit hot-reload doesn't re-run `load_dotenv()` in the same process — restart required when `.env` changes

---

## Contributing

Open to PRs. Ideas:
- Streaming responses (challenging with AgentExecutor + Streamlit)
- Persistent memory across sessions
- Image generation tool
- Email / calendar integration

---

<div align="center">

Made by **Motawfeek** — [GitHub](https://github.com/Motawfeek)

⭐ Star if useful!

</div>
