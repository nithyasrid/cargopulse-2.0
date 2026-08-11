package com.cargopulse.dto;

import jakarta.validation.constraints.NotBlank;
import java.time.LocalDateTime;

public record CreateShipmentRequest(
        @NotBlank String shipmentId,
        @NotBlank String orderId,
        @NotBlank String origin,
        @NotBlank String destination,
        String warehouse,
        @NotBlank String status,
        LocalDateTime expectedDelivery
) {}
