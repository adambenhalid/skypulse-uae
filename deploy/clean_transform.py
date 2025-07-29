import pandas as pd
from pathlib import Path
from datetime import datetime, timezone
import logging

# --------------------------------------------------------------------------
# 📘 CONFIGURATION
# --------------------------------------------------------------------------
today = datetime.now(timezone.utc).date().isoformat()
TMP_DATA_DIR = Path("/tmp/data")
TMP_DATA_DIR.mkdir(parents=True, exist_ok=True)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# --------------------------------------------------------------------------
# 🧼 CLEANING FUNCTION
# --------------------------------------------------------------------------
def clean_daily_csv():
    """
    Load daily raw CSV from /tmp, clean it, enforce schema, add 'date', and save the cleaned version.
    """
    input_path = TMP_DATA_DIR / f"{today}.csv"
    output_path = TMP_DATA_DIR / f"{today}-clean.csv"

    logging.info(f"🔍 Loading raw data from {input_path}")
    df = pd.read_csv(input_path)

    if df.empty:
        raise ValueError("❌ Raw data file is empty.")

    df.dropna(inplace=True)
    df = df.round(2)

    # ✅ Enforce float types for schema consistency
    numeric_columns = [
        "temperature_2m",
        "apparent_temperature",
        "relative_humidity_2m",
        "pm10",
        "pm2_5"
    ]
    for col in numeric_columns:
        if col in df.columns:
            df[col] = df[col].astype(float)

    # ✅ Add 'date' column for deduplication and partitioning
    df["date"] = today

    if df.empty:
        raise ValueError("❌ Data is empty after cleaning.")

    df.to_csv(output_path, index=False)
    logging.info(f"✅ Cleaned data saved to {output_path}")

# --------------------------------------------------------------------------
# ▶️ ENTRY POINT
# --------------------------------------------------------------------------
if __name__ == "__main__":
    clean_daily_csv()
