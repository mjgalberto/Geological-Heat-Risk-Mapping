import numpy as np
import pandas as pd

def celsius_to_fahrenheit(c):
    return c * 9.0 / 5.0 + 32.0

def compute_heat_index(T, RH):
    # Rothfusz regression (US NWS)
    return (
        -42.379 + 2.04901523 * T + 10.14333127 * RH - 0.22475541 * T * RH
        - 0.00683783 * T * T - 0.05481717 * RH * RH
        + 0.00122874 * T * T * RH + 0.00085282 * T * RH * RH
        - 0.00000199 * T * T * RH * RH
    )

def convert_to_geojson(geojson_data, df):
    risk_map = {}

    # Ensure temperature is float and humidity is present
    df['temperature'] = pd.to_numeric(df['temperature'], errors='coerce')
    df['humidity_level'] = pd.to_numeric(df['humidity_level'], errors='coerce')
    df = df.dropna(subset=['temperature', 'humidity_level'])

    # Summarize by region: take the mean temperature and humidity for each region over 12 months
    summary = df.groupby('location').agg({
        'temperature': 'mean',
        'humidity_level': 'mean'
    }).reset_index()

    # Compute Heat Index for each region using the mean values
    summary['T_F'] = summary['temperature'].apply(celsius_to_fahrenheit)
    summary['HI'] = summary.apply(lambda row: compute_heat_index(row['T_F'], row['humidity_level']), axis=1)

    # Normalize HI to 0-100% scale based on min/max HI across all regions
    hi_min = summary['HI'].min()
    hi_max = summary['HI'].max()
    if hi_max > hi_min:
        summary['risk_percent'] = summary['HI'].apply(lambda hi: max(0, min(100, round((hi - hi_min) / (hi_max - hi_min) * 100, 2))))
    else:
        summary['risk_percent'] = 0  # If all HI are the same, set risk to 0

    for _, row in summary.iterrows():
        location = row['location']
        risk = row['risk_percent']
        risk_map[location] = risk

    # Attach to GeoJSON
    for feature in geojson_data["features"]:
        region_name = feature["properties"].get("REGION")
        risk = risk_map.get(region_name)
        feature["properties"]["risk_percentage"] = risk

    return geojson_data, risk_map

# ---
# Scientific basis:
# - Heat Index formula: Rothfusz regression (US National Weather Service)
#   https://www.wpc.ncep.noaa.gov/html/heatindex_equation.shtml
# - Risk zones:
#   HI >= 103°F: Extreme risk
#   90°F <= HI < 103°F: High risk
#   80°F <= HI < 90°F: Moderate risk
#   HI < 80°F: Lower risk
# ---