import json
import os
import random
import time
import uuid
from datetime import datetime, timezone, timedelta

from kafka import KafkaProducer

BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
TOPIC = os.getenv("KAFKA_TOPIC", "shipment-events")

producer = KafkaProducer(
    bootstrap_servers=BOOTSTRAP,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    key_serializer=lambda v: v.encode("utf-8"),
)

statuses = ["PICKED_UP", "IN_TRANSIT", "AT_WAREHOUSE", "OUT_FOR_DELIVERY", "DELIVERED", "DELAYED"]
locations = ["Chennai", "Bengaluru", "Coimbatore", "Hyderabad", "Mumbai"]

for i in range(20):
    shipment_id = f"SHP-DEMO-{i+1:04d}"
    event = {
        "eventId": str(uuid.uuid4()),
        "shipmentId": shipment_id,
        "eventType": random.choice(statuses),
        "eventTimestamp": datetime.now(timezone.utc).replace(tzinfo=None).isoformat(),
        "location": random.choice(locations),
        "status": random.choice(statuses),
        "origin": "Chennai",
        "destination": random.choice(["Bengaluru", "Hyderabad", "Mumbai"]),
    }
    producer.send(TOPIC, key=shipment_id, value=event)
    print(event)
    time.sleep(0.25)

producer.flush()
producer.close()
print("Demo events published.")
