package com.cargopulse.controller;

import com.cargopulse.dto.CreateShipmentRequest;
import com.cargopulse.dto.StatusUpdateRequest;
import com.cargopulse.entity.Shipment;
import com.cargopulse.service.ShipmentService;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/v1/shipments")
public class ShipmentController {
    private final ShipmentService service;

    public ShipmentController(ShipmentService service) {
        this.service = service;
    }

    @GetMapping
    public List<Shipment> all() {
        return service.findAll();
    }

    @GetMapping("/{id}")
    public Shipment one(@PathVariable String id) {
        return service.find(id);
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public Shipment create(@Valid @RequestBody CreateShipmentRequest request) {
        return service.create(request);
    }

    @PutMapping("/{id}/status")
    public Shipment updateStatus(
            @PathVariable String id,
            @Valid @RequestBody StatusUpdateRequest request) {
        return service.updateStatus(id, request.status());
    }
}
