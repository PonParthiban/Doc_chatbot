# RAG API Setup and Testing Guide

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables
```bash
cp .env.example .env
# Edit .env and replace HF_TOKEN with your HuggingFace API token
# Get your token from: https://huggingface.co/settings/tokens
```

### 3. Prepare Data
```bash
mkdir -p data
# Add your PDF files to the ./data directory
# Example:
# cp /path/to/documents/*.pdf ./data/
```

### 4. Run the Server
```bash
# Development mode (with auto-reload)
python app.py

# Or using uvicorn directly
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

The server will start at `http://localhost:8000`

## API Endpoints

### Health Check
```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "service": "RAG API"
}
```

### Query Documentation
```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What are the main topics covered?"}'
```

Response:
```json
{
  "answer": "The documents cover machine learning, deep learning, and natural language processing. They discuss various neural network architectures, training techniques, and real-world applications.",
  "sources": [
    {"file": "ml_guide.pdf", "score": 0.98},
    {"file": "deep_learning.pdf", "score": 0.94},
    {"file": "nlp_introduction.pdf", "score": 0.87}
  ]
}
```

### Interactive API Documentation
Open your browser and visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Testing with curl

### Basic Query
```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is machine learning?"}'
```

### Multiple Questions (Test Script)
```bash
#!/bin/bash

questions=(
  "What are the key concepts?"
  "How are neural networks trained?"
  "What applications are discussed?"
)

for q in "${questions[@]}"; do
  echo "Question: $q"
  curl -X POST http://localhost:8000/ask \
    -H "Content-Type: application/json" \
    -d "{\"question\": \"$q\"}"
  echo ""
  echo "---"
  echo ""
done
```

## Project Structure

```
rag-api/
├── app.py                  # FastAPI application entry point
│                          # - Startup/shutdown events (lifespan)
│                          # - /health, /ask, / endpoints
│                          # - Error handling and CORS
│
├── rag_engine.py          # RAG logic module
│                          # - RAGEngine class (singleton pattern)
│                          # - Index loading/building/persistence
│                          # - Document processing and querying
│
├── config.py              # Configuration management
│                          # - Environment variable loading (.env)
│                          # - Config validation on import
│                          # - Path management
│
├── models.py              # Pydantic schemas
│                          # - AskRequest (question validation)
│                          # - AskResponse (answer + sources)
│                          # - ErrorResponse (error handling)
│
├── requirements.txt       # Python dependencies
│                          # - FastAPI, Uvicorn
│                          # - LlamaIndex + integrations
│                          # - PyTorch, Transformers
│
├── .env.example           # Environment variables template
│                          # - Copy to .env and fill in values
│
├── data/                  # PDF documents (create this)
│                          # - Place your PDF files here
│
└── storage/               # Persisted index (auto-created)
                          # - Vector index stored as docstore.json
                          # - Avoids recomputation on startup
```

## Key Features

✓ **Index Persistence**: Index built once, reused on restart  
✓ **Async Endpoints**: Non-blocking request handling  
✓ **Input Validation**: Pydantic models for request/response  
✓ **Error Handling**: Proper HTTP status codes and error messages  
✓ **Logging**: Track startup, queries, and errors  
✓ **CORS Enabled**: Cross-origin requests allowed  
✓ **Environment Config**: All secrets in .env file  
✓ **Semantic Chunking**: Smart document splitting  
✓ **Source Attribution**: Know which documents contributed to answers  

## Troubleshooting

### "HF_TOKEN environment variable not set"
- Copy `.env.example` to `.env`
- Add your HuggingFace token to `.env`
- Get token from: https://huggingface.co/settings/tokens

### "Data directory not found"
- Create `./data` directory
- Add PDF files to `./data`
- Restart the server

### "Waiting for model download"
- First startup downloads embedding model (~80MB)
- Subsequent startups are much faster
- Embedding model is cached locally

### "HuggingFace API timeout"
- Check your internet connection
- Verify HF_TOKEN is valid
- Increase timeout in config if needed

## Performance Tips

1. **Batch similar queries** - Leverage cached embeddings
2. **Adjust SIMILARITY_TOP_K** - Reduce from 3 to 1-2 for speed
3. **Use breakpoint_percentile_threshold** - Higher = fewer, larger chunks
4. **Cache responses** - Consider adding Redis for response caching
5. **Monitor logs** - Track query latency and optimize

## Production Deployment

For production, consider:
- Use proper ASGI server: Gunicorn + Uvicorn workers
- Set `API_RELOAD=False`
- Add monitoring and metrics
- Use proper secret management (not .env)
- Add rate limiting and request validation
- Use a proper logging system (e.g., ELK stack)
- Deploy with containerization (Docker)

Example Gunicorn command:
```bash
gunicorn app:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
```
