"""Tools package for the AI agent."""
from .search import search_tool
from .calculator import calculator_tool
from .weather import weather_tool
from .wikipedia_tool import wikipedia_tool


def get_all_tools():
    """Return a list of all available agent tools."""
    return [
        search_tool,
        calculator_tool,
        weather_tool,
        wikipedia_tool,
    ]


__all__ = ["get_all_tools", "search_tool", "calculator_tool", "weather_tool", "wikipedia_tool"]
