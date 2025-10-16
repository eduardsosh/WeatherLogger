import sqlite3
import json
import datetime as dt
from db_scripts import CREATE_FORECAST_TABLE, INSERT_FORECAST
from logger import get_logger

logger = get_logger(__name__)
DB_NAME = 'weather_data.db'

def _init_db():
    """Initialize the SQLite database and create necessary tables.
    Returns the database connection."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute(CREATE_FORECAST_TABLE)
    cursor.close()
    
    logger.info("Database initialized and tables created.")
    conn.commit()
    return conn 
    
    
    
def save_forecast(forecast_data_dict: dict):
    """Save the fetched forecast data into the database."""
    conn = _init_db()
    cursor = conn.cursor()
    
    city = forecast_data_dict.get('city').get('name') # let fail if no city
    issued_at = dt.datetime.now().isoformat()

    count = 0
    for entry in forecast_data_dict.get('list', []):
        forecast_datetime = entry.get('dt_txt')
        forecast_data_json = json.dumps(forecast_data_dict)
        
        cursor.execute(INSERT_FORECAST, (
            issued_at,
            city,
            forecast_datetime,
            forecast_data_json
        ))
        count += 1
    

    conn.commit()
    conn.close()
    logger.info(f"{count} forecast entries saved to the database.")