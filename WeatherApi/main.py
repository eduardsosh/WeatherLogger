import requests
import logging
import os
from api import fetch_weather_forecast
from db import save_forecast
from logger import get_logger

logger = get_logger(__name__)

API_BASE_URL = "api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={APIkey}"
API_KEY = os.environ.get("OPENWEATHER_API_KEY")
LATITUDE = "56.9677" # Riga general coordinates
LONGITUDE = "24.1056"

# Riga general coordinates
LATITUDE = "56.9677"
LONGITUDE = "24.1056"


if __name__ == "__main__":
    try:
        forecast_data = fetch_weather_forecast(LATITUDE, LONGITUDE, API_KEY)
        save_forecast(forecast_data)
    except Exception as e:
        logger.error(f"Error fetching weather data: {e}")