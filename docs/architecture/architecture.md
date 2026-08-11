# CargoPulse Architecture

## Layers

### 1. Application layer
Spring Boot exposes REST APIs and publishes business events.

### 2. Event layer
Kafka provides decoupled event transport.

### 3. Processing layer
Spark Structured Streaming validates, transforms and enriches events.

### 4. Orchestration layer
Airflow runs scheduled KPI and warehouse workflows.

### 5. Storage layer
PostgreSQL is used for local operational/analytics workloads. BigQuery is the cloud warehouse.

### 6. Presentation layer
Streamlit provides a lightweight analytics dashboard.

## Core entities

- Shipment
- ShipmentEvent
- ShipmentAnalytics
- SupplyChainKPI

## Production extensions

- Kafka Schema Registry / Avro
- GCP Pub/Sub or managed Kafka
- Dataproc / Serverless Spark
- BigQuery native streaming
- Cloud Composer
- Secret Manager
- IAM least privilege
- OpenTelemetry
- Prometheus/Grafana
- Kubernetes
