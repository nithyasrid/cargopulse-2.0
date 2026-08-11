# CargoPulse 2.0 — Smart Supply Chain Intelligence Platform

**Primary Track:** Data Engineering  
**Secondary Track:** Java Backend / SDE

CargoPulse is an event-driven supply-chain platform that ingests shipment, warehouse, and inventory events through Kafka, processes them with Spark, orchestrates batch analytics with Airflow, stores operational data in PostgreSQL, and provides a BigQuery loader for GCP deployment.

## Architecture

```text
                    CargoPulse 2.0
                         |
             +-----------+-----------+
             |                       |
       Spring Boot API          Event Producer
             |                       |
             +-----------+-----------+
                         |
                       Kafka
                         |
                  Spark Streaming
                         |
                 Data Transformation
                         |
                    PostgreSQL
                         |
                +--------+--------+
                |                 |
             Airflow          Dashboard
                |
          KPI / Analytics
                |
             BigQuery
                |
                GCP Analytics
```

## Included modules

- Kafka shipment event producer
- Kafka topics and event schemas
- PySpark Structured Streaming processor
- PostgreSQL operational/analytics database
- Airflow KPI DAG
- Java Spring Boot REST API
- Streamlit analytics dashboard
- BigQuery batch loader
- Docker Compose local environment
- Tests and sample data

## Requirements

- Docker Desktop
- Docker Compose
- Git

Optional for development outside Docker:

- Python 3.11+
- Java 17+
- Maven 3.9+
- Google Cloud SDK

## Quick start

```bash
git clone <your-repository-url>
cd CargoPulse-2.0

docker compose up --build
```

This starts the API, Kafka, PostgreSQL, Spark streaming job, Airflow, and dashboard.

Services:

- API: http://localhost:8080
- Dashboard: http://localhost:8501
- Airflow: http://localhost:8081
- PostgreSQL: localhost:5432
- Kafka: localhost:9092

Airflow login:

```text
username: admin
password: admin
```

The API automatically creates the required PostgreSQL tables.

## Configure Airflow

After the containers start:

```bash
bash setup-airflow.sh
```

Then open Airflow and enable `cargopulse_daily_kpis`.

## Create a shipment

```bash
curl -X POST http://localhost:8080/api/v1/shipments \
  -H "Content-Type: application/json" \
  -d '{
    "shipmentId":"SHP-1001",
    "orderId":"ORD-5001",
    "origin":"Chennai",
    "destination":"Bengaluru",
    "warehouse":"WH-01",
    "status":"IN_TRANSIT",
    "expectedDelivery":"2026-08-15T18:00:00"
  }'
```

The API stores the shipment and publishes a Kafka `shipment-events` message.

## Generate demo events

```bash
docker compose run --rm event-producer
```

Or call:

```bash
curl -X POST http://localhost:8080/api/v1/demo/generate?count=20
```

## View analytics

Open:

```text
http://localhost:8501
```

## BigQuery / GCP

Local mode uses PostgreSQL so the whole project runs without cloud credentials.

For GCP:

1. Create a GCP project.
2. Enable BigQuery API.
3. Create dataset `cargopulse`.
4. Create a service account with BigQuery Data Editor and Job User permissions.
5. Download its JSON key.
6. Set:

```bash
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
export GCP_PROJECT_ID=your-project-id
export BIGQUERY_DATASET=cargopulse
```

Then run:

```bash
python warehouse/bigquery_loader.py
```

## Main API endpoints

```text
GET    /api/v1/shipments
GET    /api/v1/shipments/{shipmentId}
POST   /api/v1/shipments
PUT    /api/v1/shipments/{shipmentId}/status
GET    /api/v1/analytics/kpis
GET    /api/v1/analytics/delays
POST   /api/v1/demo/generate
GET    /health
```

## Data flow

1. Spring Boot receives shipment events.
2. Spring Boot persists the operational shipment record.
3. Spring Boot publishes an event to Kafka.
4. Spark consumes Kafka events.
5. Spark validates and transforms the event.
6. Spark writes curated records to PostgreSQL.
7. Airflow calculates supply-chain KPIs.
8. Streamlit reads KPI and shipment tables.
9. BigQuery loader exports curated data to GCP.

## Resume positioning

### Data Engineering

> Built an event-driven supply-chain intelligence platform using Kafka, PySpark, Airflow, PostgreSQL, BigQuery and GCP to process shipment events, automate KPI pipelines, and deliver delivery, warehouse and inventory analytics.

### Java Backend / SDE

> Built a Spring Boot microservice exposing shipment and analytics REST APIs, integrating PostgreSQL persistence with Kafka-based event publishing and asynchronous data processing.

## Disclaimer

This repository is a complete local development MVP. Cloud deployment, authentication, secrets management, observability, and high-availability settings should be hardened before production use.
