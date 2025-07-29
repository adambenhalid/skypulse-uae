from datetime import datetime, timezone
from pathlib import Path
import requests
import pandas as pd
import logging
import os

# ------------------------------------------------------------------------------
# 📘 CONFIGURATION
# ------------------------------------------------------------------------------
latitude = 25.2048
longitude = 55.2708
today = datetime.now(timezone.utc).date().isoformat()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Cloud Functions only allow writing to /tmp
TMP_DATA_DIR = Path("/tmp/data")
TMP_DATA_DIR.mkdir(parents=True, exist_ok=True)

# ------------------------------------------------------------------------------
# 🔧 FUNCTION: Fetch data from an API and validate response
# ------------------------------------------------------------------------------
def fetch_hourly_data(url: str, label: str) -> pd.DataFrame:
    """Fetch and validate hourly JSON data from API."""
    logging.info(f"🌐 Requesting {label} data...")
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"❌ {label} API failed with status {response.status_code}")

    data = response.json()
    if "hourly" not in data:
        raise KeyError(f"❌ {label} API response missing 'hourly' key")

    df = pd.DataFrame(data["hourly"])
    if df.empty:
        raise ValueError(f"❌ {label} data is empty")

    logging.info(f"✅ Received {len(df)} rows of {label} data.")
    return df

# ------------------------------------------------------------------------------
# 🚀 MAIN FUNCTION: Orchestrates data fetch and save
# ------------------------------------------------------------------------------
def fetch_and_save_data():
    """Fetch weather and air quality data and save as daily CSV."""
    weather_url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={latitude}&longitude={longitude}"
        f"&hourly=temperature_2m,apparent_temperature,relative_humidity_2m"
        f"&timezone=Asia%2FDubai&start_date={today}&end_date={today}"
    )

    air_url = (
        f"https://air-quality-api.open-meteo.com/v1/air-quality?"
        f"latitude={latitude}&longitude={longitude}"
        f"&hourly=pm10,pm2_5"
        f"&timezone=Asia%2FDubai&start_date={today}&end_date={today}"
    )

    weather_df = fetch_hourly_data(weather_url, "Weather")
    air_df = fetch_hourly_data(air_url, "Air Quality")
    merged_df = pd.merge(weather_df, air_df, on="time")
    merged_df.rename(columns={"time": "timestamp"}, inplace=True)

    output_path = TMP_DATA_DIR / f"{today}.csv"
    merged_df.to_csv(output_path, index=False)
    logging.info(f"📁 Data saved successfully to: {output_path}")

# ------------------------------------------------------------------------------
# ▶️ ENTRY POINT
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    fetch_and_save_data()
