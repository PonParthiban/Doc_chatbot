# Production RAG API - Quick Reference

## Project Created ✓

```
rag-api/
├── app.py              # FastAPI entry point with endpoints
├── rag_engine.py       # RAG logic (index building/querying)
├── config.py           # Environment & configuration
├── models.py           # Pydantic request/response schemas
├── requirements.txt    # Python dependencies
├── .env.example        # Environment template
├── .gitignore          # Git ignore patterns
├── SETUP.md            # Setup and testing guide
└── ARCHITECTURE.md     # System design documentation
```

## Quick Start (5 steps)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Copy environment template
cp .env.example .env
# Edit .env and add your HF_TOKEN from https://huggingface.co/settings/tokens

# 3. Prepare data
mkdir -p data
# Add your PDF files to ./data/

# 4. Run the server
python app.py

# 5. Test the API
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What are the main topics?"}'
```

## Key Features

✓ Index persists to disk (./storage/) - no recomputation  
✓ Async FastAPI endpoints - non-blocking requests  
✓ Input validation via Pydantic schemas  
✓ Comprehensive error handling with proper HTTP status codes  
✓ Logging for startup, queries, and errors  
✓ CORS enabled for cross-origin requests  
✓ Environment variables for all secrets (HF_TOKEN)  
✓ Source attribution - know which documents contributed  
✓ Semantic chunking - intelligent document splitting  
✓ Production-ready - singleton pattern, lifespan management  

## File Overview

### app.py (4.5 KB)
- FastAPI application
- HTTP endpoints: GET /health, POST /ask, GET /
- Lifespan management (startup/shutdown)
- CORS middleware
- Error handling & logging

### rag_engine.py (6.2 KB)
- RAGEngine class (singleton)
- Document loading from ./data
- Index building with SemanticSplitterNodeParser
- Index persistence to ./storage
- Query processing with source extraction

### config.py (1.8 KB)
- Load .env file
- Validate required settings (HF_TOKEN)
- Centralized configuration
- Path management

### models.py (1.7 KB)
- AskRequest: {"question": str}
- AskResponse: {"answer": str, "sources": [...]}
- SourceMetadata: {"file": str, "score": float}
- ErrorResponse: {"detail": str, "error_code": str}

### requirements.txt
- FastAPI, Uvicorn
- LlamaIndex + integrations
- HuggingFace models
- Torch, Transformers

## API Endpoints

### Health Check
```bash
curl http://localhost:8000/health
```

### Ask Question
```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Your question here?"}'
```

### Interactive Docs
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Startup Process

1. Load .env → Config class
2. Validate HF_TOKEN present
3. FastAPI initializes
4. CORS middleware added
5. Lifespan startup:
   - RAGEngine singleton created
   - LLM & embedding models configured
   - Documents loaded from ./data
   - Check for existing index in ./storage
   - Build (1st run) or load (subsequent runs)
   - QueryEngine created
6. Server ready on port 8000

## Environment Variables

```env
HF_TOKEN=hf_YOUR_TOKEN_HERE  # Get from https://huggingface.co/settings/tokens
MODEL_ID=meta-llama/Llama-3.1-8B-Instruct
EMBEDDING_MODEL=all-MiniLM-L6-v2
LLM_MAX_TOKENS=512
LLM_TEMPERATURE=0.7
SIMILARITY_TOP_K=3
DATA_DIR=./data
STORAGE_DIR=./storage
API_PORT=8000
CORS_ORIGINS=*
```

## Request/Response Example

### Request
```json
{
  "question": "What are the main topics covered?"
}
```

### Response (200 OK)
```json
{
  "answer": "The documents cover machine learning, deep learning, and NLP. They discuss neural network architectures, training techniques, and real-world applications.",
  "sources": [
    {"file": "ml_guide.pdf", "score": 0.98},
    {"file": "deep_learning.pdf", "score": 0.94},
    {"file": "nlp_intro.pdf", "score": 0.87}
  ]
}
```

### Error Response (400 Bad Request)
```json
{
  "detail": "string should have at least 1 characters",
  "error_code": "VALIDATION_ERROR"
}
```

## Performance Notes

- **First startup**: 2-5 minutes (building index from PDFs)
- **Subsequent startups**: 10-30 seconds (loading existing index)
- **Per query**: 2-4 seconds (mostly LLM API latency)
- **Memory**: ~1-2 GB (embeddings + index)

## Important Notes

1. **HF_TOKEN is required** - Get from HuggingFace settings
2. **PDFs go in ./data** - Create directory and add files
3. **Index stored in ./storage** - Auto-created, add to .gitignore
4. **First build is slow** - Patience required for large document sets
5. **Async endpoints** - Non-blocking, handles concurrent requests
6. **Logging enabled** - Check console for startup details and query latency

## Next Steps

1. Copy .env.example → .env
2. Add HuggingFace API token to .env
3. Create ./data directory and add PDFs
4. Run: `python app.py`
5. Test: `curl -X POST http://localhost:8000/ask ...`
6. Browse docs: http://localhost:8000/docs

See **SETUP.md** for detailed instructions and troubleshooting.
See **ARCHITECTURE.md** for system design details.
