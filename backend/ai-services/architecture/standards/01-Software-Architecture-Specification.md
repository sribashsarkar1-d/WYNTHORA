# Software Architecture Specification (SAS)
## Wynthora World Simulation Engine

### 1. Introduction
The Wynthora World Simulation Engine is a production-grade Enterprise Data Platform designed to power a Digital Twin Earth simulation. This document serves as the ultimate source of truth for the system's architectural design.

### 2. Architectural Principles
- **Clean Architecture & DDD:** Strict boundary enforcement across domains (Economy, Climate, Trade, Politics, etc.).
- **Async-First:** Asynchronous processing across all I/O bound operations (FastAPI, AsyncPG, httpx).
- **Repository Pattern:** Services must never access databases directly; all access is abstracted via repositories.
- **Fail-Safe & Resilient:** Centralized API rate limiters, retries (Tenacity), and circuit breakers to ensure high availability.

### 3. System Components
#### 3.1 Data Ingestion Layer
- **Plugins (`app/plugins/`)**: `BaseDataSource` implementations for WorldBank, GDELT, Yahoo, etc.
- **Normalizers (`app/normalizers/`)**: Transform raw heterogeneous JSON into standardized Pydantic schemas.
- **Validators (`app/validators/`)**: Quality checks preventing dirty data insertion.

#### 3.2 Data Lake & Warehouse
- **Raw Storage (`storage/raw/`)**: Immutable archive of original API responses.
- **PostgreSQL Warehouse**: Normalized historical tracking using bulk UPSERTs and partitioning readiness.

#### 3.3 Application Layer
- **Services (`app/services/`)**: Core business logic.
- **Domains (`app/domains/`)**: Aggregated business context encapsulating models, logic, and persistence.

### 4. Future AI & Scaling Readiness (Phases 2-4)
- **Feature Store & ML Pipeline**: Generates features like GDP Growth, War Index.
- **Message Queues**: RabbitMQ/Kafka abstract interfaces prepared.
- **Monitoring Stack**: Prometheus, Grafana, OpenTelemetry hooks designed into the core system.

### 5. Constraint & Limitations
- Never remove working code; maintain backward compatibility.
- Ensure API keys are injected via `Pydantic Settings` and `.env`, never hardcoded.
