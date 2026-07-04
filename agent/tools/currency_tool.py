"""Currency converter using fawazahmed0 currency API (free, no key, 170+ currencies)."""
import requests
from langchain_core.tools import Tool

_API_BASE = "https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies"
_FALLBACK  = "https://latest.currency-api.pages.dev/v1/currencies"
_SHOW_RATES = ["usd", "eur", "egp", "gbp", "sar", "aed", "try", "jpy"]


def _fetch_rates(from_cur: str) -> dict:
    from_lower = from_cur.lower()
    try:
        r = requests.get(f"{_API_BASE}/{from_lower}.json", timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception:
        r = requests.get(f"{_FALLBACK}/{from_lower}.json", timeout=10)
        r.raise_for_status()
        return r.json()


def convert_currency(query: str) -> str:
    parts = query.strip().upper().split()
    try:
        if len(parts) >= 4 and "TO" in parts:
            to_idx  = parts.index("TO")
            amount  = float(parts[0])
            from_cur = parts[1].lower()
            to_cur  = parts[to_idx + 1].lower()
            data   = _fetch_rates(from_cur)
            rates  = data[from_cur]
            if to_cur not in rates:
                return f"Currency '{to_cur.upper()}' not found."
            rate = rates[to_cur]
            return (
                f"Currency Conversion\n"
                f"  {amount:,.2f} {from_cur.upper()}  =  {amount * rate:,.2f} {to_cur.upper()}\n"
                f"  Rate: 1 {from_cur.upper()} = {rate:,.4f} {to_cur.upper()}\n"
                f"  Date: {data.get('date', 'today')}"
            )
        elif len(parts) == 3 and parts[1] == "TO":
            from_cur = parts[0].lower()
            to_cur   = parts[2].lower()
            data  = _fetch_rates(from_cur)
            rate  = data[from_cur].get(to_cur)
            if not rate:
                return f"Currency '{to_cur.upper()}' not found."
            return f"1 {from_cur.upper()} = {rate:,.4f} {to_cur.upper()} ({data.get('date','today')})"
        else:
            from_cur = parts[0].lower()
            data  = _fetch_rates(from_cur)
            rates = data[from_cur]
            lines = [
                f"  1 {from_cur.upper()} = {rates[c]:,.4f} {c.upper()}"
                for c in _SHOW_RATES if c != from_cur and c in rates
            ]
            return f"{from_cur.upper()} Rates ({data.get('date','today')}):\n" + "\n".join(lines)
    except Exception as e:
        return f"Error: {e}"


currency_tool = Tool(
    name="currency",
    func=convert_currency,
    description=(
        "Convert currencies or get live exchange rates. Supports 170+ currencies including EGP, SAR, AED. "
        "Input: '100 USD to EGP', 'EUR to GBP', or just 'USD' to see rates. "
        "Common codes: USD, EUR, EGP, GBP, SAR, AED, TRY, JPY, CNY, CAD."
    ),
)
