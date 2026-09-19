from enum import Enum
from typing import NamedTuple

class WeatherDetails(NamedTuple):
    text: str
    icon: str

class WmoWeather(Enum):
    """WMO Weather Codes mapped to human-readable text and Bootstrap icons."""
    # Clear & Cloudy
    CLEAR_SKY = (0, WeatherDetails("Clear sky", "bi-sun-fill"))
    MAINLY_CLEAR = (1, WeatherDetails("Mainly clear", "bi-cloud-sun-fill"))
    PARTLY_CLOUDY = (2, WeatherDetails("Partly cloudy", "bi-cloud-sun"))
    OVERCAST = (3, WeatherDetails("Overcast", "bi-cloud-fill"))

    # Fog
    FOG = (45, WeatherDetails("Fog", "bi-cloud-fog-fill"))
    DEPOSITING_RIME_FOG = (48, WeatherDetails("Depositing rime fog", "bi-cloud-fog"))

    # Drizzle
    LIGHT_DRIZZLE = (51, WeatherDetails("Light drizzle", "bi-cloud-drizzle"))
    MODERATE_DRIZZLE = (53, WeatherDetails("Moderate drizzle", "bi-cloud-drizzle-fill"))
    DENSE_DRIZZLE = (55, WeatherDetails("Dense drizzle", "bi-cloud-drizzle-fill"))
    LIGHT_FREEZING_DRIZZLE = (56, WeatherDetails("Light freezing drizzle", "bi-cloud-sleet"))
    DENSE_FREEZING_DRIZZLE = (58, WeatherDetails("Dense freezing drizzle", "bi-cloud-sleet-fill"))

    # Rain
    SLIGHT_RAIN = (61, WeatherDetails("Slight rain", "bi-cloud-rain"))
    MODERATE_RAIN = (63, WeatherDetails("Moderate rain", "bi-cloud-rain-fill"))
    HEAVY_RAIN = (65, WeatherDetails("Heavy rain", "bi-cloud-rain-heavy-fill"))
    LIGHT_FREEZING_RAIN = (66, WeatherDetails("Light freezing rain", "bi-cloud-sleet"))
    HEAVY_FREEZING_RAIN = (67, WeatherDetails("Heavy freezing rain", "bi-cloud-sleet-fill"))

    # Snow
    SLIGHT_SNOWFALL = (71, WeatherDetails("Slight snowfall", "bi-cloud-snow"))
    MODERATE_SNOWFALL = (73, WeatherDetails("Moderate snowfall", "bi-cloud-snow-fill"))
    HEAVY_SNOWFALL = (75, WeatherDetails("Heavy snowfall", "bi-cloud-snow-heavy-fill"))
    SNOW_GRAINS = (77, WeatherDetails("Snow grains", "bi-snow"))

    # Rain Showers
    SLIGHT_RAIN_SHOWERS = (80, WeatherDetails("Slight rain showers", "bi-cloud-rain"))
    MODERATE_RAIN_SHOWERS = (81, WeatherDetails("Moderate rain showers", "bi-cloud-rain-fill"))
    VIOLENT_RAIN_SHOWERS = (82, WeatherDetails("Violent rain showers", "bi-cloud-rain-heavy-fill"))

    # Snow Showers
    SLIGHT_SNOW_SHOWERS = (85, WeatherDetails("Slight snow showers", "bi-cloud-snow"))
    HEAVY_SNOW_SHOWERS = (86, WeatherDetails("Heavy snow showers", "bi-cloud-snow-heavy-fill"))

    # Thunderstorm
    THUNDERSTORM = (95, WeatherDetails("Thunderstorm", "bi-cloud-lightning-fill"))
    THUNDERSTORM_SLIGHT_HAIL = (96, WeatherDetails("Thunderstorm with slight hail", "bi-cloud-lightning-rain"))
    THUNDERSTORM_HEAVY_HAIL = (99, WeatherDetails("Thunderstorm with heavy hail", "bi-cloud-lightning-rain-fill"))

    def __new__(cls, code_value: int, details: WeatherDetails):
        obj = object.__new__(cls)
        obj._value_ = code_value
        obj.text = details.text
        obj.icon = details.icon
        return obj

    @classmethod
    def get(cls, code: int) -> WeatherDetails:
        """Safe lookup method that returns the mapped item or a default fallback."""
        try:
            return cls(code)
        except ValueError:
            return WeatherDetails("Unknown", "bi-question-circle")