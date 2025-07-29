from google.cloud import bigquery
from datetime import datetime, timezone
import os
import logging

# ------------------------------------------------------------------------------
# 📘 CONFIGURATION
# ------------------------------------------------------------------------------

# Project and dataset configuration
project_id = os.environ.get("GCP_PROJECT", "skypulse-uae")
dataset_id = os.environ.get("BQ_DATASET", "uae_weather_data")
table_id = os.environ.get("BQ_TABLE", "daily_readings")
bucket_name = os.environ.get("GCS_BUCKET", "uae-weather-data-avb-2025")

# Current date
today = datetime.now(timezone.utc).date().isoformat()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ------------------------------------------------------------------------------
# 🧾 LOAD FUNCTION
# ------------------------------------------------------------------------------

def load_csv_to_bigquery():
    """
    Load cleaned weather and air quality data from GCS into BigQuery.
    """
    gcs_uri = f"gs://{bucket_name}/daily/{today}-clean.csv"
    table_ref = f"{project_id}.{dataset_id}.{table_id}"

    client = bigquery.Client()
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        autodetect=True,
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
    )

    logging.info(f"📥 Starting load job for: {gcs_uri}")
    job = client.load_table_from_uri(gcs_uri, table_ref, job_config=job_config)
    job.result()  # Wait for job to complete

    logging.info(f"✅ Loaded {today}-clean.csv into {table_ref}")

# ------------------------------------------------------------------------------
# ▶️ ENTRY POINT
# ------------------------------------------------------------------------------

if __name__ == "__main__":
    load_csv_to_bigquery()
