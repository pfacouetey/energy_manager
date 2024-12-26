import gc
import numpy as np
import pandas as pd
from typing import Optional

from src.energy_manager.utils.set_edf_prices import set_edf_prices
from src.energy_manager.utils.set_hchp_hours import set_hchp_hours
from src.energy_manager.apis.weather.get_daily_weather import get_daily_weather
from src.energy_manager.utils.generate_daily_timestamps import generate_daily_timestamps
from src.energy_manager.utils.get_midnight_utc_timestamp import get_midnight_utc_timestamp
from src.energy_manager.apis.buildings.get_buildings_consumptions import get_buildings_consumptions


def compute_daily_expenses(
        user_city_name: str,
        user_dpe_usage: float,
        user_temperature: float,
        openweathermap_api_key: str,
        user_insulation_factor: Optional[float] = 1.0,
) -> Optional[pd.DataFrame]:
    """
    Computes daily energy expenses for different building types and DPE (Energy Performance Diagnosis)
    classes based on user-provided information, retrieved weather data, and default presets.

    The function combines various datasets, such as energy consumptions for buildings,
    hourly pricing options, and weather conditions. It estimates the daily energy expenses
    by considering the user's energy usage, insulation factor, and temperature preferences.
    The results are provided for multiple subscription options and categorized by building type
    and energy performance class.

    Args:
        user_city_name (str): The name of the city for which to compute energy expenses.
        user_dpe_usage (float): The user's energy consumption measured in kWh per square meter.
        user_temperature (float): The user's preferred temperature to maintain in the building.
        openweathermap_api_key (str): The API key used for accessing OpenWeatherMap data.
        user_insulation_factor (Optional[float]): A scalar factor representing the insulation quality of
            the user's building. Default is 1.0, which corresponds to standard insulation.

    Returns:
        Optional[pd.DataFrame]: A DataFrame containing the computed daily energy expenses for
            various subscription options, building types, and energy performance classes.
            Returns None if the required input datasets (e.g., weather, consumption data) cannot
            be obtained or processed.
    """
    buildings_consumptions_df = get_buildings_consumptions(city_name=user_city_name)

    if buildings_consumptions_df is None:
        print(f"No buildings consumption data found for the city {user_city_name}.")
        return None

    midnight_utc_timestamp = get_midnight_utc_timestamp()
    daily_timestamps = generate_daily_timestamps(start_timestamp=midnight_utc_timestamp)

    daily_weather_df = get_daily_weather(
        city_name=user_city_name,
        openweathermap_api_key=openweathermap_api_key,
        timestamps=daily_timestamps
    )
    if not daily_weather_df.empty:

        daily_weather_df["degree_diff"] = np.abs(daily_weather_df["temperature"] - user_temperature)
        del daily_weather_df["temperature"], daily_timestamps, midnight_utc_timestamp
        gc.collect()

        hchp_hours_df = set_hchp_hours()
        merged_df = daily_weather_df.copy(deep=True)
        merged_df[hchp_hours_df.columns.tolist()[1:]] = hchp_hours_df[hchp_hours_df.columns.tolist()[1:]].copy(deep=True)

        df_edf_prices = set_edf_prices()
        merged_two_df = merged_df.copy(deep=True)
        merged_two_df["option_0"] = np.unique(
            df_edf_prices.loc[df_edf_prices["subscription"] == "Base", df_edf_prices.columns[1:]].values[0]
        )[0]

        other_options = ["option_1", "option_2", "option_3", "option_4"]
        merged_two_df[other_options] = merged_two_df[other_options].map(
            lambda hour_type: (
                df_edf_prices.loc[
                    df_edf_prices["subscription"] == "Heures Creuses - Heures Pleines", "kwh_price_normal_hour"
                ].values[0] if hour_type == "HC"
                else df_edf_prices.loc[
                    df_edf_prices["subscription"] == "Heures Creuses - Heures Pleines", "kwh_price_peak_hour"
                ].values[0]
            )
        )
        gc.collect()

        merged_three_df = merged_two_df.copy(deep=True)
        all_options = ["option_0"] + other_options
        merged_three_df[all_options] = merged_three_df[all_options].apply(
            lambda option_col: user_dpe_usage * option_col * merged_three_df["degree_diff"] / user_insulation_factor,
            axis=0,
        )
        del merged_two_df, other_options, merged_three_df["degree_diff"]
        gc.collect()

        all_expenses = []
        for building_type in buildings_consumptions_df["building_type"].unique():
            dpe_building_type_df = buildings_consumptions_df[
                buildings_consumptions_df["building_type"] == building_type
            ]
            for dpe_class in dpe_building_type_df["dpe_class"].unique():
                temp_df = merged_three_df.copy(deep=True)
                dpe_value = dpe_building_type_df.loc[
                    dpe_building_type_df["dpe_class"] == dpe_class, "consumption_in_kwh_per_square_meter"
                ].values[0]
                temp_df[all_options] = temp_df[all_options].multiply(dpe_value)
                temp_df["building_type"] = building_type
                temp_df["dpe_class"] = dpe_class
                all_expenses.append(temp_df)
        expenses_df = pd.concat(all_expenses, ignore_index=True)
        gc.collect()

        columns_reordered = [
            "date_time",
            "weather_description",
            "option_0", "option_1", "option_2", "option_3", "option_4",
            "building_type",
            "dpe_class"
        ]
        expenses_df = expenses_df[columns_reordered]
        return expenses_df

    print("Failed to fetch daily weather data.")
    return None
