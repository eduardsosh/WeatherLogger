CREATE_FORECAST_TABLE = \
"""
CREATE TABLE IF NOT EXISTS forecast (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    issued_at DATETIME,
    city TEXT,
    forecast_datetime DATETIME,
    forecast_data TEXT
)
"""

INSERT_FORECAST = \
"""
INSERT INTO forecast (issued_at, city, forecast_datetime, forecast_data)
VALUES (?, ?, ?, ?)
"""
