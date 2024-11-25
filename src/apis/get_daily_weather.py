import pandas as pd
from typing import List, Optional

from energy_manager.src.apis.get_coordinates import get_coordinates
from energy_manager.src.apis.get_hourly_weather import get_hourly_weather


def get_daily_weather(city_name: str, timestamps: List[int]) -> Optional[pd.DataFrame]:
   """
   Fetch weather data for all timestamps and return a concatenated DataFrame.

   Args:
       city_name (str): Name of the city.
       timestamps (List[int]): List of Unix timestamps to fetch weather data for.

   Returns:
       Optional[pd.DataFrame]: Concatenated DataFrame with weather data, or None if all fetches fail.
   """
   if not get_coordinates(city_name): return None

   df_daily_weather = []
   for timestamp in timestamps:
      df_hourly_weather = get_hourly_weather(city_name, timestamp)
      if df_hourly_weather is None:
         print(f"Failed to fetch weather data for timestamp {timestamp}.")
         return None
      else:
         df_daily_weather.append(df_hourly_weather)

   return pd.concat(df_daily_weather, ignore_index=True)
