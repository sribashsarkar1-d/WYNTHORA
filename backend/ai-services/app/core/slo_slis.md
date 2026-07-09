# Enterprise SLIs & SLOs (Service Level Indicators & Objectives)

## 99.99% API Uptime Strategy (Four Nines)
- **Allowed Downtime**: 52.60 minutes per year (~4.38 minutes per month)
- **Architecture**:
  - Multi-AZ Deployment (Kubernetes)
  - Active-Active Database Replication (PostgreSQL with read replicas)
  - Redis Cluster for High Availability Caching
  - Automated Failover & Disaster Recovery via AWS Route 53 / Azure Traffic Manager

## Service Level Indicators (SLIs)
1. **API Error Rate**: (Count of 5xx HTTP responses / Total HTTP responses) * 100
2. **API Latency**: The 99th percentile (P99) of HTTP request duration in milliseconds.
3. **Simulation Tick Lag**: Time taken for the simulation worker to process a tick minus expected processing time.
4. **Data Freshness**: Time since the last successful Data Warehouse ingestion.

## Service Level Objectives (SLOs)
1. **API Error Rate SLO**: < 0.1% of all requests over a 30-day rolling window.
2. **API Latency SLO**: P99 latency < 200ms for read endpoints (`/status`, `/forecasts/risk`) over a 7-day rolling window.
3. **Simulation Tick Lag SLO**: Simulation ticks drift no more than 500ms behind real-time pacing.
4. **Data Freshness SLO**: Core economic indicators (IMF/NOAA data) are no more than 24 hours stale.

## Monitoring & Alerting
- Prometheus metrics are exposed at `/metrics`.
- OpenTelemetry traces track request lifecycles.
- AlertManager triggers PagerDuty for critical SLO breaches (e.g., Error Rate > 1% in a 5-minute window).
