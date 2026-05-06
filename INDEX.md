# RAG API Documentation Index

Complete documentation for your production-ready RAG backend.

## Quick Navigation

### 🚀 Getting Started (5 minutes)
- **GETTING_STARTED.md** - Step-by-step setup guide
  - Installation
  - Configuration  
  - Testing
  - Troubleshooting
  - Common customizations

### 📖 Core Documentation
1. **README.md** - Overview & quick reference
   - Feature summary
   - API endpoints
   - Example request/response
   - Project structure

2. **SETUP.md** - Detailed setup guide
   - Complete installation steps
   - Testing procedures
   - Troubleshooting tips
   - Performance optimization
   - Production deployment

3. **ARCHITECTURE.md** - System design
   - Architecture overview
   - Request flow diagrams
   - Startup sequence
   - Data persistence strategy
   - Performance characteristics
   - Security considerations
   - Extension examples

### 💻 Code Reference
- **CODE_REFERENCE.md** - Code patterns & examples
  - 10 key code patterns
  - Design patterns used
  - Common modifications
  - Testing patterns
  - Deployment checklist

### 📝 Configuration
- **.env.example** - Environment variables template
  - Copy to `.env` and add your HF_TOKEN
  - All configuration options explained

## File Organization

```
rag-api/
├── Python Code (462 lines total)
│   ├── app.py              (169 lines) - FastAPI entry point
│   ├── rag_engine.py       (177 lines) - RAG logic
│   ├── config.py           (61 lines)  - Configuration
│   └── models.py           (55 lines)  - Pydantic schemas
│
├── Configuration
│   ├── requirements.txt    - Dependencies
│   ├── .env.example        - Environment template
│   └── .gitignore          - Git ignore
│
├── Documentation (30+ KB)
│   ├── GETTING_STARTED.md  - Quickstart guide ⭐ START HERE
│   ├── README.md           - Overview
│   ├── SETUP.md            - Detailed setup
│   ├── ARCHITECTURE.md     - System design
│   ├── CODE_REFERENCE.md   - Code patterns
│   └── INDEX.md            - This file
│
└── Testing
    └── test_api.sh        - Example curl requests
```

## Documentation by Use Case

### I want to start immediately
1. Read: **GETTING_STARTED.md**
2. Run: `python app.py`
3. Test: Visit http://localhost:8000/docs

### I want to understand the code
1. Read: **README.md** (overview)
2. Read: **CODE_REFERENCE.md** (patterns)
3. Browse: **app.py** and **rag_engine.py**

### I want to understand the architecture
1. Read: **ARCHITECTURE.md**
2. Review: System design diagrams
3. Study: Data flow explanation

### I want to customize it
1. Check: **GETTING_STARTED.md** (Common Customizations section)
2. Read: **CODE_REFERENCE.md** (Modifications section)
3. Edit: `.env` file

### I want to deploy it
1. Read: **SETUP.md** (Production Deployment section)
2. Check: **CODE_REFERENCE.md** (Deployment Checklist)
3. Choose: Docker, Gunicorn, or cloud platform

### I'm having issues
1. Check: **GETTING_STARTED.md** (Troubleshooting section)
2. Check: **SETUP.md** (Troubleshooting section)
3. Review: **CODE_REFERENCE.md** (Common Modifications)

## API Endpoints Reference

| Method | Path | Purpose | Input | Output |
|--------|------|---------|-------|--------|
| POST | /ask | Query RAG engine | `{"question": "..."}` | `{"answer": "...", "sources": [...]}` |
| GET | /health | Health check | None | `{"status": "healthy"}` |
| GET | / | Service info | None | Endpoints list |
| GET | /docs | Swagger UI | None | Interactive API docs |
| GET | /redoc | ReDoc | None | Alternative API docs |

## Configuration Reference

### Required
```env
HF_TOKEN=hf_YOUR_TOKEN_HERE
```

### Optional (with defaults)
```env
# LLM
MODEL_ID=meta-llama/Llama-3.1-8B-Instruct
LLM_MAX_TOKENS=512
LLM_TEMPERATURE=0.7

# Embedding
EMBEDDING_MODEL=all-MiniLM-L6-v2

# Index
SIMILARITY_TOP_K=3
BREAKPOINT_PERCENTILE_THRESHOLD=95

# Paths
DATA_DIR=./data
STORAGE_DIR=./storage

# Server
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=False

# CORS
CORS_ORIGINS=*
```

## Performance Metrics

| Metric | Value |
|--------|-------|
| First startup | 2-5 minutes |
| Subsequent startups | 10-30 seconds |
| Per-query latency | 2-4 seconds |
| Memory usage | ~1-2 GB |
| Index size | 100MB-1GB (depends on PDFs) |

## Key Features

✅ Index Persistence - No recomputation on restart
✅ Async Endpoints - Non-blocking request handling
✅ Input Validation - Pydantic models
✅ Error Handling - Proper HTTP status codes
✅ Logging - Track all operations
✅ CORS - Web integration ready
✅ Environment Config - Secrets in .env
✅ Auto Docs - Swagger UI + ReDoc
✅ Type Safety - Full Python typing
✅ Source Attribution - Know which docs helped
✅ Production-Ready - Singleton, lifespan management
✅ Semantic Chunking - Smart document splitting

## Common Commands

```bash
# Setup
pip install -r requirements.txt
cp .env.example .env

# Run
python app.py

# Test
curl http://localhost:8000/health
curl -X POST http://localhost:8000/ask -d '{"question": "..."}'

# Development (with reload)
API_RELOAD=True python app.py

# Production (Gunicorn)
gunicorn app:app --workers 4 --worker-class uvicorn.workers.UvicornWorker
```

## Directory Structure

### data/ (Create this)
Place PDF documents here for RAG processing.

### storage/ (Auto-created)
Contains the persisted vector index. Delete to force rebuild.

### .env (Create from .env.example)
Environment variables including HF_TOKEN.

## Troubleshooting Quick Links

- HF_TOKEN not set? → **GETTING_STARTED.md** > Troubleshooting
- Data directory missing? → **GETTING_STARTED.md** > Troubleshooting
- Slow startup? → **GETTING_STARTED.md** > Performance Expectations
- Customization? → **CODE_REFERENCE.md** > Common Modifications
- Deployment? → **SETUP.md** > Production Deployment

## What's Next?

1. **Start here:** Read **GETTING_STARTED.md**
2. **Then:** Run `python app.py`
3. **Next:** Visit http://localhost:8000/docs
4. **Explore:** Review the code
5. **Customize:** Edit `.env` as needed
6. **Deploy:** Follow production deployment guide

## File Purposes Summary

| File | Purpose |
|------|---------|
| **app.py** | FastAPI application with endpoints and lifespan management |
| **rag_engine.py** | RAG logic: document loading, indexing, querying |
| **config.py** | Load and validate environment variables |
| **models.py** | Pydantic request/response validation schemas |
| **requirements.txt** | Python package dependencies |
| **.env.example** | Environment variables template |
| **.gitignore** | Git ignore patterns |
| **GETTING_STARTED.md** | Step-by-step quickstart guide ⭐ |
| **README.md** | Overview and quick reference |
| **SETUP.md** | Detailed setup and troubleshooting |
| **ARCHITECTURE.md** | System design and optimization |
| **CODE_REFERENCE.md** | Code patterns and customization |
| **test_api.sh** | Example curl requests |

---

## Quick Answers

**Q: Where do I start?**
A: Read **GETTING_STARTED.md**

**Q: How do I set it up?**
A: Follow the 5-step quickstart in **GETTING_STARTED.md**

**Q: How do I run it?**
A: `python app.py` after setup

**Q: How do I test it?**
A: Visit http://localhost:8000/docs or run `bash test_api.sh`

**Q: How do I customize it?**
A: Edit `.env` and review **CODE_REFERENCE.md**

**Q: How do I deploy it?**
A: See **SETUP.md** > Production Deployment

**Q: What if something breaks?**
A: Check **GETTING_STARTED.md** > Troubleshooting

---

**Ready to start?** Begin with **GETTING_STARTED.md** 🚀
