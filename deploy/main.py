import logging
from flask import jsonify, Request

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
    fetch_and_save_data()
    clean_daily_csv()
    upload_to_gcs()
    load_csv_to_bigquery()
    logging.info("✅ Pipeline completed successfully.")

def entry_point(request: Request):
    """Cloud Function HTTP entry point"""
    try:
        run_pipeline()
        return jsonify({"status": "success", "message": "Pipeline executed successfully"}), 200
    except Exception as e:
        logging.error(f"❌ Cloud Function failed: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
