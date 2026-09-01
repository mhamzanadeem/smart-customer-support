# Case Study: Smart Customer Support & Knowledge Management System

## 1. Problem definition

Customer-support teams are pressured to answer repetitive questions quickly while also handling technical incidents, ambiguous requests, and cases that require human judgment. A conventional FAQ bot can answer predictable questions, but it often fails when information is spread across PDFs, runbooks, product manuals, or internal policies.

A second problem is that support interactions contain reusable knowledge, yet that knowledge is frequently lost after a ticket is closed.

This project addresses the problem with a support agent that combines retrieval-augmented generation, a stateful workflow engine, and a multi-agent runtime.

The system accepts a customer query, determines the type of request, retrieves relevant internal evidence when appropriate, delegates specialized work to an agent, and either returns an answer or prepares a simulated human escalation.

A learning step turns successful interactions into knowledge candidates.

The design intentionally separates orchestration from specialist behavior.

LangGraph owns workflow state and conditional routing.

The OpenAI Agents SDK owns specialist agent execution and tool calling.

Supabase Postgres with pgvector stores document embeddings and performs semantic retrieval.

---

## 2. Solution overview

The request enters a FastAPI backend.

The API validates the request and passes it to a LangGraph state machine.

The first node classifies the query into:

- FAQ
- Technical
- Escalation

FAQ requests go to the RAG path.

The application embeds the question and searches Supabase using cosine similarity.

The retrieved passages are then supplied to the RAG Agent, which answers from evidence rather than relying only on model memory.

Technical questions enter the Technical Agent path.

The agent can call a deterministic error-diagnosis tool and can also use retrieved documentation.

A conditional edge decides whether the issue is resolved or needs escalation.

Escalation requests go directly to the Escalation Agent.

The agent creates a concise human-handoff package.

A local ticket simulator assigns a ticket identifier.

Successful non-escalated interactions reach the Learning Agent.

It generates a candidate article that can later be reviewed and inserted into the knowledge base.

In a production implementation, this final step should use an approval queue rather than automatically publishing generated content.

---

## 3. Architecture choices

### RAG

Supabase is used as both the relational database and vector store.

The `documents` table contains:

- document metadata
- document text chunks
- embeddings

The embeddings are generated with:

`text-embedding-3-small`

The embedding dimension is 1536.

pgvector's cosine distance operator is used by a Postgres RPC function to retrieve the top matching chunks.

The ingestion script extracts text from PDFs with `pypdf`.

It normalizes the extracted text, creates overlapping chunks, generates embeddings, and inserts them into Supabase.

This keeps retrieval independent from the LLM and makes the evidence inspectable.

---

### LangGraph

LangGraph is responsible for the workflow because customer support is not a single prompt.

The graph contains:

- classification
- RAG
- technical
- escalation
- learning

nodes.

Conditional edges implement routing and the technical-resolution decision.

The graph is compiled with a checkpointer, so each thread can retain state between calls.

The local reference implementation uses an in-memory checkpointer to keep the initial setup simple.

For production, the graph should be compiled with `PostgresSaver` from `langgraph-checkpoint-postgres` using the Supabase/Postgres connection string.

This gives durable checkpoints and recovery semantics.

---

### Agent SDK

The OpenAI Agents SDK supplies the specialist agents.

Each agent has focused instructions and only the tools it needs.

The RAG Agent can invoke semantic search.

The Technical Agent can call the error-diagnosis function.

The Escalation and Learning Agents are intentionally tool-light.

This separation improves observability and reduces the chance that one general-purpose prompt will attempt every task.

The SDK also provides managed agent turns, tool execution, handoffs, and tracing capabilities.

---

## 4. Challenges faced

### Retrieval grounding

The first challenge is keeping retrieval grounded.

A vector search result is useful only if the application sends the retrieved evidence to the model and instructs it not to invent unsupported policy.

The implementation therefore keeps retrieval as a separate service and includes the retrieved passages in the agent prompt.

---

### Workflow state

The second challenge is workflow state.

A stateless HTTP request is insufficient for escalation or multi-step support because the system needs a stable thread identifier.

LangGraph's checkpoint model solves this by associating state with a `thread_id`.

---

### Provider portability

The third challenge is provider portability.

OpenAI is the default provider, while Groq can be used through its OpenAI-compatible endpoint.

The application keeps provider configuration in environment variables.

---

### Safe learning

The fourth challenge is safe learning.

Automatically writing every model response into the knowledge base can amplify mistakes.

Therefore the Learning Agent creates a candidate article rather than silently publishing it.

A production version should add:

- human approval
- versioning
- evaluation
- audit history

before publication.

---

## 5. Component implementation

### RAG

RAG is implemented in:

```text
src/services/vector_store.py
src/tools/rag_tool.py
supabase/schema.sql
ingest.py