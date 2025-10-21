from utils.dbConnector import get_db_connection, FORECAST_TABLE_FIELDTYPE
from pprint import pprint
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt

def get_date_forecast_counts():
    """Retrieve the count of forecast entries grouped by forecast date."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = """
    SELECT 
        forecast_datetime AS forecast_date, 
        COUNT(*) AS entry_count
    FROM 
        forecast
    GROUP BY 
        forecast_date
    ORDER BY 
        forecast_date;
    """
    
    cursor.execute(query)
    results = cursor.fetchall()
    pprint(results)

    cursor.close()
    conn.close()
    
    return results



def forecasts_for_date(forecast_date: str):
    """Retrieve all forecast entries for a specific forecast date."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = """
    SELECT *
    FROM forecast
    WHERE forecast_datetime = ?
    ORDER BY forecast_datetime;
    """
    
    cursor.execute(query, (forecast_date,))
    results = cursor.fetchall()

    cursor.close()
    conn.close()
    print(results)
    return results

def k_to_c(kelvin_str: str) -> float:
    """Convert temperature from Kelvin to Celsius."""
    kelvin_temp = float(kelvin_str)
    return kelvin_temp - 273.15

def _to_dt(s):
    if isinstance(s, dt.datetime):
        return s
    s = str(s).strip()
    # fast path: "YYYY-mm-dd HH:MM:SS"
    try:
        return dt.datetime.strptime(s, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        pass
    # ISO variants (e.g., with T or Z)
    if s.endswith('Z'):
        s = s[:-1] + '+00:00'
    return dt.datetime.fromisoformat(s).replace(tzinfo=None)


def plot_forecast_evolution_multi(forecast_list: list, field_names):
    """
    Plot one line per field in `field_names` against issuance time for the same forecast_datetime.
    Assumes all fields are comparable and need the same value transform (k_to_c).
    """
    if isinstance(field_names, str):
        field_names = [field_names]

    # Parse rows and collect
    rows = []
    target_dt = None
    for entry in forecast_list:
        row = dict(zip(FORECAST_TABLE_FIELDTYPE, entry))
        target_dt = target_dt or row.get('forecast_datetime')  # identical across rows
        rows.append({
            'issued_at': _to_dt(row['issued_at']),
            **{fn: row.get(fn) for fn in field_names}
        })

    if not rows:
        raise ValueError("No rows to plot.")

    # Sort by issuance time once
    rows.sort(key=lambda r: r['issued_at'])

    # Build per-field series (skip None values)
    series = {}
    for fn in field_names:
        xs_f, ys_f = [], []
        for r in rows:
            val = r.get(fn)
            if val is None:
                continue
            xs_f.append(r['issued_at'])
            ys_f.append(k_to_c(val))  # same transform for all fields
        if xs_f:  # only keep non-empty series
            series[fn] = (xs_f, ys_f)

    if not series:
        raise ValueError("No plottable data for the requested fields.")

    # Plot
    fig, ax = plt.subplots(figsize=(10, 5))
    for fn, (xs_f, ys_f) in series.items():
        ax.plot(xs_f, ys_f, marker='o', label=fn)

    fields_str = ", ".join(series.keys())
    ax.set_title(f'{fields_str} for forecast_datetime={target_dt}')
    ax.set_xlabel('issued_at')
    ax.set_ylabel(f'{fields_str} (°C)')

    # ticks every 3 hours, formatted
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=3))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))

    ax.legend()
    ax.grid(True, which='major', linestyle='--', alpha=0.4)

    fig.autofmt_xdate()
    fig.tight_layout()
    plt.show()

if __name__ == "__main__":
    forecasts = forecasts_for_date("2025-10-21 18:00:00")
    plot_forecast_evolution_multi(forecasts, ['temp', 'feels_like','temp_min', 'temp_max'])