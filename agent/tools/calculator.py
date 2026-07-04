"""Safe calculator tool for mathematical operations."""
import math
from langchain_core.tools import Tool


def safe_calculate(expression: str) -> str:
    """
    Safely evaluate a mathematical expression using a restricted namespace.
    Supports basic arithmetic and common math functions.
    """
    safe_globals = {
        "__builtins__": {},
        # Basic math
        "abs": abs, "round": round, "pow": pow,
        # Math module functions
        "sqrt": math.sqrt, "log": math.log, "log10": math.log10,
        "log2": math.log2, "exp": math.exp,
        "sin": math.sin, "cos": math.cos, "tan": math.tan,
        "asin": math.asin, "acos": math.acos, "atan": math.atan,
        "ceil": math.ceil, "floor": math.floor,
        "factorial": math.factorial, "gcd": math.gcd,
        # Constants
        "pi": math.pi, "e": math.e, "inf": math.inf,
    }

    try:
        result = eval(expression, safe_globals, {})  # noqa: S307
        if isinstance(result, float):
            result = round(result, 10)
        return f"{expression} = {result}"
    except ZeroDivisionError:
        return "Error: Division by zero is not allowed."
    except Exception as exc:
        return f"Error evaluating '{expression}': {exc}"


calculator_tool = Tool(
    name="calculator",
    func=safe_calculate,
    description=(
        "Perform mathematical calculations. "
        "Supports +, -, *, /, ** (power), % (modulo), parentheses, "
        "and functions: sqrt, sin, cos, tan, log, log10, ceil, floor, factorial, pi, e. "
        "Input: a math expression, e.g. 'sqrt(144) + 3 * pi'."
    ),
)
