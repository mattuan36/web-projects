import openmeteo_requests

import pandas as pd
import requests_cache
from retry_requests import retry
from weather_codes import WmoWeather

def get_hourly_weather_data(input_coords):
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": input_coords[0],
        "longitude": input_coords[1],
        "hourly": ["apparent_temperature", "precipitation_probability", "precipitation", "weather_code", "is_day", "pressure_msl"],
	    "temperature_unit": "fahrenheit",
	    "precipitation_unit": "inch",
        "timezone": "America/Los_Angeles",
        "past_days": 1,  # Includes yesterday's data
        "forecast_days": 2,  # Includes today's data
    }
    responses = openmeteo.weather_api(url, params = params)

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

    # 1. Generate the DatetimeIndex and convert the timezone
    dates_index = pd.date_range(
        start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
        end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
        freq=pd.Timedelta(seconds=hourly.Interval()),
        inclusive="left"
    ).tz_convert("America/Los_Angeles")

    # 2. Use a lambda map to format, strip leading zero from the hour, and insert the <br> tag
    formatted_dates = dates_index.map(
        lambda dt: f"{dt.strftime('%a')}<br>{dt.strftime('%I %p').lstrip('0')}"
    )

    # Using your timezone: "America/Los_Angeles"
    now = pd.Timestamp.now(tz="America/Los_Angeles")

    # 2. Round the current time down to the nearest hour
    now_rounded_down = now.floor("h")

    # 3. Find the integer index position in your index timeline
    # method="ffill" ensures it snaps to the nearest preceding match (rounded down)
    nearest_hour_index = dates_index.get_indexer([now_rounded_down], method="ffill")[0]

    hourly_data = {
        "date": formatted_dates[nearest_hour_index:nearest_hour_index+24],
        "weather_sym": hourly_weather_sym[nearest_hour_index:nearest_hour_index+24],
        "apparent_temperature": hourly_apparent_temperature[nearest_hour_index:nearest_hour_index+24]
    }
        #,
                   #"precipitation_probability": hourly_precipitation_probability, "precipitation": hourly_precipitation,
                   #"pressure_msl": hourly_pressure_msl}


    hourly_dataframe = pd.DataFrame(data = hourly_data)

    # Pass the data to the template as a list of dictionaries
    hourly_records = hourly_dataframe.to_dict(orient='records')

    #print("\nHourly data\n", hourly_dataframe)
    return hourly_records

def main():
    input_coords = [45.55, -122.69]  # Portland, OR
    get_hourly_weather_data(input_coords)

if __name__ == "__main__":
    main()