from google.cloud import storage
from pathlib import Path
from datetime import datetime, timezone
import os
import logging

# ------------------------------------------------------------------------------
# 📘 CONFIGURATION
# ------------------------------------------------------------------------------
today = datetime.now(timezone.utc).date().isoformat()
bucket_name = os.environ.get("GCS_BUCKET", "uae-weather-data-avb-2025")

# Use Cloud Function's writable temp directory
TMP_DATA_DIR = Path("/tmp/data")

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ------------------------------------------------------------------------------
# ☁️ UPLOAD FUNCTION
# ------------------------------------------------------------------------------
def upload_to_gcs():
    """
    Upload the cleaned daily CSV file from /tmp to Google Cloud Storage.
    """
    local_file = TMP_DATA_DIR / f"{today}-clean.csv"
    gcs_path = f"daily/{today}-clean.csv"

    if not local_file.exists():
        raise FileNotFoundError(f"❌ File not found: {local_file}")

    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(gcs_path)
    blob.upload_from_filename(local_file)

    logging.info(f"✅ Uploaded {local_file} to gs://{bucket_name}/{gcs_path}")

# ------------------------------------------------------------------------------
# ▶️ ENTRY POINT
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    upload_to_gcs()
