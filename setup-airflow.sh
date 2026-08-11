#!/usr/bin/env bash
set -e
docker compose exec airflow airflow connections delete postgres_default || true
docker compose exec airflow airflow connections add postgres_default \
  --conn-type postgres \
  --conn-host postgres \
  --conn-schema cargopulse \
  --conn-login cargopulse \
  --conn-password cargopulse \
  --conn-port 5432
echo "Airflow postgres_default connection configured."
