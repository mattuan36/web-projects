"""Open-Meteo forecast and geocoding helpers."""

from __future__ import annotations

import openmeteo_requests

import pandas as pd
import requests
import requests_cache
from retry_requests import retry
from weather_codes import WmoWeather

FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"

# Order matters: the indices below refer to this list.
HOURLY_VARIABLES = [
    "apparent_temperature",
    "precipitation_probability",
    "precipitation",
    "weather_code",
    "is_day",
    "pressure_msl",
]


def _http_session():
    """Cached + retrying session, shared by the forecast and geocoding calls."""
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    return retry(cache_session, retries=5, backoff_factor=0.2)


def geocode_location(query, count=5):
    """Resolve a place name to coordinates. Returns [] when nothing matches."""
    response = _http_session().get(
        GEOCODE_URL,
        params={"name": query, "count": count, "language": "en", "format": "json"},
        timeout=15,
    )
    response.raise_for_status()
    return [
        {
            "name": item["name"],
            "region": item.get("admin1") or "",
            "country": item.get("country") or "",
            "country_code": item.get("country_code") or "",
            "latitude": item["latitude"],
            "longitude": item["longitude"],
            "timezone": item.get("timezone") or "auto",
        }
        for item in response.json().get("results") or []
    ]


def _timezone_name(response):
    """The SDK hands back bytes, and pandas needs a str."""
    zone = response.Timezone()
    if isinstance(zone, (bytes, bytearray)):
        zone = zone.decode("utf-8")
    return zone or "UTC"


def get_hourly_weather_data(input_coords, timezone="auto"):
    # Setup the Open-Meteo API client with cache and retry on error
    openmeteo = openmeteo_requests.Client(session=_http_session())

    params = {
        "latitude": round(float(input_coords[0]), 4),
        "longitude": round(float(input_coords[1]), 4),
        "hourly": HOURLY_VARIABLES,
        "temperature_unit": "fahrenheit",
        "precipitation_unit": "inch",
        # "auto" resolves from the coordinates; callers may pass an IANA name.
        "timezone": timezone or "auto",
        "past_days": 1,  # Includes yesterday's data
        "forecast_days": 2,  # Includes today's data
    }
    responses = openmeteo.weather_api(FORECAST_URL, params=params, timeout=20)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]

    # Process hourly data. The order of variables needs to be the same as requested.
    hourly = response.Hourly()
    hourly_apparent_temperature = hourly.Variables(0).ValuesAsNumpy().round().astype(int)
    hourly_precipitation_probability = hourly.Variables(1).ValuesAsNumpy()
    hourly_precipitation = hourly.Variables(2).ValuesAsNumpy()
    hourly_weather_code = hourly.Variables(3).ValuesAsNumpy()
    hourly_is_day = hourly.Variables(4).ValuesAsNumpy()
    hourly_weather_sym = [WmoWeather.get(code, is_night=(is_day == 0)) for code, is_day in zip(hourly_weather_code, hourly_is_day)]
    hourly_pressure_msl = hourly.Variables(5).ValuesAsNumpy()

    # The location's own zone, so "hour" means the hour there.
    local_zone = _timezone_name(response)

    # 1. Generate the DatetimeIndex and convert the timezone
    dates_index = pd.date_range(
        start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
        end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
        freq=pd.Timedelta(seconds=hourly.Interval()),
        inclusive="left"
    ).tz_convert(local_zone)

    # 2. Use a lambda map to format, strip leading zero from the hour, and insert the <br> tag
    formatted_dates = dates_index.map(
        lambda dt: f"{dt.strftime('%a')}<br>{dt.strftime('%I %p').lstrip('0')}"
    )

    # 3. Find the position of the current local hour in the timeline
    now_rounded_down = pd.Timestamp.now(tz=local_zone).floor("h")

    # method="ffill" ensures it snaps to the nearest preceding match (rounded down)
    nearest_hour_index = max(0, dates_index.get_indexer([now_rounded_down], method="ffill")[0])

    hourly_weather_data = [
        {
            "date": date,
            "weather_sym": symbol,
            "apparent_temperature": temp
        }
        for date, symbol, temp in zip(
            formatted_dates[nearest_hour_index: nearest_hour_index + 24],
            hourly_weather_sym[nearest_hour_index: nearest_hour_index + 24],
            hourly_apparent_temperature[nearest_hour_index: nearest_hour_index + 24]
        )
    ]
    temp_compare_data = {
        "chart_dates": [item[7:] for item in formatted_dates[0:24].tolist()],
        "yesterday_temps": hourly_apparent_temperature[0:24].tolist(),
        "today_temps": hourly_apparent_temperature[24:48].tolist()
    }

    return {
        "hourly_weather": hourly_weather_data,
        "temp_compare": temp_compare_data,
    }


def main():
    input_coords = [45.55, -122.69]  # Portland, OR
    get_hourly_weather_data(input_coords)


if __name__ == "__main__":
    main()