#!/usr/bin/env python3
"""
CLI interface for the Multi-Tool AI Agent.

Usage:
    python main.py
"""
import os
import sys

from dotenv import load_dotenv

from agent.core import create_agent_executor

load_dotenv()

BANNER = r"""
╔══════════════════════════════════════════════════════════════╗
║        🤖  Multi-Tool AI Agent  —  Powered by Groq ⚡        ║
║   Tools: Web Search | Calculator | Weather | Wikipedia       ║
╚══════════════════════════════════════════════════════════════╝
  Type your question and press Enter.
  Commands: 'clear' — reset session | 'quit' — exit
"""


def main() -> None:
    print(BANNER)

    # --- API key ---
    api_key = os.getenv("GROQ_API_KEY", "").strip()
    if not api_key:
        api_key = input("  Enter your Groq API key: ").strip()
    if not api_key:
        print("Error: A Groq API key is required. Get one free at https://console.groq.com")
        sys.exit(1)

    model = os.getenv("DEFAULT_MODEL", "llama3-70b-8192")
    print(f"  Model: {model}\n")

    # --- Initialize agent ---
    try:
        agent = create_agent_executor(api_key=api_key, model=model)
    except Exception as exc:
        print(f"Error initializing agent: {exc}")
        sys.exit(1)

    # --- Chat loop ---
    while True:
        try:
            user_input = input("\n You  → ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\nGoodbye! 👋")
            break

        if not user_input:
            continue

        if user_input.lower() in {"quit", "exit", "q"}:
            print("Goodbye! 👋")
            break

        if user_input.lower() == "clear":
            agent = create_agent_executor(api_key=api_key, model=model)
            print("  Session cleared ✓")
            continue

        try:
            result = agent.invoke({"input": user_input})
            print(f"\n 🤖 Agent → {result['output']}")

            steps = result.get("intermediate_steps", [])
            if steps:
                tools_used = [step[0].tool for step in steps]
                print(f"    └─ Tools used: {', '.join(tools_used)}")

        except Exception as exc:
            print(f"\n  Error: {exc}")


if __name__ == "__main__":
    main()
