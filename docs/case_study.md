# Case Study: Smart Customer Support & Knowledge Management System

## Problem

Traditional customer support systems rely on rule-based routing and static FAQ pages. Customers often wait for human agents even for simple questions, while support teams handle repetitive inquiries. The goal was to build an AI-powered system that could understand customer queries, retrieve relevant knowledge base documents, and provide accurate responses automatically — while routing complex issues to the appropriate specialist or human agent.

## Solution

We designed a multi-agent architecture powered by LangGraph that classifies incoming customer queries and routes them to specialized agents. Each agent handles a specific type of support interaction, and a learning agent records all interactions for continuous improvement.

### Core Technologies

- **FastAPI** — Async Python API framework for high-concurrency request handling
- **LangGraph** — Stateful workflow orchestration with conditional routing and retry logic
- **OpenAI Agents SDK** — LLM-powered agent execution with structured outputs
- **RAG** — Retrieval-Augmented Generation using MongoDB Atlas Vector Search
- **MongoDB Atlas** — Vector search for document retrieval + conversation storage
- **Next.js** — React frontend deployed on Vercel
- **Render** — Backend hosting with automatic deployments

## Architecture

The system follows this request flow:

```text
User → Frontend → FastAPI → LangGraph → Router Agent
                                          │
                    ┌─────────────────────┼─────────────────────┐
                    ▼                     ▼                     ▼
              FAQ Category         Technical Category     Escalation Category
                    │                     │                     │
              RAG Agent            Technical Agent        Escalation Agent
                    │                     │                     │
           MongoDB Vector          MCP Tools + LLM        Human Review
              Search                                          │
                    │                                    Learning Agent
                    └────────────────┬──────────────────────┘
                                     ▼
                              Learning Agent
                                     │
                              MongoDB Storage
```

### Router Agent

The Router Agent classifies incoming queries into one of three categories:

- **FAQ** — General questions, policies, shipping, refunds
- **TECHNICAL** — Errors, broken features, payment failures
- **ESCALATION** — Legal issues, angry customers, security incidents

The classification is performed by an LLM call via the OpenAI Agents SDK, which returns a structured category string.

### RAG Agent

For FAQ queries, the RAG Agent:

1. Generates an embedding of the customer query using OpenAI's `text-embedding-3-small` model
2. Performs a MongoDB Atlas vector search against the `knowledge_documents` collection
3. Retrieves the top-k most similar documents
4. Passes the retrieved context to an LLM to generate a grounded response

This ensures responses are based on actual company documentation rather than hallucinated content.

### Technical Agent

For technical issues, the Technical Agent provides step-by-step troubleshooting guidance. It can access MCP tools to look up customer and order information from the database.

### Escalation Agent

For complex or sensitive issues, the Escalation Agent creates a structured escalation summary that includes the customer issue, what was already attempted, why human intervention is needed, and the recommended next action.

### Learning Agent

After every interaction, the Learning Agent records the thread ID, query, answer, category, and agent used to a `conversations` collection in MongoDB. This data can be used for analytics and continuous improvement.

## RAG Implementation

### Document Ingestion

Documents are ingested using a chunking strategy:

- Chunk size: 1200 characters
- Overlap: 200 characters
- Each chunk is embedded and stored with metadata (title, source, content)

### Vector Search

MongoDB Atlas performs approximate nearest neighbor search using:

- Index: `knowledge_vector_index`
- Field: `embedding` (1536 dimensions)
- Similarity: cosine
- Threshold: 0.70

### Graceful Degradation

When no documents match the query (score below threshold), the system returns a fallback message rather than hallucinating an answer. This is critical for maintaining trust.

## LangGraph Workflow

The workflow uses LangGraph's `StateGraph` with:

- **Nodes**: classify, rag, technical, escalation, learning
- **Conditional edges**: Route based on classification category
- **Retry logic**: RAG node can retry once if no documents found
- **State**: TypedDict carrying query, category, answer, sources, and metadata

### Infinite Retry Bug Fix

During development, we discovered a critical bug: the RAG retry counter was never incremented, causing the workflow to retry indefinitely when MongoDB returned no results.

**Root cause**: `rag_node()` spread `**state` (which included `retry_count=0`) without updating it.

**Fix**: Added `"retry_count": retry + 1` to the return value of `rag_node()`, breaking the infinite loop.

This bug would have caused production requests to hang indefinitely, consuming resources and never returning a response.

## MongoDB Atlas

### Collections

| Collection | Purpose |
|------------|---------|
| `knowledge_documents` | Ingested RAG documents with embeddings |
| `conversations` | Chat interaction logs |
| `customers` | Customer records (MCP tools) |
| `orders` | Order records (MCP tools) |
| `support_tickets` | Support ticket records |

### Network Access

MongoDB Atlas must be configured to accept connections from:

- Render backend IPs
- Local development IPs
- `0.0.0.0/0` for testing only

## Performance

Measured locally during development:

| Metric | Value |
|--------|-------|
| `/api/chat` (end-to-end) | ~4 seconds |
| OpenAI classification | ~3.2 seconds |
| OpenAI LLM calls | ~1.8 seconds |
| MongoDB vector search | ~0.5 seconds |
| Embedding generation | ~0.3 seconds |
| MongoDB ping | ~71 ms |

> These are development/test measurements, not production SLAs. Actual performance depends on network latency, OpenAI load, and MongoDB Atlas tier.

## Challenges

### 1. Infinite Retry Loop

The most critical issue was the infinite RAG retry loop. When no documents existed in MongoDB (before ingestion), the workflow would retry the RAG node forever because `retry_count` was never incremented.

**Resolution**: Increment `retry_count` in `rag_node()` return value.

### 2. CORS Configuration

The frontend (Vercel) and backend (Render) run on different domains. CORS must be configured to allow cross-origin requests while maintaining security.

**Resolution**: Environment-driven `CORS_ORIGINS` variable supporting wildcards for development and specific origins for production.

### 3. Cold Start on Render

Render's free tier services spin down after inactivity, causing slow cold starts.

**Resolution**: Added a lightweight `/api/keepalive` endpoint that the frontend polls every 40 seconds to keep the service alive.

### 4. Async/Sync Mixing

The OpenAI Agents SDK's `Runner.run()` is async, while MongoDB's `pymongo` operations are synchronous. Mixing these incorrectly can cause blocking.

**Resolution**: Used async FastAPI routes with `await` for agent calls, and kept synchronous MongoDB operations in sync functions called from LangGraph nodes (which run in thread pools).

## Deployment

### Backend (Render)

- **Build**: `pip install -r requirements.txt`
- **Start**: `uvicorn src.api.main:app --host 0.0.0.0 --port $PORT`
- **Environment**: Python 3.10, MongoDB Atlas, OpenAI API

### Frontend (Vercel)

- **Framework**: Next.js 15 with App Router
- **Environment Variable**: `NEXT_PUBLIC_API_URL` pointing to Render backend

### Database (MongoDB Atlas)

- **Tier**: M0 (free)
- **Features**: Vector Search, Atlas Search
- **Network**: Configured for Render + development access

## Future Improvements

1. **Streaming responses** — Stream LLM tokens to the frontend for better UX
2. **Conversation memory** — Maintain multi-turn context using thread IDs
3. **Feedback loop** — Allow customers to rate responses and feed back into the learning agent
4. **Analytics dashboard** — Visualize support metrics, agent performance, and common issues
5. **Multi-language support** — Extend RAG and agents to handle multiple languages
6. **Authentication** — Add user authentication for personalized support
7. **Rate limiting** — Protect the API from abuse
8. **Monitoring** — Add structured logging and alerting for production
