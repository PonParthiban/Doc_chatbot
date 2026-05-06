# Code Reference - Key Patterns

## 1. Request/Response Flow (app.py)

```python
# FastAPI endpoint with Pydantic validation
@app.post("/ask", response_model=AskResponse)
async def ask_question(request: AskRequest) -> AskResponse:
    """Input validation, RAG query, response building"""
    # request.question is automatically validated (1-1000 chars)
    
    rag_engine = get_rag_engine()
    answer, sources = rag_engine.query(request.question)
    
    source_metadata = [
        SourceMetadata(file=s["file"], score=s["score"])
        for s in sources
    ]
    
    return AskResponse(answer=answer, sources=source_metadata)
```

## 2. Configuration Loading (config.py)

```python
from dotenv import load_dotenv
import os
from pathlib import Path

# Auto-loads .env file
load_dotenv()

class Config:
    HF_TOKEN = os.getenv("HF_TOKEN")  # Required
    if not HF_TOKEN:
        raise ValueError("HF_TOKEN not set")
    
    # Defaults provided
    MODEL_ID = os.getenv("MODEL_ID", "meta-llama/Llama-3.1-8B-Instruct")
    DATA_DIR = Path(os.getenv("DATA_DIR", "./data"))
    STORAGE_DIR = Path(os.getenv("STORAGE_DIR", "./storage"))
```

## 3. Singleton RAG Engine (rag_engine.py)

```python
class RAGEngine:
    def __init__(self):
        self.index = None
        self.query_engine = None
    
    def initialize(self):
        """Called once on startup"""
        # Load or build index
        self.index = self._load_or_build_index()
        self.query_engine = self.index.as_query_engine(
            similarity_top_k=3
        )
    
    def query(self, question: str) -> Tuple[str, List[dict]]:
        """Called per request"""
        response = self.query_engine.query(question)
        answer = str(response)
        sources = self._extract_sources(response.source_nodes)
        return answer, sources

# Singleton getter
_rag_engine = None

def get_rag_engine() -> RAGEngine:
    global _rag_engine
    if _rag_engine is None:
        _rag_engine = RAGEngine()
    return _rag_engine
```

## 4. Index Persistence Logic

```python
def _load_or_build_index(self) -> VectorStoreIndex:
    """Smart loading: reuse existing, build if needed"""
    
    index_path = self.config.STORAGE_DIR / "docstore.json"
    
    # Try to load existing
    if index_path.exists():
        try:
            storage_context = StorageContext.from_defaults(
                persist_dir=str(self.config.STORAGE_DIR)
            )
            return load_index_from_storage(storage_context)
        except:
            pass  # Fall through to rebuild
    
    # Build new index
    docs = self._load_documents()
    parser = SemanticSplitterNodeParser(
        embed_model=Settings.embed_model,
        breakpoint_percentile_threshold=95
    )
    nodes = parser.get_nodes_from_documents(docs)
    index = VectorStoreIndex(nodes)
    
    # Persist for next run
    index.storage_context.persist(str(self.config.STORAGE_DIR))
    return index
```

## 5. Application Lifecycle (app.py)

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    # STARTUP
    print("Starting...")
    initialize_rag_engine()  # Load/build index once
    
    yield  # Server running
    
    # SHUTDOWN
    print("Shutting down...")

# FastAPI uses lifespan
app = FastAPI(lifespan=lifespan)
```

## 6. Pydantic Models (models.py)

```python
class AskRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="User question"
    )

class SourceMetadata(BaseModel):
    file: str
    score: float = Field(..., ge=0.0, le=1.0)

class AskResponse(BaseModel):
    answer: str
    sources: List[SourceMetadata]
```

## 7. Error Handling Pattern

```python
try:
    rag_engine = get_rag_engine()
    if not rag_engine.query_engine:
        raise HTTPException(
            status_code=500,
            detail="Engine not initialized",
            headers={"X-Error-Code": "ENGINE_NOT_READY"}
        )
    
    answer, sources = rag_engine.query(request.question)
    return AskResponse(answer=answer, sources=sources)

except ValueError as e:
    raise HTTPException(status_code=400, detail=str(e))
except Exception as e:
    logger.error(f"Error: {e}", exc_info=True)
    raise HTTPException(status_code=500, detail="Internal error")
```

## 8. Logging Configuration

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Usage throughout
logger.info("Starting RAG engine...")
logger.warning("Index not found, rebuilding...")
logger.error(f"Query failed: {e}", exc_info=True)
```

## 9. CORS Configuration

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=Config.CORS_ORIGINS,  # ["*"] or specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 10. Source Extraction from LLM Response

```python
def query(self, question: str) -> Tuple[str, List[dict]]:
    response = self.query_engine.query(question)
    
    # Extract answer text
    answer = str(response)
    
    # Extract and score sources
    sources = []
    if response.source_nodes:
        for node in response.source_nodes:
            file_name = node.metadata.get("file_name", "Unknown")
            score = float(node.score) if node.score else 0.0
            sources.append({"file": file_name, "score": score})
    
    return answer, sources
```

## Key Design Patterns Used

### 1. **Singleton Pattern** (RAGEngine)
- One instance across all requests
- Expensive initialization happens once
- Reused per query

### 2. **Dependency Injection** (get_rag_engine)
- Pass RAG engine to endpoints
- Easy to mock in tests
- Follows FastAPI patterns

### 3. **Lifespan Context Manager**
- Startup: initialize resources
- Shutdown: cleanup if needed
- Ensures proper lifecycle management

### 4. **Pydantic Models**
- Request validation automatically
- Response type safety
- Auto-generated OpenAPI docs

### 5. **Environment Configuration**
- .env file for secrets
- Defaults for optional settings
- Validation on import

### 6. **Error Hierarchy**
- Validation → 400 Bad Request
- Runtime → 500 Internal Server Error
- Proper HTTP semantics

## Common Modifications

### Change LLM Model
```python
# In .env:
MODEL_ID=meta-llama/Llama-3.2-1B-Instruct
LLM_TEMPERATURE=0.5
```

### Adjust Retrieved Documents
```python
# In .env:
SIMILARITY_TOP_K=5  # Get more context
```

### Change Embedding Model
```python
# In .env:
EMBEDDING_MODEL=sentence-transformers/all-mpnet-base-v2  # Larger, slower
```

### Enable Development Reload
```python
# In .env:
API_RELOAD=True
```

### Change CORS Policy
```python
# In .env:
CORS_ORIGINS=https://example.com,https://app.example.com
```

## Testing Patterns

### Health Check
```bash
curl http://localhost:8000/health
```

### Basic Query
```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "..."}'
```

### With Pretty Print
```bash
curl -s -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "..."}' | jq .
```

### Extract Just Answer
```bash
curl -s -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "..."}' | jq -r '.answer'
```

## Performance Optimization Tips

1. **Increase SIMILARITY_TOP_K** for accuracy (trade latency)
2. **Decrease SIMILARITY_TOP_K** for speed (trade quality)
3. **Use lighter embedding model** for speed (trade quality)
4. **Cache responses** for repeated queries
5. **Add rate limiting** in production
6. **Use Gunicorn workers** for concurrency

## Deployment Checklist

- [ ] HF_TOKEN set in environment
- [ ] .env not committed to git
- [ ] DATA_DIR contains PDFs
- [ ] CORS_ORIGINS set correctly
- [ ] API_RELOAD=False in production
- [ ] Logging configured for production
- [ ] Error handling tested
- [ ] Load tested for expected traffic
- [ ] Monitoring/alerting in place
