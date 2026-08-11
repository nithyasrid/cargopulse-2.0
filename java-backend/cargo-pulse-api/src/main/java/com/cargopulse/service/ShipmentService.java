package com.cargopulse.service;

import com.cargopulse.dto.CreateShipmentRequest;
import com.cargopulse.entity.Shipment;
import com.cargopulse.repository.ShipmentRepository;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.List;
import java.util.NoSuchElementException;
import java.util.UUID;

@Service
public class ShipmentService {
    private final ShipmentRepository repository;
    private final KafkaTemplate<String, String> kafkaTemplate;
    private final String topic;

    public ShipmentService(
            ShipmentRepository repository,
            KafkaTemplate<String, String> kafkaTemplate,
            org.springframework.core.env.Environment env) {
        this.repository = repository;
        this.kafkaTemplate = kafkaTemplate;
        this.topic = env.getProperty("cargopulse.kafka-topic", "shipment-events");
    }

    public Shipment create(CreateShipmentRequest request) {
        if (repository.existsById(request.shipmentId())) {
            throw new IllegalArgumentException("Shipment already exists: " + request.shipmentId());
        }

        Shipment shipment = new Shipment();
        shipment.setShipmentId(request.shipmentId());
        shipment.setOrderId(request.orderId());
        shipment.setOrigin(request.origin());
        shipment.setDestination(request.destination());
        shipment.setWarehouse(request.warehouse());
        shipment.setStatus(request.status());
        shipment.setExpectedDelivery(request.expectedDelivery());

        Shipment saved = repository.save(shipment);
        publishEvent(saved, "SHIPMENT_CREATED");
        return saved;
    }

    public List<Shipment> findAll() {
        return repository.findAll();
    }

    public Shipment find(String id) {
        return repository.findById(id)
                .orElseThrow(() -> new NoSuchElementException("Shipment not found: " + id));
    }

    public Shipment updateStatus(String id, String status) {
        Shipment shipment = find(id);
        shipment.setStatus(status);
        if ("DELIVERED".equalsIgnoreCase(status)) {
            shipment.setActualDelivery(LocalDateTime.now());
        }
        Shipment saved = repository.save(shipment);
        publishEvent(saved, "STATUS_UPDATED");
        return saved;
    }

    public void publishEvent(Shipment shipment, String eventType) {
        String eventId = UUID.randomUUID().toString();
        String timestamp = LocalDateTime.now().toString();
        String json = """
                {
                  "eventId":"%s",
                  "shipmentId":"%s",
                  "eventType":"%s",
                  "eventTimestamp":"%s",
                  "location":"%s",
                  "status":"%s",
                  "origin":"%s",
                  "destination":"%s"
                }
                """.formatted(
                eventId,
                shipment.getShipmentId(),
                eventType,
                timestamp,
                shipment.getWarehouse() == null ? "UNKNOWN" : shipment.getWarehouse(),
                shipment.getStatus(),
                shipment.getOrigin(),
                shipment.getDestination()
        );

        kafkaTemplate.send(topic, shipment.getShipmentId(), json);
    }
}
