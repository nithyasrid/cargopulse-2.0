-- Fact-like event table
CREATE TABLE shipment_events (
    event_id VARCHAR(64) PRIMARY KEY,
    shipment_id VARCHAR(64) NOT NULL,
    event_type VARCHAR(64) NOT NULL,
    event_timestamp TIMESTAMP NOT NULL,
    location VARCHAR(128),
    status VARCHAR(32),
    payload JSONB,
    processed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Shipment operational dimension/entity
CREATE TABLE shipments (
    shipment_id VARCHAR(64) PRIMARY KEY,
    order_id VARCHAR(64) NOT NULL,
    origin VARCHAR(128) NOT NULL,
    destination VARCHAR(128) NOT NULL,
    warehouse VARCHAR(64),
    status VARCHAR(32) NOT NULL,
    expected_delivery TIMESTAMP,
    actual_delivery TIMESTAMP,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);
