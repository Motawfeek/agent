"""Web search tool using DuckDuckGo (no API key required)."""
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.tools import Tool

_ddg = DuckDuckGoSearchRun()

search_tool = Tool(
    name="web_search",
    func=_ddg.run,
    description=(
        "Search the internet for current, up-to-date information. "
        "Use this for news, recent events, prices, or any information "
        "that may have changed recently. "
        "Input: a search query string."
    ),
)
