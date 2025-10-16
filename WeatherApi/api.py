import requests
import os
from logger import get_logger

logger = get_logger(__name__)

API_BASE_URL = "http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={APIkey}"
API_KEY = os.environ.get("OPENWEATHER_API_KEY")
LATITUDE = "56.9677" # Riga general coordinates
LONGITUDE = "24.1056"

def fetch_weather_forecast(lat, lon, api_key):
    url = API_BASE_URL.format(lat=lat, lon=lon, APIkey=api_key)
    try:
        logger.info(f"Fetching weather data from URL: {url}")
        response = requests.get(url)
        if response.status_code == 200:
            logger.info(f"Fetched data: {response.status_code}")
            return response.json()
        else:
            response.raise_for_status()
    except Exception as e:
        logger.error(f"Error fetching weather data: {e}")
        raise

if __name__ == "__main__":
    try:
        forecast_data = fetch_weather_forecast(LATITUDE, LONGITUDE, API_KEY)
        logger.info(f"Weather forecast data fetched successfully. {forecast_data['city']['name']}")
    except Exception as e:
        logger.error(f"Error fetching weather data: {e}")