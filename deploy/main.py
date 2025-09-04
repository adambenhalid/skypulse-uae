import sys
import os
import logging
from flask import jsonify, Request

# 👇 Add the deploy/ folder to Python's search path
sys.path.append(os.path.dirname(__file__))

from fetch_data import fetch_and_save_data
from clean_transform import clean_daily_csv
from upload_to_gcs import upload_to_gcs
from load_to_bigquery import load_csv_to_bigquery

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def run_pipeline():
    logging.info("🚀 Starting UAE Weather Data Pipeline")

    logging.info("📥 Step 1: Fetching raw data from Open-Meteo API...")
    fetch_and_save_data()
    logging.info("✅ Data fetched and saved locally.")

    logging.info("🧹 Step 2: Cleaning and transforming daily CSV...")
    clean_daily_csv()
    logging.info("✅ Data cleaned and saved as daily CSV.")

    logging.info("☁️ Step 3: Uploading cleaned CSV to Google Cloud Storage...")
    upload_to_gcs()
    logging.info("✅ File successfully uploaded to GCS bucket.")

    logging.info("🗄️ Step 4: Loading file into BigQuery table...")
    load_csv_to_bigquery()
    logging.info("✅ Data successfully loaded into BigQuery.")

    logging.info("🎉 Pipeline completed successfully!")

def entry_point(request: Request):
    """Cloud Function HTTP entry point"""
    try:
        run_pipeline()
        return jsonify({"status": "success", "message": "Pipeline executed successfully"}), 200
    except Exception as e:
        logging.error(f"❌ Cloud Function failed: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# 👇 This part is missing in your version
if __name__ == "__main__":
    run_pipeline()
