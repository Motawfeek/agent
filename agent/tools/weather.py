"""Weather tool using the free wttr.in API (no API key required)."""
import requests
from langchain.tools import Tool


def get_weather(city: str) -> str:
    """Fetch current weather for a given city using wttr.in."""
    city_encoded = city.strip().replace(" ", "+")
    url = f"https://wttr.in/{city_encoded}?format=j1"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        current = data["current_condition"][0]
        area_info = data["nearest_area"][0]
        area_name = area_info["areaName"][0]["value"]
        country = area_info["country"][0]["value"]

        return (
            f"Weather in {area_name}, {country}:\n"
            f"  Temperature : {current['temp_C']}°C / {current['temp_F']}°F\n"
            f"  Feels Like  : {current['FeelsLikeC']}°C\n"
            f"  Condition   : {current['weatherDesc'][0]['value']}\n"
            f"  Humidity    : {current['humidity']}%\n"
            f"  Wind Speed  : {current['windspeedKmph']} km/h\n"
            f"  Visibility  : {current['visibility']} km\n"
            f"  UV Index    : {current['uvIndex']}"
        )

    except requests.exceptions.Timeout:
        return f"Error: Request timed out for '{city}'. Try again later."
    except requests.exceptions.HTTPError as exc:
        return f"Error: Could not retrieve weather for '{city}' ({exc})."
    except (KeyError, ValueError) as exc:
        return f"Error: Unexpected response format ({exc})."
    except Exception as exc:
        return f"Error: {exc}"


weather_tool = Tool(
    name="weather",
    func=get_weather,
    description=(
        "Get real-time weather conditions for any city worldwide. "
        "Returns temperature, humidity, wind speed, and sky conditions. "
        "Input: a city name, e.g. 'Cairo', 'New York', 'Tokyo'."
    ),
)
