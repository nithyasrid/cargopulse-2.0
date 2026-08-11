from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

POSTGRES_CONN = "postgres_default"

with DAG(
    dag_id="cargopulse_daily_kpis",
    start_date=datetime(2026, 1, 1),
    schedule="*/15 * * * *",
    catchup=False,
    default_args={"retries": 2, "retry_delay": timedelta(minutes=2)},
    tags=["cargopulse", "supply-chain", "data-engineering"],
) as dag:

    calculate_kpis = SQLExecuteQueryOperator(
        task_id="calculate_supply_chain_kpis",
        conn_id=POSTGRES_CONN,
        sql="""
        INSERT INTO supply_chain_kpis (
            metric_date,
            total_shipments,
            delivered_shipments,
            delayed_shipments,
            on_time_rate,
            average_delay_minutes,
            calculated_at
        )
        SELECT
            CURRENT_DATE,
            COUNT(*),
            COUNT(*) FILTER (WHERE status = 'DELIVERED'),
            COUNT(*) FILTER (WHERE status = 'DELAYED'),
            CASE
                WHEN COUNT(*) = 0 THEN 0
                ELSE ROUND(
                    (COUNT(*) FILTER (WHERE status = 'DELIVERED')::numeric
                    / COUNT(*)::numeric) * 100, 2
                )
            END,
            COALESCE(AVG(delay_minutes), 0),
            NOW()
        FROM shipments s
        LEFT JOIN shipment_analytics a
          ON a.shipment_id = s.shipment_id
        ON CONFLICT (metric_date) DO UPDATE SET
            total_shipments = EXCLUDED.total_shipments,
            delivered_shipments = EXCLUDED.delivered_shipments,
            delayed_shipments = EXCLUDED.delayed_shipments,
            on_time_rate = EXCLUDED.on_time_rate,
            average_delay_minutes = EXCLUDED.average_delay_minutes,
            calculated_at = NOW();
        """,
    )
