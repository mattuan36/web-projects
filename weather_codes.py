from enum import Enum
from typing import NamedTuple, Optional

class WeatherDetails(NamedTuple):
    text: str
    icon: str
    night_icon: Optional[str] = None  # Optional field to support time-neutral fallback

class WmoWeather(Enum):
    """WMO Weather Codes mapped to human-readable text and Meteocons icons."""

    # --- Clear & Cloudy ---
    CLEAR_SKY = (0, WeatherDetails("Clear sky", "clear-day", "clear-night"))
    MAINLY_CLEAR = (1, WeatherDetails("Mainly clear", "partly-cloudy-day", "partly-cloudy-night"))
    PARTLY_CLOUDY = (2, WeatherDetails("Partly cloudy", "partly-cloudy-day", "partly-cloudy-night"))
    OVERCAST = (3, WeatherDetails("Overcast", "overcast-day", "overcast-night"))

    # --- Atmosphere (Fog & Haze) ---
    FOG = (45, WeatherDetails("Fog", "fog-day", "fog-night"))
    RIME_FOG = (48, WeatherDetails("Depositing rime fog", "fog"))  # Neutral

    # --- Drizzle ---
    LIGHT_DRIZZLE = (51, WeatherDetails("Light drizzle", "drizzle"))  # Neutral
    MODERATE_DRIZZLE = (53, WeatherDetails("Moderate drizzle", "drizzle"))  # Neutral
    DENSE_DRIZZLE = (55, WeatherDetails("Dense drizzle", "drizzle"))  # Neutral

    LIGHT_FREEZING_DRIZZLE = (56, WeatherDetails("Light freezing drizzle", "sleet"))  # Neutral
    DENSE_FREEZING_DRIZZLE = (57, WeatherDetails("Dense freezing drizzle", "sleet"))  # Neutral

    # --- Rain ---
    SLIGHT_RAIN = (61, WeatherDetails("Slight rain", "rain"))  # Neutral
    MODERATE_RAIN = (63, WeatherDetails("Moderate rain", "rain"))  # Neutral
    HEAVY_RAIN = (65, WeatherDetails("Heavy rain", "extreme-rain"))  # Neutral

    LIGHT_FREEZING_RAIN = (66, WeatherDetails("Light freezing rain", "sleet"))  # Neutral
    HEAVY_FREEZING_RAIN = (67, WeatherDetails("Heavy freezing rain", "extreme-sleet"))  # Neutral

    # --- Snow Fall ---
    SLIGHT_SNOW = (71, WeatherDetails("Slight snow fall", "snow"))  # Neutral
    MODERATE_SNOW = (73, WeatherDetails("Moderate snow fall", "snow"))  # Neutral
    HEAVY_SNOW = (75, WeatherDetails("Heavy snow fall", "extreme-snow"))  # Neutral
    SNOW_GRAINS = (77, WeatherDetails("Snow grains", "snowflake"))  # Neutral

    # --- Showers ---
    # Meteocons provides beautiful dynamic variations for convective showers
    SLIGHT_RAIN_SHOWERS = (80, WeatherDetails("Slight rain showers", "partly-cloudy-day-rain", "partly-cloudy-night-rain"))
    MODERATE_RAIN_SHOWERS = (81, WeatherDetails("Moderate rain showers", "rain"))  # Neutral
    VIOLENT_RAIN_SHOWERS = (82, WeatherDetails("Violent rain showers", "extreme-rain"))  # Neutral

    SLIGHT_SNOW_SHOWERS = (85, WeatherDetails("Slight snow showers", "partly-cloudy-day-snow", "partly-cloudy-night-snow"))
    HEAVY_SNOW_SHOWERS = (86, WeatherDetails("Heavy snow showers", "extreme-snow"))  # Neutral

    # --- Thunderstorms ---
    THUNDERSTORM = (95, WeatherDetails("Thunderstorm", "thunderstorms-day", "thunderstorms-night"))
    THUNDERSTORM_HAIL_SLIGHT = (96, WeatherDetails("Thunderstorm with slight hail", "thunderstorms-day-rain", "thunderstorms-night-rain"))
    THUNDERSTORM_HAIL_HEAVY = (99, WeatherDetails("Thunderstorm with heavy hail", "thunderstorms-day-extreme-rain", "thunderstorms-night-extreme-rain"))

    def __new__(cls, code_value: int, details: WeatherDetails):
        obj = object.__new__(cls)
        obj._value_ = code_value
        obj.text = details.text
        obj.icon = details.icon
        obj.night_icon = details.night_icon
        return obj

    @classmethod
    def get(cls, code: int, is_night: bool = False) -> str:
        """Safe lookup method that returns the mapped item or a default fallback."""
        for member in cls:
            # Match against the _value_ code initialized in __new__
            if member.value == code:
                # Return night_icon if true and configured, otherwise the main icon
                if is_night and member.night_icon:
                    return member.night_icon
                return member.icon

        # Fallback icon string if the WMO code is unknown
        return "not-available"