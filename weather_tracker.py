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
        "hourly": ["apparent_temperature", "precipitation_probability", "precipitation", "weather_code", "pressure_msl"],
	    "temperature_unit": "fahrenheit",
	    "precipitation_unit": "inch",
        "timezone": "America/Los_Angeles",
        "past_days": 1,  # Includes yesterday's data
        "forecast_days": 1,  # Includes today's data
    }
    responses = openmeteo.weather_api(url, params = params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]
    print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
    print(f"Elevation: {response.Elevation()} m asl")
    print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")

    # Process hourly data. The order of variables needs to be the same as requested.
    hourly = response.Hourly()
    hourly_apparent_temperature = hourly.Variables(0).ValuesAsNumpy()
    hourly_precipitation_probability = hourly.Variables(1).ValuesAsNumpy()
    hourly_precipitation = hourly.Variables(2).ValuesAsNumpy()
    hourly_weather_code = hourly.Variables(3).ValuesAsNumpy()
    hourly_weather_sym = [WmoWeather.get(x).icon for x in hourly_weather_code]
    hourly_pressure_msl = hourly.Variables(4).ValuesAsNumpy()

    hourly_data = {"date": pd.date_range(
        start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
        end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
        freq=pd.Timedelta(seconds=hourly.Interval()),
        inclusive="left"
    ).tz_convert("America/Los_Angeles"), "weather_sym": hourly_weather_sym,
                   "apparent_temperature": hourly_apparent_temperature}
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