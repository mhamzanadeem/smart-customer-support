# Smart Customer Support & Knowledge Management System

AI-powered customer support system using RAG, LangGraph, multiple agents, MongoDB Atlas, and OpenAI.

## Features

- **RAG** — Retrieval-Augmented Generation with MongoDB Atlas Vector Search
- **LangGraph** — Workflow orchestration with conditional routing
- **Multi-agent architecture** — Router, RAG, Technical, Escalation, and Learning agents
- **FastAPI** — High-performance async Python API
- **OpenAI** — LLM and embeddings
- **MongoDB Atlas** — Vector search + conversation storage
- **Next.js frontend** — Deployed on Vercel
- **Render backend** — Deployed on Render

## Architecture

```text
                         ┌──────────────────┐
                         │     Vercel       │
                         │    Frontend      │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │      Render      │
                         │     FastAPI      │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │    LangGraph     │
                         └────────┬─────────┘
                                  │
                         ┌────────▼────────┐
                         │  Router Agent   │
                         └────────┬────────┘
                                  │
              ┌───────────────────┼───────────────────┐
              ▼                   ▼                   ▼
        ┌──────────┐       ┌──────────────┐    ┌─────────────┐
        │ RAG Agent│       │Technical     │    │ Escalation  │
        │          │       │Agent         │    │ Agent       │
        └────┬─────┘       └──────────────┘    └─────────────┘
             │
             ▼
      ┌─────────────────┐
      │  MongoDB Atlas  │
      │ Vector Search   │
      └─────────────────┘
```

## Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- MongoDB Atlas account
- OpenAI API key

### Backend

```powershell
git clone YOUR_REPOSITORY_URL
cd smart_customer_support\backend

python -m venv .venv
.\.venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

Create `.env` from `.env.example` and fill in your values:

```powershell
copy .env.example .env
```

Run the backend:

```powershell
python -m uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```powershell
cd ..\frontend

npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

## Windows PowerShell Commands

### Create virtual environment

```powershell
python -m venv .venv
```

### Activate

```powershell
.\.venv\Scripts\Activate.ps1
```

### Install dependencies

```powershell
pip install -r requirements.txt
```

### Run tests

```powershell
python -m pytest tests/ -q
```

### Start backend

```powershell
python -m uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

### Health check

```powershell
Invoke-RestMethod http://localhost:8000/health
```

### Keepalive

```powershell
Invoke-RestMethod http://localhost:8000/api/keepalive
```

### Chat test

```powershell
$body = @{
    query = "How do I reset my password?"
} | ConvertTo-Json

Invoke-RestMethod `
    -Uri "http://localhost:8000/api/chat" `
    -Method POST `
    -ContentType "application/json" `
    -Body $body
```

### Ingest documents

```powershell
python scripts/ingest.py --folder .\data
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Root — service info |
| GET | `/health` | Health check |
| POST | `/api/chat` | Main chat endpoint |
| GET | `/api/keepalive` | Lightweight keepalive |
| GET | `/api/debug/ping` | Backend reachability test |
| GET | `/api/debug/openai` | OpenAI connectivity test |
| GET | `/api/debug/mongodb` | MongoDB connectivity test |
| POST | `/api/debug/llm` | LLM-only test (no RAG) |

## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for full deployment instructions.

### Render (Backend)

| Setting | Value |
|---------|-------|
| Root Directory | `backend` |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `uvicorn src.api.main:app --host 0.0.0.0 --port $PORT` |

### Vercel (Frontend)

| Setting | Value |
|---------|-------|
| Root Directory | `frontend` |
| Framework | Next.js |
| Environment Variable | `NEXT_PUBLIC_API_URL=https://YOUR-RENDER-URL.onrender.com` |

## Project Structure

```text
smart_customer_support/
├── backend/
│   ├── src/
│   │   ├── agents/          # Agent implementations
│   │   ├── api/             # FastAPI routes
│   │   ├── graph/           # LangGraph workflow
│   │   ├── models/          # Pydantic schemas
│   │   ├── rag/             # RAG + embeddings
│   │   ├── services/        # Database, LLM, logging
│   │   └── mcp/             # MCP tools
│   ├── scripts/             # Ingestion scripts
│   ├── tests/               # Test suite
│   └── requirements.txt
├── frontend/
│   ├── app/                 # Next.js App Router
│   │   ├── components/      # React components
│   │   ├── page.tsx
│   │   └── layout.tsx
│   └── package.json
├── docs/                    # Documentation
├── render.yaml              # Render configuration
├── DEPLOYMENT.md
└── README.md
```
