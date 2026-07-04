"""Current date and time tool — useful when the agent needs to know today's date."""
from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from langchain_core.tools import Tool

# أشهر المدن — بحطها هنا عشان الـ LLM أحياناً بيكتب "Cairo" مش "Africa/Cairo"
_ALIASES = {
    "cairo": "Africa/Cairo",
    "egypt": "Africa/Cairo",
    "london": "Europe/London",
    "paris": "Europe/Paris",
    "new york": "America/New_York",
    "dubai": "Asia/Dubai",
    "riyadh": "Asia/Riyadh",
    "mecca": "Asia/Riyadh",
    "beijing": "Asia/Shanghai",
    "tokyo": "Asia/Tokyo",
    "utc": "UTC",
}


def get_datetime(location: str = "Cairo") -> str:
    tz_name = _ALIASES.get(location.strip().lower(), location.strip())

    try:
        tz = ZoneInfo(tz_name)
    except (ZoneInfoNotFoundError, KeyError):
        # fallback — لو مش لاقي الـ timezone بستخدم UTC
        tz = ZoneInfo("UTC")
        tz_name = "UTC (timezone not found)"

    now = datetime.now(tz)
    offset = now.strftime("%z")
    offset_fmt = f"UTC{offset[:3]}:{offset[3:]}" if offset else "UTC"

    return (
        f"Current date & time ({tz_name}):\n"
        f"  Date    : {now.strftime('%A, %d %B %Y')}\n"
        f"  Time    : {now.strftime('%I:%M:%S %p')}\n"
        f"  Offset  : {offset_fmt}"
    )


datetime_tool = Tool(
    name="datetime",
    func=get_datetime,
    description=(
        "Get the current date and time for any city or timezone. "
        "Input: city name like 'Cairo', 'London', 'Dubai', or IANA timezone like 'America/New_York'."
    ),
)
