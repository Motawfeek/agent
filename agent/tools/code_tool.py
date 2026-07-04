"""Safe Python REPL — runs code in a restricted sandbox, no file system or network access."""
import io
import math
import json
import statistics
from langchain_core.tools import Tool


def run_python(code: str) -> str:
    """Execute Python code safely and return stdout output."""

    # بحدد الـ builtins المسموح بيها بس — مش هنفتح باب الـ __import__ أو os
    stdout_buf = io.StringIO()

    _safe_builtins = {
        "print": lambda *a, **kw: print(*a, **kw, file=stdout_buf),
        # Types
        "int": int, "float": float, "str": str, "bool": bool,
        "list": list, "dict": dict, "tuple": tuple, "set": set,
        "bytes": bytes,
        # Built-in funcs
        "len": len, "range": range, "enumerate": enumerate,
        "zip": zip, "map": map, "filter": filter,
        "sorted": sorted, "reversed": reversed,
        "sum": sum, "min": min, "max": max,
        "abs": abs, "round": round, "pow": pow, "divmod": divmod,
        "all": all, "any": any,
        "type": type, "isinstance": isinstance, "issubclass": issubclass,
        "repr": repr, "format": format, "hash": hash,
        "chr": chr, "ord": ord, "hex": hex, "oct": oct, "bin": bin,
        # Exceptions
        "ValueError": ValueError, "TypeError": TypeError,
        "IndexError": IndexError, "KeyError": KeyError,
        "Exception": Exception, "StopIteration": StopIteration,
        # Built-in constants
        "True": True, "False": False, "None": None,
    }

    _globals = {
        "__builtins__": _safe_builtins,
        "math": math,
        "json": json,
        "statistics": statistics,
    }

    try:
        compiled = compile(code, "<sandbox>", "exec")
        exec(compiled, _globals)  # noqa: S102
        result = stdout_buf.getvalue().strip()
        return result if result else "✅ Code ran successfully (no output)"
    except SyntaxError as e:
        return f"❌ Syntax error on line {e.lineno}: {e.msg}"
    except Exception as e:
        return f"❌ {type(e).__name__}: {e}"


code_tool = Tool(
    name="python_repl",
    func=run_python,
    description=(
        "Execute Python code in a safe sandbox and return the output. "
        "Perfect for data processing, list operations, sorting, string manipulation, and algorithms. "
        "Has access to: math, json, statistics modules. "
        "Always use print() to display results. "
        "Example: 'nums = [3,1,4,1,5,9,2,6]\\nprint(sorted(nums))\\nprint(sum(nums)/len(nums))'"
    ),
)
