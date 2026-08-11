import json
from datetime import datetime

def test_event_has_required_fields():
    event = {
        "eventId": "E1",
        "shipmentId": "S1",
        "eventType": "IN_TRANSIT",
        "eventTimestamp": datetime.now().isoformat(),
        "status": "IN_TRANSIT",
    }

    required = {"eventId", "shipmentId", "eventType", "eventTimestamp", "status"}
    assert required.issubset(event.keys())
    assert event["shipmentId"]
