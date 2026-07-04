<div align="center">

# 🤖 Multi-Tool AI Agent

**A production-ready AI agent powered by Groq ⚡ and LangChain**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![LangChain](https://img.shields.io/badge/LangChain-0.2+-1C3C3C?style=for-the-badge&logo=chainlink&logoColor=white)](https://langchain.com)
[![Groq](https://img.shields.io/badge/Groq-Llama3_70B-F55036?style=for-the-badge&logo=groq&logoColor=white)](https://groq.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-Web_UI-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge)](LICENSE)

[Features](#-features) · [Quick Start](#-quick-start) · [Architecture](#-architecture) · [Examples](#-example-queries)

</div>

---

## 🌟 Overview

A fully-functional, multi-tool AI agent built with **LangChain** and **Groq's ultra-fast LLM inference** (Llama 3 70B). The agent uses the **ReAct (Reasoning + Acting)** framework to intelligently decide *which tool to use* and *how many steps* it needs to answer any question accurately.

Ships with both a **beautiful Streamlit web interface** and a **terminal CLI** — ready to deploy or extend.

---

## ✨ Features

| Capability | Description |
|------------|-------------|
| 🔍 **Web Search** | Real-time internet search via DuckDuckGo — no API key needed |
| 🧮 **Calculator** | Safe math evaluation with `sqrt`, `sin`, `log`, `factorial`, and more |
| 🌤️ **Weather** | Live weather data for any city worldwide (temperature, humidity, wind) |
| 📖 **Wikipedia** | Instant access to a vast factual knowledge base |
| ⚡ **Groq Inference** | Up to 800 tokens/sec with Llama 3 70B, Mixtral, or Gemma 2 |
| 🧠 **ReAct Agent** | Multi-step reasoning with transparent tool selection |
| 💬 **Streamlit UI** | Chat interface with collapsible reasoning trace |
| 🖥️ **CLI Mode** | Terminal interface for quick, scriptable interactions |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    User Interfaces                       │
│         Streamlit Web App (app.py) │ CLI (main.py)      │
└──────────────────────┬──────────────────────────────────┘
                       │ question
┌──────────────────────▼──────────────────────────────────┐
│             LangChain ReAct AgentExecutor                │
│         Reason → Act → Observe → Repeat → Answer        │
└────┬──────────┬──────────────┬──────────────┬───────────┘
     │          │              │              │
┌────▼───┐ ┌───▼──────┐ ┌────▼──────┐ ┌────▼──────┐
│  Web   │ │Calculator│ │  Weather  │ │ Wikipedia │
│ Search │ │  (math)  │ │ (wttr.in) │ │  (facts)  │
└────────┘ └──────────┘ └───────────┘ └───────────┘
                       │ LLM calls
┌──────────────────────▼──────────────────────────────────┐
│               Groq — Ultra-Fast Inference ⚡             │
│    Llama 3 70B │ Llama 3 8B │ Mixtral 8x7B │ Gemma 2   │
└─────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/multi-tool-ai-agent.git
cd multi-tool-ai-agent
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure your API key
```bash
cp .env.example .env
# Open .env and paste your Groq API key
```

### 4. Launch the web UI
```bash
streamlit run app.py
```

Or use the CLI directly:
```bash
python main.py
```

> **Get a free Groq API key** at [console.groq.com](https://console.groq.com) — no credit card required.

---

## 💡 Example Queries

```
🔍  "What are the latest developments in AI this week?"
🌤️  "What's the weather in Cairo and should I take an umbrella?"
🧮  "What is the compound interest on $5,000 at 7% for 15 years?"
📖  "Explain quantum computing in simple terms"
🌐  "Search for the top 5 Python libraries for machine learning"
🔀  "What is the weather in London and convert 22°C to Fahrenheit?"
```

---

## 📁 Project Structure

```
multi-tool-ai-agent/
│
├── app.py                  # 🌐 Streamlit web interface
├── main.py                 # 🖥️  CLI interface
├── requirements.txt        # 📦 Python dependencies
├── .env.example            # 🔑 Environment variable template
│
├── agent/
│   ├── __init__.py
│   ├── core.py             # 🧠 AgentExecutor setup (ReAct + Groq)
│   └── tools/
│       ├── __init__.py
│       ├── search.py       # 🔍 DuckDuckGo web search
│       ├── calculator.py   # 🧮 Safe math evaluator
│       ├── weather.py      # 🌤️  wttr.in weather API
│       └── wikipedia_tool.py  # 📖 Wikipedia lookups
│
└── config/
    ├── __init__.py
    └── settings.py         # ⚙️  Model list & constants
```

---

## 🧠 How ReAct Works

The agent follows a **Reasoning + Acting** loop:

```
User question
     ↓
[Thought]  → "I need to search the web for current information"
[Action]   → web_search("...")
[Observe]  → "<search results>"
[Thought]  → "Now I can calculate the answer"
[Action]   → calculator("...")
[Observe]  → "result"
[Thought]  → "I have everything I need"
[Final Answer] → Clear, complete response
```

Every reasoning step is visible in the **"Agent reasoning steps"** expander in the web UI.

---

## 📊 Model Comparison

| Model | Speed | Context Window | Best For |
|-------|-------|---------------|----------|
| `llama3-70b-8192` | ⚡⚡⚡ | 8K tokens | Best quality (recommended) |
| `llama3-8b-8192` | ⚡⚡⚡⚡ | 8K tokens | Fastest responses |
| `mixtral-8x7b-32768` | ⚡⚡⚡ | 32K tokens | Long context tasks |
| `gemma2-9b-it` | ⚡⚡⚡ | 8K tokens | Balanced performance |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| LLM Inference | [Groq](https://groq.com) — world's fastest AI inference |
| Agent Framework | [LangChain](https://langchain.com) ReAct agent |
| Language Model | [Llama 3 70B](https://ai.meta.com/llama/) by Meta |
| Web Interface | [Streamlit](https://streamlit.io) |
| Web Search | [DuckDuckGo](https://duckduckgo.com) (no API key needed) |
| Weather Data | [wttr.in](https://wttr.in) (no API key needed) |
| Knowledge Base | [Wikipedia](https://wikipedia.org) |

---

## 🤝 Contributing

Contributions are welcome! Ideas for extension:

- 🐍 **Python REPL** — execute code snippets
- 📧 **Email tool** — send/read emails
- 🗄️ **Database tool** — query SQL databases
- 🖼️ **Image generation** — DALL·E / Stable Diffusion
- 🔔 **Memory** — persistent conversation history
- 🌍 **Multi-language** — internationalization support

---

## 📝 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for details.

---

<div align="center">

Made with ❤️ using Python, LangChain, and Groq

**⭐ Star this repo if you found it useful!**

</div>
