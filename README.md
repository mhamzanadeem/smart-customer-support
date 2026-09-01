# 🤖 Smart Customer Support & Knowledge Management System

> **AI Agent Capstone Project — RAG + LangGraph + OpenAI Agents SDK**

An end-to-end AI-powered customer support and knowledge management platform that answers customer questions using internal company documentation, troubleshoots technical issues using tools, escalates complex problems to human support, and generates reusable knowledge from resolved interactions.

The project is designed to run locally in minutes and can be deployed using free-tier infrastructure such as **Supabase** and **Render**.

---

# 📋 Table of Contents

1. [Project Overview](#-project-overview)
2. [Problem Statement](#-problem-statement)
3. [Solution](#-solution)
4. [Key Features](#-key-features)
5. [Technology Stack](#-technology-stack)
6. [Architecture](#-architecture)
7. [Agent Architecture](#-agent-architecture)
8. [Workflow](#-workflow)
9. [Project Structure](#-project-structure)
10. [Prerequisites](#-prerequisites)
11. [Supabase Setup](#-supabase-setup)
12. [Local Installation](#-local-installation)
13. [Environment Variables](#-environment-variables)
14. [PDF Knowledge Ingestion](#-pdf-knowledge-ingestion)
15. [Running the Backend](#-running-the-backend)
16. [Running the Frontend](#-running-the-frontend)
17. [API Documentation](#-api-documentation)
18. [API Examples](#-api-examples)
19. [Example Queries](#-example-queries)
20. [Testing](#-testing)
21. [Docker](#-docker)
22. [Render Deployment](#-render-deployment)
23. [Production Configuration](#-production-configuration)
24. [Error Handling](#-error-handling)
25. [Logging](#-logging)
26. [Security](#-security)
27. [Performance Metrics](#-performance-metrics)
28. [Acceptance Criteria](#-acceptance-criteria)
29. [Future Improvements](#-future-improvements)
30. [Case Study](#-case-study)
31. [Troubleshooting](#-troubleshooting)
32. [Conclusion](#-conclusion)

---

# 🚀 Project Overview

The **Smart Customer Support & Knowledge Management System** is an AI-agent platform designed to automate customer support while keeping responses grounded in company documentation.

The system combines three major AI technologies:

* **Retrieval-Augmented Generation (RAG)**
* **LangGraph**
* **OpenAI Agents SDK**

The application supports three primary request types:

```text
FAQ
Technical Support
Complex / Human Escalation
```

The system can:

* Search internal PDF documentation.
* Perform semantic vector search.
* Answer documentation-based questions.
* Diagnose common technical errors.
* Execute tools through AI agents.
* Escalate complex problems.
* Generate simulated support tickets.
* Maintain workflow state.
* Generate knowledge-base candidates from successful interactions.
* Display retrieved sources.
* Display the LangGraph execution trace.

---

# 🎯 Problem Statement

Companies receive hundreds or thousands of customer-support requests every day.

Many of these requests are repetitive:

```text
How do I reset my password?

What is your refund policy?

How can I cancel my subscription?

Where can I find the API documentation?
```

However, other requests require technical investigation:

```text
Why am I receiving HTTP 401?

Why does the API return HTTP 429?

Why is the integration timing out?

Why is the database unavailable?
```

Some cases should not be handled entirely by AI:

```text
I need a human manager.

I want to file a formal complaint.

This is a security issue.

I need someone from the legal team.
```

Traditional chatbots usually struggle because they:

1. Do not have access to private company documentation.
2. Cannot reliably distinguish simple and complex requests.
3. Have no stateful workflow.
4. Cannot perform useful tools.
5. Cannot escalate intelligently.
6. Do not learn from previous support interactions.

This project addresses those limitations.

---

# 💡 Solution

The system creates an AI support pipeline:

```text
Customer
   |
   v
Streamlit UI
   |
   v
FastAPI
   |
   v
LangGraph
   |
   v
Query Classification
   |
   +------------------+
   |                  |
   v                  v
FAQ              Technical
   |                  |
   v                  v
RAG Agent       Technical Agent
   |                  |
   v                  v
Supabase         Diagnostic Tool
pgvector              |
   |                  v
   |              Resolution?
   |              /          \
   |            Yes           No
   |             |             |
   +-------> Learning      Escalation
               Agent           |
                 |             v
                 v         Human Review
             Knowledge          |
             Candidate          v
                            Support Ticket
```

---

# ✨ Key Features

## RAG

The system supports:

* PDF ingestion.
* Text extraction.
* Text chunking.
* OpenAI embeddings.
* Supabase vector storage.
* pgvector similarity search.
* Retrieval thresholds.
* Top-K document retrieval.

---

## LangGraph

LangGraph manages:

* Stateful workflows.
* Conditional routing.
* Multi-step processing.
* Technical resolution decisions.
* Escalation paths.
* Thread IDs.
* Checkpoint-ready architecture.

---

## OpenAI Agents SDK

The system contains multiple specialized agents:

```text
RAG Agent
Technical Agent
Escalation Agent
Learning Agent
```

Agents can execute tools when necessary.

---

## Human Escalation

Complex issues are converted into a structured escalation package.

The application simulates ticket creation:

```text
SUP-XXXXXXXX
```

Example:

```text
SUP-8A12C9EF
```

---

## Knowledge Learning

After a successful interaction, the Learning Agent creates a candidate knowledge article.

Example:

```text
TITLE:
Resolving AUTH-401 API Errors

ARTICLE:
AUTH-401 normally indicates an authentication
failure. Verify token expiration, credentials,
and clock synchronization...
```

The candidate can later be reviewed by a human before publishing.

---

# 🧠 Technology Stack

| Component        | Technology        |
| ---------------- | ----------------- |
| Frontend         | Streamlit         |
| Backend          | FastAPI           |
| Workflow         | LangGraph         |
| Agent Framework  | OpenAI Agents SDK |
| LLM              | OpenAI            |
| Optional LLM     | Groq              |
| Embeddings       | OpenAI Embeddings |
| Vector Database  | Supabase          |
| Vector Engine    | pgvector          |
| PDF Processing   | pypdf             |
| Validation       | Pydantic          |
| Testing          | Pytest            |
| Containerization | Docker            |
| Deployment       | Render            |

---

# 🏗 Architecture

```mermaid
flowchart TD

    USER[Customer]

    UI[Streamlit Frontend]

    API[FastAPI Backend]

    GRAPH[LangGraph Orchestrator]

    ROUTER[Query Classification]

    RAG[RAG Agent]

    TECH[Technical Agent]

    ESC[Escalation Agent]

    LEARN[Learning Agent]

    VECTOR[Supabase pgvector]

    EMBED[OpenAI Embeddings]

    TOOL[Diagnostic Tool]

    TICKET[Human Review / Ticket]

    USER --> UI

    UI --> API

    API --> GRAPH

    GRAPH --> ROUTER

    ROUTER -->|FAQ| RAG

    ROUTER -->|Technical| TECH

    ROUTER -->|Escalation| ESC

    RAG --> EMBED

    EMBED --> VECTOR

    VECTOR --> RAG

    TECH --> TOOL

    TECH --> VECTOR

    TECH --> LEARN

    RAG --> LEARN

    ESC --> TICKET

    LEARN --> VECTOR
```

---

# 🤖 Agent Architecture

## 1. RAG Agent

Responsibilities:

* Search company documentation.
* Read retrieved passages.
* Answer customer questions.
* Avoid unsupported claims.

Tool:

```text
semantic_search
```

---

## 2. Technical Agent

Responsibilities:

* Diagnose technical problems.
* Analyze common error codes.
* Provide troubleshooting steps.
* Decide whether escalation is necessary.

Tool:

```text
diagnose_error
```

Supported demo errors:

```text
AUTH-401
RATE-429
DB-503
TIMEOUT
```

---

## 3. Escalation Agent

Responsibilities:

* Summarize the customer's problem.
* Include relevant evidence.
* Include attempted troubleshooting.
* Prepare a human handoff.

---

## 4. Learning Agent

Responsibilities:

* Analyze successful interactions.
* Identify reusable information.
* Create knowledge-base candidates.
* Avoid exposing secrets or personal information.

---

# 🔄 Workflow

The LangGraph workflow is:

```text
START
  |
  v
classify_query
  |
  +----------+-------------+
  |          |             |
 FAQ     Technical     Escalation
  |          |             |
  v          v             v
RAG       Technical     Escalation
Agent       Agent         Agent
  |          |             |
  |       resolved?        |
  |       /      \         |
  |     yes       no       |
  |      |         |       |
  +------|---------|-------+
         |         |
         v         v
       Learning  Human
       Agent     Review
         |         |
         v         v
        END       END
```

---

# 📁 Project Structure

```text
smart-customer-support/
│
├── src/
│   │
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── base_agent.py
│   │   ├── orchestrator.py
│   │   └── worker_agents.py
│   │
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── search_tool.py
│   │   ├── analysis_tool.py
│   │   └── rag_tool.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── schemas.py
│   │   └── context.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── logging_config.py
│   │   ├── llm_service.py
│   │   └── vector_store.py
│   │
│   └── api/
│       ├── __init__.py
│       ├── routes.py
│       └── main.py
│
├── supabase/
│   └── schema.sql
│
├── tests/
│   ├── test_agents.py
│   └── test_integration.py
│
├── docs/
│   └── case_study.md
│
├── data/
│
├── ingest.py
├── streamlit_app.py
├── Dockerfile
├── docker-compose.yml
├── deploy.sh
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

# 💻 Prerequisites

Install the following:

* Python 3.12+
* Git
* Docker Desktop — optional
* Supabase account
* OpenAI API key
* Groq API key — optional

Recommended:

```text
Python 3.12
Git
PowerShell
VS Code
```

---

# 🗄 Supabase Setup

Create a new Supabase project.

Open:

```text
Supabase Dashboard
        ↓
SQL Editor
```

Open:

```text
supabase/schema.sql
```

Copy its contents into Supabase SQL Editor.

Execute the SQL.

The schema creates:

```text
documents
```

with:

```text
id
title
content
source
embedding
created_at
```

It also creates:

```text
match_documents()
```

which performs semantic similarity search.

---

# 🔐 Supabase Credentials

From:

```text
Supabase
   ↓
Project Settings
   ↓
API
```

Copy:

```text
Project URL
service_role key
```

The service-role key must remain on the backend.

Never commit it to GitHub.

---

# 🐍 Local Installation

Clone the project:

```powershell
git clone <YOUR_GITHUB_REPO_URL>

cd smart-customer-support
```

Create virtual environment:

```powershell
py -3.12 -m venv .venv
```

Activate:

```powershell
Set-ExecutionPolicy `
    -Scope Process `
    -ExecutionPolicy Bypass

.\.venv\Scripts\Activate.ps1
```

Upgrade pip:

```powershell
python -m pip install --upgrade pip
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

---

# ⚙️ Environment Configuration

Create the environment file:

```powershell
Copy-Item .env.example .env
```

Open it:

```powershell
notepad .env
```

Example:

```env
OPENAI_API_KEY=sk-your-key

OPENAI_MODEL=gpt-5.6-luna

GROQ_API_KEY=gsk-your-key

GROQ_MODEL=llama-3.3-70b-versatile

PROVIDER=openai

SUPABASE_URL=https://xxxxx.supabase.co

SUPABASE_SERVICE_ROLE_KEY=your-service-role-key

SUPABASE_DB_URL=postgresql://postgres:password@db.xxxxx.supabase.co:5432/postgres?sslmode=require

EMBEDDING_MODEL=text-embedding-3-small

EMBEDDING_DIM=1536

TOP_K=5

SIMILARITY_THRESHOLD=0.70

CHECKPOINT_DB_URL=

APP_ENV=development

LOG_LEVEL=INFO
```

---

# 🔑 Environment Variables

| Variable                    | Description                   |
| --------------------------- | ----------------------------- |
| `OPENAI_API_KEY`            | OpenAI API key                |
| `OPENAI_MODEL`              | OpenAI model                  |
| `GROQ_API_KEY`              | Optional Groq API key         |
| `GROQ_MODEL`                | Groq model                    |
| `PROVIDER`                  | `openai` or `groq`            |
| `SUPABASE_URL`              | Supabase URL                  |
| `SUPABASE_SERVICE_ROLE_KEY` | Supabase backend key          |
| `SUPABASE_DB_URL`           | PostgreSQL connection         |
| `EMBEDDING_MODEL`           | Embedding model               |
| `EMBEDDING_DIM`             | Vector dimensions             |
| `TOP_K`                     | Number of retrieved documents |
| `SIMILARITY_THRESHOLD`      | Minimum similarity            |
| `CHECKPOINT_DB_URL`         | Production LangGraph database |
| `APP_ENV`                   | Application environment       |
| `LOG_LEVEL`                 | Logging level                 |

---

# 📚 PDF Knowledge Ingestion

Create:

```powershell
New-Item `
    -ItemType Directory `
    -Force `
    data
```

Copy PDFs:

```powershell
Copy-Item `
    "C:\CompanyDocs\*.pdf" `
    .\data\
```

Example:

```text
data/
├── company-handbook.pdf
├── refund-policy.pdf
├── api-documentation.pdf
└── troubleshooting-guide.pdf
```

Run:

```powershell
python .\ingest.py --folder .\data
```

The ingestion process:

```text
PDF
 ↓
Text Extraction
 ↓
Text Cleaning
 ↓
Chunking
 ↓
OpenAI Embedding
 ↓
Supabase
 ↓
pgvector
```

Example output:

```text
Ingested 17 chunks from data\company-handbook.pdf
Ingested 22 chunks from data\api-documentation.pdf
```

---

# 🔎 Semantic Search

When a user submits:

```text
What is the refund policy?
```

the system:

```text
Question
   ↓
Embedding
   ↓
Vector
   ↓
pgvector
   ↓
Cosine Similarity
   ↓
Top 5 Documents
   ↓
RAG Agent
   ↓
Answer
```

The application uses:

```text
TOP_K=5
```

by default.

Similarity filtering:

```text
SIMILARITY_THRESHOLD=0.70
```

---

# ▶️ Running the Backend

Start FastAPI:

```powershell
uvicorn `
    src.api.main:app `
    --reload `
    --host 127.0.0.1 `
    --port 8000
```

The API runs at:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

Alternative ReDoc:

```text
http://127.0.0.1:8000/redoc
```

---

# 🎨 Running the Frontend

Open another PowerShell terminal.

Activate the environment:

```powershell
cd smart-customer-support

.\.venv\Scripts\Activate.ps1
```

Set API URL:

```powershell
$env:API_URL="http://127.0.0.1:8000"
```

Start Streamlit:

```powershell
streamlit run .\streamlit_app.py
```

Open:

```text
http://localhost:8501
```

---

# 🔌 API Documentation

## Health endpoint

```http
GET /api/health
```

Response:

```json
{
  "status": "ok"
}
```

---

# 💬 Chat API

Endpoint:

```http
POST /api/chat
```

Request:

```json
{
  "query": "How do I reset my password?",
  "thread_id": "demo-001"
}
```

Response:

```json
{
  "answer": "According to the internal documentation...",
  "query_type": "faq",
  "sources": [],
  "escalated": false,
  "ticket_id": null,
  "thread_id": "demo-001",
  "trace": [
    "classified:faq",
    "rag_agent",
    "learning_agent"
  ]
}
```

---

# 🧪 PowerShell API Test

Health:

```powershell
Invoke-RestMethod `
    "http://127.0.0.1:8000/api/health"
```

Chat:

```powershell
$body = @{
    query = "How do I reset my password?"
    thread_id = "demo-001"
} | ConvertTo-Json

Invoke-RestMethod `
    -Uri "http://127.0.0.1:8000/api/chat" `
    -Method Post `
    -ContentType "application/json" `
    -Body $body
```

---

# 🧪 Technical Query

```powershell
$body = @{
    query = "Our API returns AUTH-401. What should I check?"
    thread_id = "technical-001"
} | ConvertTo-Json

Invoke-RestMethod `
    -Uri "http://127.0.0.1:8000/api/chat" `
    -Method Post `
    -ContentType "application/json" `
    -Body $body
```

Expected routing:

```text
classify_query
       ↓
technical
       ↓
Technical Agent
       ↓
diagnose_error
       ↓
Learning Agent
```

---

# 🚨 Escalation Query

```powershell
$body = @{
    query = "I need a human manager to review this complaint."
    thread_id = "escalation-001"
} | ConvertTo-Json

Invoke-RestMethod `
    -Uri "http://127.0.0.1:8000/api/chat" `
    -Method Post `
    -ContentType "application/json" `
    -Body $body
```

Expected response:

```json
{
  "escalated": true,
  "ticket_id": "SUP-XXXXXXXX"
}
```

---

# 💡 Example Queries

## FAQ

```text
How do I reset my password?
```

```text
What is your refund policy?
```

```text
How do I cancel my subscription?
```

```text
What are your support hours?
```

---

## Technical

```text
Our API returns AUTH-401. What should I check?
```

```text
Why am I receiving RATE-429?
```

```text
Our database returns DB-503.
```

```text
The API keeps timing out.
```

---

## Escalation

```text
I need a human manager.
```

```text
I want to file a formal complaint.
```

```text
This is an urgent security issue.
```

```text
I need someone from the legal team.
```

---

# 🔄 LangGraph State

The workflow state contains:

```python
{
    "query": str,
    "query_type": str,
    "retrieved": list,
    "answer": str,
    "escalated": bool,
    "ticket_id": str | None,
    "trace": list,
    "learning_candidate": str,
    "attempts": int
}
```

This allows the workflow to maintain information between nodes.

---

# 💾 Checkpointing

Local development uses:

```python
InMemorySaver()
```

This is convenient for local development.

For production, PostgreSQL checkpointing should be used.

Configure:

```env
CHECKPOINT_DB_URL=postgresql://...
```

Then use:

```python
from langgraph.checkpoint.postgres import PostgresSaver

checkpointer = PostgresSaver.from_conn_string(
    settings.checkpoint_db_url
)

checkpointer.setup()

graph = builder.compile(
    checkpointer=checkpointer
)
```

Every conversation should have a stable:

```text
thread_id
```

Example:

```text
customer-123-session-001
```

---

# 🧪 Testing

Run all tests:

```powershell
pytest -q
```

Verbose:

```powershell
pytest -v
```

Agent tests:

```powershell
pytest tests/test_agents.py -v
```

Integration tests:

```powershell
pytest tests/test_integration.py -v
```

---

# 🔬 Manual RAG Test

First ingest a document:

```powershell
python .\ingest.py --folder .\data
```

Then ask:

```text
What is the company's refund policy?
```

Verify that:

```text
query_type = faq
```

and the response includes retrieved documentation.

The trace should include:

```text
classified:faq
rag_agent
learning_agent
```

---

# 🔧 Manual Technical Test

Ask:

```text
Our API returns AUTH-401.
```

Expected:

```text
classified:technical
technical_agent
learning_agent
```

The Technical Agent has access to:

```text
diagnose_error()
```

---

# 🚨 Manual Escalation Test

Ask:

```text
I need a human manager to review this complaint.
```

Expected:

```text
classified:escalation
escalation_agent
human_review_simulation
```

The response should contain:

```text
SUP-XXXXXXXX
```

---

# 🐳 Docker

Build:

```powershell
docker compose build
```

Start:

```powershell
docker compose up
```

Or:

```powershell
docker compose up --build
```

Backend:

```text
http://localhost:8000
```

Frontend:

```text
http://localhost:8501
```

Stop:

```powershell
docker compose down
```

---

# 🐳 Docker Without Compose

Build:

```powershell
docker build `
    -t smart-customer-support .
```

Run:

```powershell
docker run `
    --env-file .env `
    -p 8000:8000 `
    smart-customer-support
```

---

# ☁️ Render Deployment

The easiest deployment architecture is two Render services:

```text
Render
│
├── FastAPI Backend
│
└── Streamlit Frontend
```

Supabase remains the external database/vector store.

---

# 🚀 Deploy Backend

Create a Render Web Service.

Connect your GitHub repository.

Build command:

```text
pip install -r requirements.txt
```

Start command:

```text
uvicorn src.api.main:app --host 0.0.0.0 --port $PORT
```

Add environment variables:

```text
OPENAI_API_KEY
OPENAI_MODEL
PROVIDER

SUPABASE_URL
SUPABASE_SERVICE_ROLE_KEY
SUPABASE_DB_URL

EMBEDDING_MODEL
EMBEDDING_DIM
TOP_K
SIMILARITY_THRESHOLD

APP_ENV
LOG_LEVEL
```

Deploy.

Your backend URL will look like:

```text
https://smart-customer-support-api.onrender.com
```

Health check:

```text
https://smart-customer-support-api.onrender.com/api/health
```

---

# 🎨 Deploy Streamlit

Create another Render Web Service.

Build:

```text
pip install -r requirements.txt
```

Start:

```text
streamlit run streamlit_app.py --server.address=0.0.0.0 --server.port=$PORT
```

Set:

```text
API_URL=https://smart-customer-support-api.onrender.com
```

Deploy.

---

# 🔒 Production Configuration

Production should use:

```text
PostgreSQL LangGraph checkpoints
```

instead of:

```text
InMemorySaver
```

Production architecture:

```text
                         ┌──────────────┐
                         │  Streamlit   │
                         └──────┬───────┘
                                │
                                v
                         ┌──────────────┐
                         │   FastAPI    │
                         └──────┬───────┘
                                │
                                v
                         ┌──────────────┐
                         │  LangGraph   │
                         └──────┬───────┘
                                │
                 ┌──────────────┼──────────────┐
                 │              │              │
                 v              v              v
              RAG Agent    Technical      Escalation
                              Agent           Agent
                 │              │              │
                 └───────┬──────┘              v
                         │                  Ticket
                         v
                   Supabase
                    pgvector
                         │
                         v
                  PostgreSQL
                  Checkpoints
```

---

# 🛡 Security

Never commit:

```text
.env
```

Never expose:

```text
SUPABASE_SERVICE_ROLE_KEY
```

Never put private API keys inside:

```text
streamlit_app.py
```

Use environment variables.

For production, add:

* Authentication.
* Authorization.
* Rate limiting.
* HTTPS.
* API request validation.
* PII redaction.
* Audit logging.
* Secret rotation.

---

# ⚠️ Error Handling

The FastAPI layer catches workflow exceptions:

```text
Agent failure
       ↓
Exception
       ↓
FastAPI
       ↓
HTTP 500
```

Production should additionally implement retries for:

* OpenAI API failures.
* Supabase network failures.
* Temporary rate limits.
* Timeouts.

Recommended strategy:

```text
Attempt 1
   ↓
wait
   ↓
Attempt 2
   ↓
wait
   ↓
Attempt 3
   ↓
controlled failure
```

Exponential backoff should be used for external API calls.

---

# 📊 Logging

Application logging is configured through:

```env
LOG_LEVEL=INFO
```

Possible levels:

```text
DEBUG
INFO
WARNING
ERROR
CRITICAL
```

Example log format:

```text
2026-09-01 10:30:00 |
INFO |
src.agents.orchestrator |
technical_agent
```

Production should move toward structured JSON logs and centralized monitoring.

---

# 📈 Performance Metrics

The project should measure:

## Retrieval

```text
Recall@5
```

Target:

```text
>= 0.85
```

---

## Grounded answers

Percentage of answers supported by retrieved documentation.

Target:

```text
>= 90%
```

---

## FAQ latency

Target:

```text
p95 < 5 seconds
```

---

## Technical latency

Target:

```text
p95 < 10 seconds
```

---

## Escalation precision

Target:

```text
>= 85%
```

---

## Knowledge acceptance

Percentage of AI-generated knowledge candidates accepted by human reviewers.

Target:

```text
>= 70%
```

These are **target metrics**, not fabricated benchmark results. Actual performance must be measured after deployment.

---

# 💰 Cost Considerations

The project is designed for a low-cost capstone deployment.

Potential costs include:

```text
OpenAI API
Supabase usage
Render usage
```

The application reduces unnecessary model usage by:

* Routing queries.
* Retrieving relevant context.
* Giving agents focused responsibilities.
* Using deterministic tools for common error codes.

Groq can optionally be configured for compatible model execution.

---

# 🧩 Why RAG?

Without RAG:

```text
Customer
   ↓
LLM
   ↓
Possible hallucination
```

With RAG:

```text
Customer
   ↓
Embedding
   ↓
Company Documentation
   ↓
Relevant Context
   ↓
LLM
   ↓
Grounded Answer
```

This makes the system suitable for private company information.

---

# 🧩 Why LangGraph?

A normal chatbot is generally:

```text
Question
 ↓
LLM
 ↓
Answer
```

Customer support requires more:

```text
Question
 ↓
Classification
 ↓
Routing
 ↓
Retrieval
 ↓
Tool use
 ↓
Decision
 ↓
Escalation OR Resolution
 ↓
Learning
```

LangGraph provides a natural way to represent this workflow as a stateful graph.

---

# 🧩 Why Agent SDK?

Different support tasks require different behavior.

Instead of one giant agent:

```text
Mega Agent
```

the system uses:

```text
RAG Agent
Technical Agent
Escalation Agent
Learning Agent
```

Each agent has a narrow responsibility.

This improves:

* Maintainability.
* Tool boundaries.
* Debugging.
* Prompt design.
* Future scaling.

---

# 🧩 Why Supabase?

Supabase provides:

```text
PostgreSQL
+
pgvector
+
Authentication options
+
APIs
+
Dashboard
```

For this capstone, Supabase acts as the knowledge/vector database.

---

# 🧠 Knowledge Management Lifecycle

The system supports:

```text
Company PDF
     ↓
Ingestion
     ↓
Embedding
     ↓
Vector Database
     ↓
Customer Question
     ↓
Retrieval
     ↓
AI Answer
     ↓
Resolved Interaction
     ↓
Learning Agent
     ↓
Knowledge Candidate
     ↓
Human Review
     ↓
Future Knowledge Base
```

This creates a feedback loop.

---

# 🔁 Learning Loop

```text
Customer Interaction
       ↓
AI Resolution
       ↓
Learning Agent
       ↓
Candidate Article
       ↓
Human Review
       ↓
Approved Knowledge
       ↓
Vector Database
       ↓
Better Future Answers
```

The current implementation intentionally generates a **candidate** rather than automatically publishing AI-generated content.

---

# 🧪 Acceptance Criteria

| Requirement           | Status |
| --------------------- | ------ |
| RAG                   | ✅      |
| LangGraph             | ✅      |
| Agent SDK             | ✅      |
| Real-world problem    | ✅      |
| PDF ingestion         | ✅      |
| Supabase              | ✅      |
| pgvector              | ✅      |
| Semantic search       | ✅      |
| Embeddings            | ✅      |
| Conditional workflow  | ✅      |
| Multiple agents       | ✅      |
| Tool calling          | ✅      |
| Human escalation      | ✅      |
| Learning agent        | ✅      |
| FastAPI               | ✅      |
| Streamlit             | ✅      |
| Environment variables | ✅      |
| Error handling        | ✅      |
| Logging               | ✅      |
| Docker                | ✅      |
| Tests                 | ✅      |
| Case study            | ✅      |
| Deployment guide      | ✅      |
| Example queries       | ✅      |

---

# 🔮 Future Improvements

## MCP

Expose tools through Model Context Protocol:

```text
MCP Server
│
├── search_documents
├── diagnose_error
├── create_ticket
└── knowledge_lookup
```

---

## A2A

The Technical Agent could become an independent service:

```text
Main Support Agent
       ↓
A2A
       ↓
Technical Agent Service
       ↓
Diagnosis
```

This would allow independently deployed agents to collaborate.

---

## Real Ticketing

Replace:

```text
create_support_ticket()
```

with integrations such as:

```text
Zendesk
Jira
ServiceNow
Freshdesk
```

---

## Authentication

Add:

```text
JWT
OAuth
Role-Based Access Control
```

---

## Advanced RAG

Future versions could implement:

```text
Hybrid Search
+
BM25
+
Vector Search
+
Reranking
+
Metadata Filtering
```

---

## Evaluation

Build an evaluation dataset:

```text
question
expected_answer
expected_source
expected_route
```

Then measure:

```text
retrieval accuracy
answer accuracy
grounding
routing accuracy
escalation accuracy
latency
cost
```

---

# 📄 Case Study

The detailed case study is available at:

```text
docs/case_study.md
```

It covers:

* Problem definition.
* Solution overview.
* Architecture.
* RAG implementation.
* LangGraph implementation.
* Agent SDK implementation.
* Challenges.
* Performance metrics.
* Future improvements.
* Production considerations.

---

# 🐛 Troubleshooting

## `OPENAI_API_KEY is required`

Check:

```powershell
Get-Content .env
```

Make sure:

```env
OPENAI_API_KEY=your-key
```

exists.

---

## Supabase connection error

Verify:

```env
SUPABASE_URL=
SUPABASE_SERVICE_ROLE_KEY=
```

Also verify the SQL schema has been executed.

---

## No documents returned

Run:

```powershell
python .\ingest.py --folder .\data
```

Then verify the `documents` table in Supabase.

---

## PDF ingestion finds no files

Check:

```powershell
Get-ChildItem .\data
```

Make sure the files end in:

```text
.pdf
```

---

## Streamlit cannot connect

Check that FastAPI is running:

```powershell
Invoke-RestMethod `
    "http://127.0.0.1:8000/api/health"
```

Then:

```powershell
$env:API_URL="http://127.0.0.1:8000"

streamlit run .\streamlit_app.py
```

---

## Port 8000 already in use

Find the process:

```powershell
Get-NetTCPConnection `
    -LocalPort 8000
```

Or use another port:

```powershell
uvicorn `
    src.api.main:app `
    --reload `
    --port 8010
```

Then:

```powershell
$env:API_URL="http://127.0.0.1:8010"
```

---

## Port 8501 already in use

Run:

```powershell
streamlit run .\streamlit_app.py `
    --server.port 8502
```

---

# 📦 Complete Setup Command Summary

For a fresh Windows machine:

```powershell
git clone <YOUR_GITHUB_REPO_URL>

cd smart-customer-support

py -3.12 -m venv .venv

Set-ExecutionPolicy `
    -Scope Process `
    -ExecutionPolicy Bypass

.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip

pip install -r requirements.txt

Copy-Item .env.example .env

notepad .env

New-Item `
    -ItemType Directory `
    -Force `
    data

# Put PDFs inside data\

python .\ingest.py --folder .\data

uvicorn `
    src.api.main:app `
    --reload `
    --host 127.0.0.1 `
    --port 8000
```

New terminal:

```powershell
cd smart-customer-support

.\.venv\Scripts\Activate.ps1

$env:API_URL="http://127.0.0.1:8000"

streamlit run .\streamlit_app.py
```

---

# 🧪 Complete Test Command Summary

```powershell
pytest -q
```

```powershell
pytest -v
```

```powershell
pytest tests/test_agents.py -v
```

```powershell
pytest tests/test_integration.py -v
```

Health:

```powershell
Invoke-RestMethod `
    "http://127.0.0.1:8000/api/health"
```

---

# 📌 GitHub Submission

Initialize Git:

```powershell
git init
```

Add files:

```powershell
git add .
```

Commit:

```powershell
git commit -m "Build smart customer support AI agent"
```

Create your GitHub repository, then:

```powershell
git remote add origin <YOUR_GITHUB_REPO_URL>
```

Push:

```powershell
git branch -M main

git push -u origin main
```

---

# 🚨 Before Pushing to GitHub

Verify:

```powershell
git status
```

Make sure `.env` is **not** listed.

Check:

```powershell
git ls-files .env
```

It should return nothing.

The repository should contain:

```text
.env.example
```

but not:

```text
.env
```

---

# 🏆 Capstone Demonstration Flow

For the final presentation/demo, demonstrate these three scenarios.

## Demo 1 — FAQ

Enter:

```text
What is the company's refund policy?
```

Show:

```text
FAQ classification
       ↓
RAG Agent
       ↓
Supabase
       ↓
Relevant documentation
       ↓
Grounded answer
```

---

## Demo 2 — Technical

Enter:

```text
Our API returns AUTH-401. What should I check?
```

Show:

```text
Technical classification
       ↓
Technical Agent
       ↓
diagnose_error()
       ↓
Troubleshooting
       ↓
Learning Agent
```

---

## Demo 3 — Escalation

Enter:

```text
I need a human manager to review this complaint.
```

Show:

```text
Escalation classification
       ↓
Escalation Agent
       ↓
Human Review
       ↓
SUP-XXXXXXXX
```

This demonstrates the complete agent lifecycle.

---

# 📊 Final Architecture Summary

```text
                         CUSTOMER
                            |
                            v
                    ┌───────────────┐
                    │   Streamlit   │
                    └───────┬───────┘
                            |
                            v
                    ┌───────────────┐
                    │    FastAPI    │
                    └───────┬───────┘
                            |
                            v
                    ┌───────────────┐
                    │   LangGraph   │
                    └───────┬───────┘
                            |
                     Query Routing
                            |
          ┌─────────────────┼─────────────────┐
          |                 |                 |
          v                 v                 v
       FAQ             Technical         Escalation
          |                 |                 |
          v                 v                 v
      RAG Agent       Technical Agent   Escalation Agent
          |                 |                 |
          v                 v                 v
     Supabase          Diagnostic       Human Review
      pgvector            Tool                |
          |                 |                 v
          |                 |              Ticket
          └────────┬────────┘
                   |
                   v
             Learning Agent
                   |
                   v
          Knowledge Candidate
                   |
                   v
             Future RAG Data
```

---

# 🎓 Learning Outcomes

This project demonstrates practical understanding of:

* Retrieval-Augmented Generation.
* Vector databases.
* Embeddings.
* Semantic search.
* Supabase and pgvector.
* LangGraph state machines.
* Conditional agent workflows.
* Multi-agent architectures.
* Tool calling.
* Human escalation.
* Knowledge management.
* FastAPI.
* Streamlit.
* Docker.
* Environment configuration.
* Testing.
* Production deployment.

---

# 👨‍💻 Author

**Smart Customer Support & Knowledge Management System**

AI Agent Capstone Project

Built using:

```text
RAG
+
LangGraph
+
OpenAI Agents SDK
+
Supabase
+
pgvector
+
FastAPI
+
Streamlit
```

---

# ⭐ Final Result

The project provides an end-to-end AI customer-support system capable of:

```text
UNDERSTAND
    ↓
RETRIEVE
    ↓
REASON
    ↓
USE TOOLS
    ↓
SOLVE
    ↓
ESCALATE WHEN NECESSARY
    ↓
LEARN
```

The architecture is intentionally modular so that MCP, A2A, real ticketing systems, authentication, advanced retrieval, and production observability can be added without redesigning the entire application.
