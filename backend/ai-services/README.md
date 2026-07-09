# Wynthora AI Services - Enterprise Edition

## Overview
Wynthora AI Services is the backend intelligence engine for the World Simulation platform. It coordinates the complex interplay between Geopolitics, Economics, Society (ABM), and Climate/Energy models, utilizing advanced AI models (GNNs, LSTMs, RL) and formal Finite State Machines.

## Architecture & Production Readiness
This module has been fully refactored for enterprise-grade production:
- **Asynchronous Execution**: Fully async FastAPI framework with Asyncpg/SQLAlchemy ORM.
- **Database**: PostgreSQL with UUIDs, connection pooling, and Alembic migrations.
- **Background Processing**: Celery & Redis for asynchronous ML model training and scheduling.
- **Live Streaming**: WebSocket integration with topic-based subscriptions.
- **AI Forecasting**: Feature Store pulling live DB data into an LSTM Predictor.
- **Security**: JWT-based RBAC Authentication, SlowAPI rate limiting (DDoS protection).
- **Observability**: OpenTelemetry tracing, Prometheus metrics, structured JSON logging.
- **Resiliency**: Automated rollback mechanisms for events, disaster recovery scripts, and robust error handling.

## Deployment
See the `helm/ai-services` chart and `docker-compose.yml` for deploying the application.
- `docker-compose up -d --build`

## Testing
`pytest tests/ -v`

## Compliance
- SLOs & SLIs documented in `app/core/slo_slis.md`
- Security Audit passed (Phase 17).
