"""Tools package for the AI agent."""
from .search import search_tool
from .calculator import calculator_tool
from .weather import weather_tool
from .wikipedia_tool import wikipedia_tool
from .datetime_tool import datetime_tool
from .currency_tool import currency_tool
from .code_tool import code_tool


def get_all_tools():
    """Return all 7 agent tools."""
    return [
        search_tool,
        calculator_tool,
        weather_tool,
        wikipedia_tool,
        datetime_tool,
        currency_tool,
        code_tool,
    ]


__all__ = [
    "get_all_tools",
    "search_tool", "calculator_tool", "weather_tool",
    "wikipedia_tool", "datetime_tool", "currency_tool", "code_tool",
]
