"""Core AI agent — builds the LangChain ReAct AgentExecutor."""
from langchain_groq import ChatGroq
from langchain.agents import create_react_agent, AgentExecutor
from langchain.prompts import PromptTemplate

from .tools import get_all_tools

# ---------------------------------------------------------------------------
# ReAct prompt (local copy — no hub.pull dependency)
# Variables required by create_react_agent: {tools}, {tool_names}, {input},
# {agent_scratchpad}
# ---------------------------------------------------------------------------
_REACT_TEMPLATE = """You are a helpful and knowledgeable AI assistant with access to the following tools:

{tools}

Use the following format strictly:

Question: the input question you must answer
Thought: think step-by-step about what to do and whether a tool is needed
Action: the action to take, must be exactly one of [{tool_names}]
Action Input: the exact input to pass to the tool
Observation: the result returned by the tool
... (you may repeat Thought/Action/Action Input/Observation as many times as needed)
Thought: I now have enough information to give a final answer
Final Answer: a clear, complete, and helpful answer to the original question

Rules:
- Always use a tool when you need current data, calculations, or factual information.
- Provide a "Final Answer" at the end without fail.
- Do not make up information — use tools instead.

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
