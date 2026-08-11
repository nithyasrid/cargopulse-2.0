CREATE TABLE IF NOT EXISTS shipments (
    shipment_id VARCHAR(64) PRIMARY KEY,
    order_id VARCHAR(64) NOT NULL,
    origin VARCHAR(128) NOT NULL,
    destination VARCHAR(128) NOT NULL,
    warehouse VARCHAR(64),
    status VARCHAR(32) NOT NULL,
    expected_delivery TIMESTAMP,
    actual_delivery TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS shipment_events (
    event_id VARCHAR(64) PRIMARY KEY,
    shipment_id VARCHAR(64) NOT NULL,
    event_type VARCHAR(64) NOT NULL,
    event_timestamp TIMESTAMP NOT NULL,
    location VARCHAR(128),
    status VARCHAR(32),
    payload JSONB,
    processed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS shipment_analytics (
    shipment_id VARCHAR(64) PRIMARY KEY,
    event_count INTEGER NOT NULL DEFAULT 0,
    latest_event_type VARCHAR(64),
    latest_status VARCHAR(32),
    latest_location VARCHAR(128),
    last_event_timestamp TIMESTAMP,
    delay_minutes DOUBLE PRECISION NOT NULL DEFAULT 0,
    is_delayed BOOLEAN NOT NULL DEFAULT FALSE,
    risk_score DOUBLE PRECISION NOT NULL DEFAULT 0,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS supply_chain_kpis (
    metric_date DATE PRIMARY KEY,
    total_shipments INTEGER NOT NULL DEFAULT 0,
    delivered_shipments INTEGER NOT NULL DEFAULT 0,
    delayed_shipments INTEGER NOT NULL DEFAULT 0,
    on_time_rate DOUBLE PRECISION NOT NULL DEFAULT 0,
    average_delay_minutes DOUBLE PRECISION NOT NULL DEFAULT 0,
    calculated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_events_shipment_id ON shipment_events(shipment_id);
CREATE INDEX IF NOT EXISTS idx_events_timestamp ON shipment_events(event_timestamp);
CREATE INDEX IF NOT EXISTS idx_analytics_delayed ON shipment_analytics(is_delayed);
