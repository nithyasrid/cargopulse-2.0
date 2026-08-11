package com.cargopulse.controller;

import com.cargopulse.dto.CreateShipmentRequest;
import com.cargopulse.service.ShipmentService;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDateTime;
import java.util.Map;
import java.util.Random;

@RestController
@RequestMapping("/api/v1/demo")
public class DemoController {
    private final ShipmentService service;
    private final Random random = new Random();

    public DemoController(ShipmentService service) {
        this.service = service;
    }

    @PostMapping("/generate")
    public Map<String, Object> generate(@RequestParam(defaultValue = "10") int count) {
        int safeCount = Math.min(Math.max(count, 1), 100);
        for (int i = 0; i < safeCount; i++) {
            String id = "SHP-" + System.currentTimeMillis() + "-" + i;
            service.create(new CreateShipmentRequest(
                    id,
                    "ORD-" + (10000 + random.nextInt(90000)),
                    random.nextBoolean() ? "Chennai" : "Coimbatore",
                    random.nextBoolean() ? "Bengaluru" : "Hyderabad",
                    "WH-0" + (1 + random.nextInt(3)),
                    random.nextInt(10) < 2 ? "DELAYED" : "IN_TRANSIT",
                    LocalDateTime.now().plusHours(24 + random.nextInt(72))
            ));
        }
        return Map.of("generated", safeCount);
    }
}
