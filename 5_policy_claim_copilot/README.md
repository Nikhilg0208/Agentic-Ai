# Async Multimodal Policy & Claim Copilot

An intelligent claims copilot that processes insurance/policy documents (RAG), extracts receipt data using vision models, audits claims with a LangGraph state machine, and processes tasks asynchronously using FastAPI + RQ + Redis with MongoDB persistence.

---

## Step 1: Infrastructure Overview

The local infrastructure runs containerized services managed via Docker Compose:

| Service | Port | Description | Dashboard / Status |
| :--- | :--- | :--- | :--- |
| **Qdrant** | `6333` (REST/Web), `6334` (gRPC) | Vector database for policy chunk embeddings | [http://localhost:6333/dashboard](http://localhost:6333/dashboard) |
| **Redis** | `6381` | In-memory message broker & task queue (RQ) | `redis://localhost:6381/0` |
| **MongoDB** | `27018` | Persistent checkpoint storage for LangGraph agent memory | `mongodb://localhost:27018` |

*(Note: Ports 6381 and 27018 are mapped to avoid collisions with any existing local instances).*

---

## Useful Commands

### 1. Check Service Health
```bash
python3 test_infrastructure.py
```

### 2. Manage Docker Containers
```bash
# Start services in the background
docker compose up -d

# Check container status
docker compose ps

# View service logs
docker compose logs -f

# Stop services
docker compose down
```

---

## Directory Layout
```
5_policy_claim_copilot/
├── docker-compose.yml       # Infrastructure orchestration (Qdrant, Redis, MongoDB)
├── .env                     # Environment settings and connection URLs
├── .env.example             # Example environment template
├── requirements.txt         # Core dependencies
├── test_infrastructure.py   # Connectivity and health check script
├── data/                    # Storage for policy PDFs and sample receipts
└── app/
    ├── config.py            # Pydantic Settings configuration loader
    ├── core/                # Database clients (Redis, Mongo, Qdrant)
    ├── ingestion/           # (Step 2) PDF parsing, chunking, and embedding
    ├── rag/                 # (Step 3) Policy retrieval and grounded Q&A
    ├── vision/              # (Step 4) Receipt image parser using Vision LLM
    ├── audit/               # (Step 5) Claim auditing logic & rules comparison
    ├── agent/               # (Steps 6 & 7) LangGraph agent & MongoDB memory
    ├── workers/             # (Step 8) RQ background worker tasks
    └── api/                 # (Step 9) FastAPI REST endpoints
```
