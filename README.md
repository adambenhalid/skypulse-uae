# SkyPulse UAE

**Daily Weather & Air Quality Data Pipeline (GCP Free-Tier Project)**

![Architecture](architecture.png)

## 📌 Overview

SkyPulse UAE is a serverless data engineering pipeline that fetches **hourly weather and air quality data** for the UAE from the [Open-Meteo API](https://open-meteo.com/), processes it, and stores it in **Google Cloud Platform (GCP)** for analysis and visualization.
This project is designed as a **portfolio-ready data engineering solution** built entirely within GCP’s free tier.

---

## ⚙️ Tools & Technologies

* **Programming:** Python (`requests`, `pandas`, `logging`)
* **Cloud Platform:** Google Cloud Platform
* **Data Storage:** Google Cloud Storage (GCS)
* **Data Warehouse:** BigQuery
* **Workflow Orchestration:** Cloud Scheduler + Cloud Functions
* **Dashboarding:** Looker Studio
* **Version Control:** GitHub


---

## 📊 Features

*  **Automated daily ingestion** of UAE weather & air quality data
*  **Data cleaning & validation** (null checks, type enforcement, deduplication)
*  **Daily CSV snapshots** stored in Google Cloud Storage
*  **BigQuery integration** for scalable querying and analytics
*  **Scheduled orchestration** via Cloud Scheduler + Cloud Functions
*  **Interactive Looker Studio Dashboard** with daily pollution alerts & trends

---

## 🗄️ BigQuery Schema

| Column                 | Type      | Description                             |
| ---------------------- | --------- | --------------------------------------- |
| timestamp              | TIMESTAMP | Hourly UTC timestamp (Dubai TZ applied) |
| temperature\_2m        | FLOAT     | 2m above ground temperature (°C)        |
| apparent\_temperature  | FLOAT     | Feels-like temperature (°C)             |
| relative\_humidity\_2m | FLOAT     | Humidity (%)                            |
| pm10                   | FLOAT     | Particulate matter ≤10 µm (µg/m³)       |
| pm2\_5                 | FLOAT     | Particulate matter ≤2.5 µm (µg/m³)      |
| date                   | DATE      | Observation date                        |

---

## 📈 Example Dashboard (Looker Studio)

![Dashboard](dashboard.png)
*Interactive Looker Studio dashboard displaying temperature & pollution trends across the UAE.*

---

## 🔒 Data Governance

| Aspect         | Implementation                                       |
| -------------- | ---------------------------------------------------- |
| Data Quality   | Null checks, schema enforcement, deduplication       |
| Access Control | IAM roles for Data Engineer, Analyst, Viewer         |
| Logging        | Python logging & Cloud Logging                       |
| Retention      | GCS lifecycle rules (optional cleanup after 30 days) |

---

## 🚨 Alerting & Monitoring

To ensure reliability and visibility of the pipeline, log-based alerting was implemented using Cloud Logging and Cloud Monitoring:

🔍 Log-Based Metrics

Two custom log-based metrics were defined:

Function Errors

Filter:

resource.type="cloud_run_revision"
resource.labels.service_name="uae-weather-etl-pipeline"
severity="ERROR"


Purpose: Captures any error logs from the Cloud Function (uae-weather-etl-pipeline).

Cloud Function Failures (Custom Text Match)

Filter:

resource.type="cloud_run_revision"
resource.labels.service_name="uae-weather-etl-pipeline"
textPayload:"Cloud Function failed"


Purpose: Specifically matches explicit failure messages in the function logs.

⏰ Scheduler Failure Alerts

A dedicated alert policy was created for the Cloud Scheduler job (uae-weather-daily-job):

Filter:

resource.type="cloud_scheduler_job"
resource.labels.job_id="uae-weather-daily-job"
severity="ERROR"


Purpose: Triggers an alert when the Scheduler fails to invoke the daily Cloud Function.

📩 Notifications

Alerts are configured to send email notifications to the pipeline owner.

Severity levels were assigned:

Critical → Scheduler or Function failure

Warning → Non-blocking errors

⚡ Response Playbook

When an alert is triggered:

Inspect logs in Cloud Logging Explorer.

If the error is Scheduler-related, manually trigger the job:

gcloud scheduler jobs run uae-weather-daily-job \
    --location=us-central1 \
    --project=skypulse-uae


If the error is from the Cloud Function, re-run it manually or re-deploy if needed.

## 🧑‍💻 Author

**Adam Benhalid**
Data Engineer | Abu Dhabi, UAE
📧 [adambenhalid@gmail.com](mailto:adambenhalid@gmail.com)

