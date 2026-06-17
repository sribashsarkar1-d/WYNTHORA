# World Simulation Engine
## Developer Guide & Comprehensive Project Structure

Welcome to the **World Simulation Engine** repository. This document serves as the ultimate guide for any new developer joining the project. By reading this, you will understand exactly how the project is structured, what technologies are used, and where you need to write your code.

---

## 🏗️ 1. High-Level Architecture & Tech Stack

This project uses a modern, enterprise-grade **Polyglot Microservices** architecture.

- **Core Engine (Backend):** `Go (Golang)` - Handles all incoming HTTP requests, Authentication, Billing, and high-concurrency WebSockets.
- **AI Services (Backend):** `Python 3.10+, FastAPI, PyTorch, Ray, Mesa` - Handles Agent-Based Modeling (ABM), Reinforcement Learning (RL), and Neural Networks.
- **Data Pipeline (Backend):** `Python, Apache Airflow, PySpark` - Handles scheduled ingestion of massive real-time datasets (Economy, Climate) from external APIs.
- **Frontend Dashboard:** `Next.js (React), TypeScript, Tailwind CSS` - The user interface for interacting with the simulation.
- **Database:** `PostgreSQL` (Relational), `Redis` (Caching).
- **Communication:** `gRPC / Protocol Buffers` for fast internal microservice communication.

---

## 📂 2. Detailed Folder Structure

```text
C:\World Simulation Engine\
│
├── backend/
│   ├── core-engine/         (Go - Main API & WebSockets)
│   ├── ai-services/         (Python - AI/ML Inference)
│   └── data-pipeline/       (Python - Airflow & Data Processing)
│
├── frontend/
│   └── dashboard/           (Next.js - User Interface)
│
├── shared/
│   └── proto/               (gRPC Protocol Buffers definitions)
│
├── database/
│   ├── migrations/          (SQL scripts to create/drop tables)
│   └── seeds/               (Dummy data for testing)
│
├── infrastructure/
│   ├── k8s/                 (Kubernetes deployment manifests)
│   ├── terraform/           (IaC for Cloud deployment)
│   └── docker/              (Global docker configurations)
│
├── docs/                    (Project Documentation)
│
├── .github/
│   └── workflows/           (CI/CD pipelines for GitHub Actions)
│
└── docker-compose.yml       (Run the entire stack locally)
```

---

## 🛠️ 3. Where to Write What Code? (Developer Guide)

If you have a task assigned to you, find the relevant section below to know exactly which folder and file you should edit.

### A. Core Engine (Go) `backend/core-engine/`
This service follows **Clean Architecture**.
- **Adding a new API Route?** Go to `internal/api/routes.go` and map your URL.
- **Writing HTTP Request Logic?** Create a handler in `internal/api/handlers/`.
- **Writing Core Business Logic?** Put it in `internal/core/services/` (e.g., simulation logic, billing logic).
- **Defining a Database Model?** Add it to `internal/core/domain/`.
- **Connecting to a new DB/External API?** Write the connection code in `internal/infrastructure/`.
- **WebSocket Logic?** Look inside `internal/infrastructure/websocket/`.

### B. AI Services (Python) `backend/ai-services/`
This service follows **Domain-Driven Design**.
- **Adding a new AI API endpoint?** Add it inside `app/api/v1/endpoints/` (e.g., `inference.py`).
- **Writing Agent-Based Modeling logic?** Write your Mesa models inside `app/services/agent_modeling/`.
- **Writing Neural Networks / Graph Logic?** Use PyTorch inside `app/services/gnn/` or `app/services/rl_engine/`.
- **Changing API Input/Output JSON?** Update the Pydantic classes in `app/models/domain.py`.

### C. Data Pipeline (Python) `backend/data-pipeline/`
- **Adding a new daily scheduled task?** Create a new DAG file in `dags/` (e.g., `climate_dag.py`).
- **Writing complex Data Cleaning logic?** Write a PySpark job inside `scripts/spark_jobs/`.
- **Adding custom Airflow connections?** Use `plugins/hooks/` and `plugins/operators/`.

### D. Frontend Dashboard (Next.js) `frontend/dashboard/`
- **Creating a new Page?** Add it inside the Next.js App Router structure in `src/app/`.
- **Creating a reusable UI component?** Put it in `src/components/`.
- **Styling changes?** Modify the Tailwind classes in your components or edit `tailwind.config.ts`.
- **Managing Global State?** Use Zustand or Context API inside a `src/store/` directory.

### E. Database Changes `database/migrations/`
- **Need to add a new column or table?** DO NOT manually create it in the database. Instead, create a new SQL migration file (e.g., `000002_add_billing.up.sql`) inside `database/migrations/`.

### F. Microservice Communication `shared/proto/`
- **Need Go and Python to talk to each other?** Define your data structures and functions in `shared/proto/simulation.proto`. Both Go and Python will auto-generate their client code from this file.

---

## 🚀 4. How to Run the Project Locally

1. **Install Prerequisites:** Docker, Docker Compose, Go (1.22+), Python (3.10+), Node.js.
2. **Run the full stack via Docker:**
   Open a terminal in the root `C:\World Simulation Engine\` directory and run:
   ```bash
   docker-compose up --build
   ```
3. **Run Individually (For Development):**
   - **Frontend:** `cd frontend/dashboard` -> `npm run dev`
   - **AI Services:** `cd backend/ai-services` -> activate venv -> `uvicorn app.main:app --reload`
   - **Core Engine:** `cd backend/core-engine` -> `go run cmd/server/main.go`

---
*Maintained by the World Simulation Engine Architecture Team.*
