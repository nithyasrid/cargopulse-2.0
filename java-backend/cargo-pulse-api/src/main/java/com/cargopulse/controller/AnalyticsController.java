package com.cargopulse.controller;

import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/v1/analytics")
public class AnalyticsController {
    private final JdbcTemplate jdbc;

    public AnalyticsController(JdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    @GetMapping("/kpis")
    public List<Map<String, Object>> kpis() {
        return jdbc.queryForList("""
            SELECT metric_date, total_shipments, delivered_shipments,
                   delayed_shipments, on_time_rate, average_delay_minutes
            FROM supply_chain_kpis
            ORDER BY metric_date DESC
            LIMIT 30
        """);
    }

    @GetMapping("/delays")
    public List<Map<String, Object>> delays() {
        return jdbc.queryForList("""
            SELECT shipment_id, latest_status, latest_location,
                   delay_minutes, is_delayed, risk_score
            FROM shipment_analytics
            WHERE is_delayed = TRUE
            ORDER BY risk_score DESC, delay_minutes DESC
            LIMIT 100
        """);
    }
}
