# ADR 001: Transition to Enterprise Asynchronous Architecture

## Status
Accepted

## Context
The AI Services module was originally a proof-of-concept written with synchronous pandas code, mock data, and hardcoded simulation dependencies. To support digital-twin earth scale at production level, we needed robust scalability, state management, and real-time connectivity.

## Decision
1. **Asynchronous Frameworks**: Migrated to FastAPI and Asyncpg for high-throughput, non-blocking I/O.
2. **Database & ORM**: Moved away from mock pandas dataframes to a real PostgreSQL Data Warehouse accessed via a strict Repository Pattern and SQLAlchemy.
3. **Finite State Machines**: Replaced hardcoded `if/else` logic with a structured FSM for managing the Engine Lifecycle (Init -> Loading -> Running -> Error).
4. **AI Layer**: Separated ML processing into a decoupled Feature Store and LSTM Prediction Engine, with heavy model retraining offloaded to Celery worker pools.
5. **Observability**: Mandated OpenTelemetry tracing, Prometheus metrics, and JSON-structured logs to fulfill our 99.99% uptime strategy.

## Consequences
- Requires Redis (for Celery and Caching) and PostgreSQL as strict dependencies.
- Significantly increases code complexity but guarantees data integrity, scalability, and observability.
