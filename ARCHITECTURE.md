# RAG API - Architecture Overview

## System Design

```
┌─────────────────────────────────────────────────────┐
│              FastAPI Application                    │
│  ┌────────────────────────────────────────────────┐ │
│  │  HTTP Endpoints                                │ │
│  │  • GET  /health       - Service status        │ │
│  │  • POST /ask          - Query engine          │ │
│  │  • GET  /docs         - API documentation     │ │
│  └────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────┐ │
│  │  Middleware                                     │ │
│  │  • CORS (Cross-Origin Resource Sharing)       │ │
│  │  • Exception Handling                          │ │
│  │  • Request Validation (Pydantic)              │ │
│  └────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────┐
│              RAG Engine                             │
│  (Singleton - initialized once on startup)          │
│  ┌────────────────────────────────────────────────┐ │
│  │  Initialize (called in lifespan.startup)       │ │
│  │  • Load documents from ./data                  │ │
│  │  • Check for existing index in ./storage       │ │
│  │  • Build or load VectorStoreIndex              │ │
│  │  • Create QueryEngine                          │ │
│  └────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────┐ │
│  │  Query (called per request)                    │ │
│  │  • Parse question                              │ │
│  │  • Retrieve similar documents (similarity_top_k=3) │
│  │  • Generate answer via LLM                     │ │
│  │  • Extract and score sources                   │ │
│  │  • Return answer + sources                     │ │
│  └────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────┘
                  ↙              ↘
          ┌──────────┐      ┌──────────┐
          │  Storage │      │  LLMs    │
          │          │      │          │
          │./storage │      │HuggingFace API │
          │(index)   │      │(Llama-3.1-8B)  │
          └──────────┘      └──────────┘
                    ↙              ↘
          ┌──────────┐      ┌──────────┐
          │   Data   │      │Embeddings│
          │          │      │          │
          │ ./data   │      │all-MiniLM-L6-v2 │
          │ (PDFs)   │      │(local)   │
          └──────────┘      └──────────┘
```

## Request Flow

1. **User sends POST /ask** with question
2. **FastAPI validates** input using AskRequest Pydantic model
3. **RAG Engine retrieves** similar documents (using embeddings)
4. **LLM generates** answer based on retrieved documents
5. **Response builder** extracts sources with relevance scores
6. **FastAPI returns** AskResponse (answer + sources)

## Key Components

### 1. app.py (FastAPI Entry Point)
- Defines HTTP endpoints
- Handles request/response validation
- Manages application lifecycle (startup/shutdown)
- Adds CORS middleware
- Logs all operations

### 2. rag_engine.py (RAG Logic)
- **RAGEngine class**: Core logic for indexing and querying
- **Index Management**: Load existing or build new
- **Document Processing**: Parse PDFs using SemanticSplitterNodeParser
- **Query Processing**: Retrieve + generate answers
- **Singleton pattern**: Only one instance across requests

### 3. config.py (Configuration)
- Load environment variables from .env
- Validate required settings
- Provide typed configuration access
- Handle path management

### 4. models.py (Pydantic Schemas)
- **AskRequest**: Input validation (min/max length)
- **SourceMetadata**: Source file + relevance score
- **AskResponse**: Final API response
- **ErrorResponse**: Error handling responses

## Data Flow in /ask Endpoint

```
AskRequest
  ↓
[Validation: min 1, max 1000 chars]
  ↓
RAGEngine.query(question)
  ├─ Embed question
  ├─ Find similar chunks (top 3)
  ├─ Build context
  ├─ Call LLM
  └─ Extract sources
  ↓
AskResponse
  ├─ answer: str (generated text)
  └─ sources: List[SourceMetadata]
     ├─ file: str
     └─ score: float (0.0-1.0)
```

## Startup Sequence

1. **Environment**: Load .env file
2. **Config**: Parse and validate configuration
3. **FastAPI**: Create app instance
4. **CORS Middleware**: Add cross-origin support
5. **Lifespan Startup**:
   - Initialize RAGEngine (singleton)
   - Setup LLM and embedding models
   - Load documents from ./data
   - Check for existing index in ./storage
   - Build or load vector index
   - Create QueryEngine
6. **Server Ready**: Accept requests on port 8000

## Index Persistence Strategy

**First Run:**
```
./data/pdf1.pdf
./data/pdf2.pdf
    ↓
[Parse with SemanticSplitterNodeParser]
    ↓
[Create semantic chunks]
    ↓
[Build VectorStoreIndex]
    ↓
./storage/docstore.json  ← Persisted
```

**Subsequent Runs:**
```
./storage/docstore.json exists?
    ↓ YES
[Load from storage]
    ↓
Skip recomputation (~minutes saved)
```

**Update Flow:**
```
Add new PDF to ./data
    ↓
Delete ./storage/ to trigger rebuild
    ↓
Restart server
    ↓
New index created
```

## Error Handling

### Validation Errors (400)
- Question too short/long
- Invalid JSON format
- Missing required fields

### Runtime Errors (500)
- RAG engine not initialized
- LLM API failure
- Document loading failure
- Index building failure

### All Errors Include
- HTTP status code
- Error message (detail)
- Error code (X-Error-Code header)

## Performance Characteristics

### Startup Time
- First run: 2-5 minutes (building index)
- Subsequent runs: 10-30 seconds (loading index + models)

### Query Time
- Embedding: ~100ms (local)
- Retrieval: ~50ms (vector similarity search)
- LLM inference: 1-3 seconds (API call)
- **Total**: ~2-4 seconds per query

### Memory Usage
- Embedding model: ~500MB
- Index (depends on document size): 100MB-1GB
- **Total**: ~1-2GB RAM

## Security Considerations

1. **HF_TOKEN**: Never commit, use .env
2. **CORS**: Configure for your domain in production
3. **Rate Limiting**: Add in production (not included)
4. **Input Validation**: Pydantic validates all inputs
5. **Logging**: Logs contain questions (consider privacy)
6. **API Keys**: Use environment variables, not code

## Extending the System

### Add Caching
```python
from redis import Redis
cache = Redis(decode_responses=True)

# In query endpoint:
cached = cache.get(question_hash)
if cached:
    return json.loads(cached)
```

### Add Rate Limiting
```python
from slowapi import Limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/ask")
@limiter.limit("5/minute")
async def ask_question(request: AskRequest):
    ...
```

### Add Database Logging
```python
# Log queries to database for analytics
await db.logs.insert_one({
    "question": request.question,
    "answer_length": len(answer),
    "source_count": len(sources),
    "timestamp": datetime.now(),
})
```

### Multi-Index Support
```python
# Support multiple document sets
indices = {
    "technical_docs": load_index("./storage/technical"),
    "manuals": load_index("./storage/manuals"),
}

@app.post("/ask/{index_name}")
async def ask_specific_index(index_name: str, request: AskRequest):
    index = indices.get(index_name)
    ...
```
