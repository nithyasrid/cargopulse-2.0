"""
Load curated PostgreSQL tables into BigQuery.

Run locally after installing:
    pip install google-cloud-bigquery pandas psycopg2-binary

Required environment variables:
    GCP_PROJECT_ID
    BIGQUERY_DATASET
    GOOGLE_APPLICATION_CREDENTIALS
"""

import os
import pandas as pd
import psycopg2
from google.cloud import bigquery

PROJECT = os.environ["GCP_PROJECT_ID"]
DATASET = os.getenv("BIGQUERY_DATASET", "cargopulse")

def pg_connection():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", "5432"),
        dbname=os.getenv("POSTGRES_DB", "cargopulse"),
        user=os.getenv("POSTGRES_USER", "cargopulse"),
        password=os.getenv("POSTGRES_PASSWORD", "cargopulse"),
    )

def load_table(table_name):
    with pg_connection() as conn:
        df = pd.read_sql(f"SELECT * FROM {table_name}", conn)

    client = bigquery.Client(project=PROJECT)
    dataset_ref = f"{PROJECT}.{DATASET}"
    client.create_dataset(bigquery.Dataset(dataset_ref), exists_ok=True)

    table_ref = f"{dataset_ref}.{table_name}"
    job = client.load_table_from_dataframe(
        df,
        table_ref,
        job_config=bigquery.LoadJobConfig(
            write_disposition="WRITE_TRUNCATE"
        ),
    )
    job.result()
    print(f"Loaded {len(df)} rows into {table_ref}")

if __name__ == "__main__":
    for table in ["shipments", "shipment_events", "shipment_analytics", "supply_chain_kpis"]:
        load_table(table)
