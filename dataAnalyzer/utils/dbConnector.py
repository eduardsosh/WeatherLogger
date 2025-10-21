import sqlite3
from pathlib import Path

BASE_PATH = Path(__file__).parent.parent.parent
DB_PATH = BASE_PATH / 'local/weather.db'


FORECAST_TABLE_FIELDTYPE = [
    'id',
    'issued_at',
    'city',
    'forecast_datetime',
    'temp',
    'feels_like',
    'temp_min',
    'temp_max',
    'pressure',
    'sea_level',
    'grnd_level',
    'humidity',
    'temp_kf',
    'weather_main',
    'clouds_all',
    'wind_speed',
    'wind_deg',
    'wind_gust',
    'visibility',
    'pop',
]

def get_db_connection(db_path: str = DB_PATH) -> sqlite3.Connection:
    """Get a connection to the SQLite database at the specified path."""
    print(f"Connecting to database at: {db_path}")
    conn = sqlite3.connect(db_path)
    return conn


class dbConnector:
    _instances = []

    def __init__(self):
        dbConnector._instances.append(self)

    @classmethod
    def close_all_connections(cls):
        for instance in cls._instances:
            if hasattr(instance, 'conn') and instance.conn:
                instance.conn.close()
    
    def get_connection(self):
        if not hasattr(self, 'conn') or self.conn is None:
            self.conn = get_db_connection()
        else:
            print("Reusing existing database connection.")
        return self.conn
