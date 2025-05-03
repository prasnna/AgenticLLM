"""Tools for the Google ADK agent."""

import datetime
from zoneinfo import ZoneInfo

def get_weather(city: str) -> dict:
    """
    Retrieves the current weather report for a specified city.
    
    Args:
        city (str): The name of the city for which to retrieve the weather report.
    
    Returns:
        dict: status and result or error msg.
    """
    if city.lower() == "new york":
        return {
            "status": "success",
            "report": (
                "The weather in New York is sunny with a temperature of 25 degrees"
                " Celsius (77 degrees Fahrenheit)."
            ),
        }
    elif city.lower() == "london":
        return {
            "status": "success",
            "report": (
                "The weather in London is cloudy with a temperature of 18 degrees"
                " Celsius (64 degrees Fahrenheit)."
            ),
        }
    elif city.lower() == "tokyo":
        return {
            "status": "success",
            "report": (
                "The weather in Tokyo is rainy with a temperature of 22 degrees"
                " Celsius (72 degrees Fahrenheit)."
            ),
        }
    else:
        return {
            "status": "error",
            "error_message": f"Weather information for '{city}' is not available.",
        }

def get_current_time(city: str) -> dict:
    """
    Returns the current time in a specified city.
    
    Args:
        city (str): The name of the city for which to retrieve the current time.
    
    Returns:
        dict: status and result or error msg.
    """
    
    city_timezone_map = {
        "new york": "America/New_York",
        "london": "Europe/London",
        "tokyo": "Asia/Tokyo",
        "paris": "Europe/Paris",
        "sydney": "Australia/Sydney",
        "berlin": "Europe/Berlin",
        "moscow": "Europe/Moscow",
        "beijing": "Asia/Shanghai",
        "dubai": "Asia/Dubai",
        "los angeles": "America/Los_Angeles",
    }
    
    city_lower = city.lower()
    if city_lower in city_timezone_map:
        tz_identifier = city_timezone_map[city_lower]
    else:
        return {
            "status": "error",
            "error_message": (
                f"Sorry, I don't have timezone information for {city}."
            ),
        }
    
    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    report = (
        f'The current time in {city} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
    )
    return {"status": "success", "report": report}
