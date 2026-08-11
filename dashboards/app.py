import os
import pandas as pd
import psycopg2
import streamlit as st

st.set_page_config(page_title="CargoPulse 2.0", page_icon="🚚", layout="wide")
st.title("🚚 CargoPulse 2.0")
st.caption("Smart Supply Chain Intelligence Platform")

def conn():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", "5432"),
        dbname=os.getenv("POSTGRES_DB", "cargopulse"),
        user=os.getenv("POSTGRES_USER", "cargopulse"),
        password=os.getenv("POSTGRES_PASSWORD", "cargopulse"),
    )

def read_sql(sql):
    with conn() as c:
        return pd.read_sql(sql, c)

try:
    shipments = read_sql("""
        SELECT shipment_id, order_id, origin, destination, warehouse, status,
               expected_delivery, actual_delivery
        FROM shipments
        ORDER BY created_at DESC
        LIMIT 500
    """)

    analytics = read_sql("""
        SELECT shipment_id, latest_status, latest_location,
               delay_minutes, is_delayed, risk_score
        FROM shipment_analytics
        ORDER BY risk_score DESC
        LIMIT 500
    """)

    total = len(shipments)
    delayed = int(analytics["is_delayed"].sum()) if not analytics.empty else 0
    delivered = int((shipments["status"] == "DELIVERED").sum()) if not shipments.empty else 0
    on_time = round((delivered / total) * 100, 2) if total else 0

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Shipments", total)
    c2.metric("Delivered", delivered)
    c3.metric("Delayed", delayed)
    c4.metric("Delivery Rate", f"{on_time}%")

    st.subheader("Shipment Status")
    if not shipments.empty:
        st.bar_chart(shipments["status"].value_counts())

    st.subheader("High-Risk / Delayed Shipments")
    if analytics.empty:
        st.info("No processed analytics yet. Start the Spark stream and generate events.")
    else:
        st.dataframe(analytics, use_container_width=True)

    st.subheader("Recent Shipments")
    st.dataframe(shipments, use_container_width=True)

except Exception as exc:
    st.error(f"Database not ready yet: {exc}")
    st.info("Start the Docker stack and generate demo shipment data.")
