# Personal Chat Agent — Portfolio Assistant Backend

A ReAct agent backend for developer portfolio chatbots. Built with LangGraph, RAG and FastAPI.

Live demo: [prashantnathv2.netlify.app](https://prashantnathv2.netlify.app)

## Architecture Diagrams

See `docs/architecture/`

---

## What it does

- Answers questions about you using a RAG knowledge base (Pinecone)
- Fetches your live GitHub repositories on demand
- Captures visitor contact details to Supabase
- Streams responses token by token via SSE
- Remembers context within a conversation session

---

## Tech Stack

| Layer        | Technology                    |
| ------------ | ----------------------------- |
| Framework    | FastAPI                       |
| Agent        | LangGraph (ReAct pattern)     |
| LLM          | OpenAI gpt-4o-mini            |
| Embeddings   | OpenAI text-embedding-3-small |
| Vector Store | Pinecone                      |
| Database     | Supabase (PostgreSQL)         |
| Memory       | LangGraph MemorySaver         |
| Streaming    | Server-Sent Events (SSE)      |

---

## Project Structure

```
app/
├── agent/
│   ├── graph.py          # LangGraph graph assembly
│   ├── nodes.py          # llm_node and tool_node
│   ├── prompt.py         # System prompt
│   └── state.py          # Agent state schema
├── api/
│   ├── api_service/
│   │   └── chat_service.py   # SSE streaming logic
│   └── routes/
│       └── chat_router.py    # /chat endpoint
├── core/
│   └── config.py         # Environment variables settings
├── services/
│   ├── pinecone_service.py
│   └── supabase_service.py
└── tools/
    ├── rag_tool.py
    ├── github_tool.py
    └── user_capture_tool.py
scripts/
└── indexing.py           # Knowledge base ingestion
```

---

## Use This For Your Portfolio

### 1. Clone the repo

```bash
git clone https://github.com/prashant00797/personal-chat-agent
cd personal-chat-agent
```

### 2. Set up environment variables

```bash
cp .env.example .env
```

Fill in your values:

```
OPENAI_API_KEY=
PINECONE_API_KEY=
PINECONE_INDEX_NAME=
PINECONE_HOST=
SUPABASE_URL=
SUPABASE_KEY=
GITHUB_BASE_URL=https://api.github.com/users/YOUR_USERNAME/repos
STREAM_DELAY=
DUMMY_HEALTH_CHECK_BOT_ID=
```

### 3. Add your knowledge base

Create a PDF with information about yourself — experience, skills, projects, availability, preferences. Place it at:

```
knowledge_base/your_name_kb.pdf
```

### 4. Run ingestion

```bash
uv run python -m scripts.indexing
```

This embeds your document and pushes vectors to Pinecone.

### 5. Update the system prompt

Edit `app/agent/prompt.py` — replace Prashant's details with your own name, contact info and persona.

### 6. Run the server

```bash
uv run uvicorn main:app --reload
```

API available at `http://localhost:8000`
Swagger docs at `http://localhost:8000/docs`

---

## API

### `POST /api/chat`

Streams a chat response as SSE.

**Request:**

```json
{
  "message": "What is your experience with React?",
  "thread_id": "uuid-string"
}
```

**SSE Events:**

```
data: {"type": "tool_call", "tool": "retrieve_relevant_chunks"}
data: {"type": "token", "content": "Prashant"}
data: {"type": "end"}
data: {"type": "error", "message": "..."}
```

---

## Deploy

Tested on [Render](https://render.com) free tier.

**Start command:**

```
uvicorn main:app --host 0.0.0.0 --port $PORT
```

Add all environment variables in Render dashboard under Environment.

---

## Requirements

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) package manager
- Pinecone account (free tier works)
- Supabase account (free tier works)
- OpenAI API key

---

## Frontend

The Next.js chat widget frontend is in a separate repo:
[my-portfolio-v2](https://github.com/prashant00797/my-portfolio-v2)
