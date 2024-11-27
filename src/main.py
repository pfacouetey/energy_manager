from energy_manager.src.utils.get_midnight_utc_timestamp import get_midnight_utc_timestamp
from energy_manager.src.utils.generate_daily_timestamps import generate_daily_timestamps
from energy_manager.src.apis.weather.get_daily_weather import get_daily_weather

def main() -> None:
    """
    Main function to orchestrate the weather data fetching process.
    """
    midnight_utc_timestamp = get_midnight_utc_timestamp()
    all_timestamps = generate_daily_timestamps(start_timestamp=midnight_utc_timestamp)
    df_daily_weather = get_daily_weather(city_name="Nangis", timestamps=all_timestamps)
    print(df_daily_weather)

if __name__ == "__main__":
    main()