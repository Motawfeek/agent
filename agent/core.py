"""Core AI agent — builds the LangChain ReAct AgentExecutor."""
from langchain_groq import ChatGroq
from langchain_classic.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate

from .tools import get_all_tools

# ---------------------------------------------------------------------------
# ReAct prompt (local copy — no hub.pull dependency)
# Variables required by create_react_agent: {tools}, {tool_names}, {input},
# {agent_scratchpad}
# ---------------------------------------------------------------------------
_REACT_TEMPLATE = """You are a helpful AI assistant. Answer the user's question directly if you already know the answer. Only use tools when you need real-time data (weather, news), calculations, or factual lookups.

You have access to these tools:
{tools}

STRICT FORMAT — follow exactly:

Question: the input question
Thought: reasoning about whether a tool is needed or if I can answer directly
Action: tool name — must be one of [{tool_names}]
Action Input: input for the tool
Observation: tool result
(repeat Thought/Action/Action Input/Observation if needed)
Thought: I have enough information now
Final Answer: the complete answer

OR if no tool is needed:

Question: the input question
Thought: I can answer this directly without any tool.
Final Answer: the complete answer

IMPORTANT: Always end with "Final Answer:" — never stop without it.

Begin!

Question: {input}
Thought:{agent_scratchpad}"""


def create_agent_executor(api_key: str, model: str = "llama3-70b-8192") -> AgentExecutor:
    """
    Create and return a configured LangChain AgentExecutor.

    Args:
        api_key: Groq API key (get one free at console.groq.com)
        model:   Groq model name

    Returns:
        AgentExecutor ready to process queries via .invoke({"input": "..."})
    """
    llm = ChatGroq(
        groq_api_key=api_key,
        model_name=model,
        temperature=0.7,
        max_tokens=2048,
    )

    tools = get_all_tools()
    prompt = PromptTemplate.from_template(_REACT_TEMPLATE)
    agent = create_react_agent(llm, tools, prompt)

    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=7,
        return_intermediate_steps=True,
    )
