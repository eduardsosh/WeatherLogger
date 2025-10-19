CREATE_FORECAST_TABLE = \
"""
CREATE TABLE IF NOT EXISTS forecast (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    issued_at DATETIME,
    city TEXT,
    forecast_datetime DATETIME,
    temp REAL,
    feels_like REAL,
    temp_min REAL,
    temp_max REAL,
    pressure INTEGER,
    sea_level INTEGER,
    grnd_level INTEGER,
    humidity INTEGER,
    temp_kf REAL,
    weather_main TEXT,
    clouds_all INTEGER,
    wind_speed REAL,
    wind_deg INTEGER,
    wind_gust REAL,
    visibility INTEGER,
    pop REAL
)
"""

INSERT_FORECAST = \
"""
INSERT INTO forecast (
    issued_at,
    city,
    forecast_datetime,
    temp,
    feels_like,
    temp_min,
    temp_max,
    pressure,
    sea_level,
    grnd_level,
    humidity,
    temp_kf,
    weather_main,
    clouds_all,
    wind_speed,
    wind_deg,
    wind_gust,
    visibility,
    pop
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""
