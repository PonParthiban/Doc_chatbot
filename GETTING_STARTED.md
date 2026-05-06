# Getting Started with RAG API

## ✅ What You Have

Your production-ready RAG API is complete with:

- **4 Python files** (462 lines total)
  - `app.py` - FastAPI application
  - `rag_engine.py` - RAG logic
  - `config.py` - Configuration
  - `models.py` - Request/response schemas

- **Complete documentation** (30+ KB)
  - README.md - Overview
  - SETUP.md - Detailed guide
  - ARCHITECTURE.md - System design
  - CODE_REFERENCE.md - Code patterns

- **Production features**
  - Index persistence (disk cache)
  - Async endpoints
  - Input validation
  - Error handling
  - Logging
  - CORS support

## 🚀 Quick Start (Copy & Paste)

### Step 1: Install Dependencies

```bash
cd /home/zyphor/coding/rag-api
pip install -r requirements.txt
```

This installs:
- FastAPI & Uvicorn
- LlamaIndex core + integrations
- HuggingFace transformers
- Pydantic for validation

### Step 2: Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and add your HuggingFace token:

```env
HF_TOKEN=hf_YOUR_TOKEN_HERE
```

Get token from: https://huggingface.co/settings/tokens

### Step 3: Prepare Documents

```bash
mkdir -p data
# Add your PDF files to ./data/
# Example:
# cp /path/to/documents/*.pdf ./data/
```

### Step 4: Run the Server

```bash
python app.py
```

You'll see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 5: Test the API

**Health check:**
```bash
curl http://localhost:8000/health
```

**Ask a question:**
```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is this about?"}'
```

**Interactive UI:**
Open: http://localhost:8000/docs (Swagger)

## 📋 Detailed Setup

### Prerequisites

- Python 3.8+
- pip or conda
- HuggingFace API token (free)
- PDF documents

### Installation Steps

1. **Clone or navigate to project:**
   ```bash
   cd /home/zyphor/coding/rag-api
   ```

2. **Create virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup configuration:**
   ```bash
   cp .env.example .env
   # Edit .env with your HF_TOKEN
   ```

5. **Prepare data:**
   ```bash
   mkdir -p data
   # Add PDF files to ./data/
   ```

6. **Run server:**
   ```bash
   python app.py
   ```

## 🧪 Testing the API

### Using curl

**List all endpoints:**
```bash
curl http://localhost:8000/
```

**Health check:**
```bash
curl http://localhost:8000/health
```

**Ask a simple question:**
```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What are the main topics?"}'
```

**Pretty print response:**
```bash
curl -s -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Summarize the content"}' | jq .
```

**Extract just the answer:**
```bash
curl -s -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is X?"}' | jq -r '.answer'
```

### Using Python requests

```python
import requests

url = "http://localhost:8000/ask"
payload = {"question": "What are the main topics?"}

response = requests.post(url, json=payload)
print(response.json())
```

### Using web browser

1. Open: http://localhost:8000/docs
2. Click "POST /ask"
3. Click "Try it out"
4. Enter your question
5. Click "Execute"

## ⚙️ Configuration Options

Edit `.env` to customize:

```env
# Required
HF_TOKEN=hf_YOUR_TOKEN_HERE

# LLM Configuration
MODEL_ID=meta-llama/Llama-3.1-8B-Instruct
LLM_MAX_TOKENS=512
LLM_TEMPERATURE=0.7

# Embedding Configuration
EMBEDDING_MODEL=all-MiniLM-L6-v2

# Index Configuration
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

## 🔍 Troubleshooting

### Issue: "HF_TOKEN environment variable not set"

**Solution:**
```bash
cp .env.example .env
# Edit .env and add your HuggingFace token
```

### Issue: "Data directory not found: ./data"

**Solution:**
```bash
mkdir -p data
# Add PDF files to ./data/
```

### Issue: "Server is slow on first startup"

**Reason:** Building the vector index for the first time
- First run: 2-5 minutes (expected)
- Subsequent runs: 10-30 seconds (index is cached)

**Solution:** Be patient on first run!

### Issue: "HuggingFace API timeout"

**Cause:** Network issue or API overloaded

**Solutions:**
- Check internet connection
- Verify HF_TOKEN is correct and active
- Try again later
- Adjust LLM model to faster alternative

### Issue: "404 Not Found" for /ask

**Cause:** Server might not be running

**Solution:**
```bash
# Make sure server is running
python app.py
# Then test again
curl -X POST http://localhost:8000/ask ...
```

## 📊 Performance Expectations

| Scenario | Time |
|----------|------|
| First startup | 2-5 minutes |
| Subsequent startups | 10-30 seconds |
| Per query | 2-4 seconds |
| Memory usage | ~1-2 GB |

*Times depend on PDF size, internet speed, and hardware*

## 📚 Where to Go Next

1. **Learn the code:**
   - Read: CODE_REFERENCE.md
   - Review: app.py, rag_engine.py

2. **Understand architecture:**
   - Read: ARCHITECTURE.md
   - Review: System design diagrams

3. **Production deployment:**
   - Read: SETUP.md (Production Deployment section)
   - Learn: Docker, Kubernetes, cloud platforms

4. **Extend functionality:**
   - Add caching (Redis)
   - Add rate limiting
   - Add authentication
   - Add monitoring/metrics

## 🎯 Common Customizations

### Change the LLM model

Edit `.env`:
```env
MODEL_ID=mistralai/Mistral-7B-Instruct-v0.1
LLM_TEMPERATURE=0.3
```

### Get more or fewer results

Edit `.env`:
```env
SIMILARITY_TOP_K=5  # More results (slower)
SIMILARITY_TOP_K=1  # Fewer results (faster)
```

### Use a different embedding model

Edit `.env`:
```env
EMBEDDING_MODEL=sentence-transformers/all-mpnet-base-v2
```

### Enable development auto-reload

Edit `.env`:
```env
API_RELOAD=True
```

### Restrict CORS origins

Edit `.env`:
```env
CORS_ORIGINS=https://example.com,https://app.example.com
```

## 🚀 Deployment Options

### Local Development

```bash
python app.py
```

### Production (Gunicorn)

```bash
pip install gunicorn

gunicorn app:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
```

### Docker

```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

Build and run:
```bash
docker build -t rag-api .
docker run -p 8000:8000 -e HF_TOKEN=your_token rag-api
```

### Cloud Deployment (AWS, GCP, Azure)

See SETUP.md for detailed cloud deployment guides.

## 📞 Support Resources

- **FastAPI docs:** https://fastapi.tiangolo.com/
- **LlamaIndex docs:** https://docs.llamaindex.ai/
- **HuggingFace docs:** https://huggingface.co/docs
- **Project docs:** README.md, SETUP.md, ARCHITECTURE.md

## ✅ Verification Checklist

- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` created with HF_TOKEN
- [ ] `./data` directory created with PDF files
- [ ] Server started (`python app.py`)
- [ ] Health check works (`curl localhost:8000/health`)
- [ ] API query works (`curl -X POST localhost:8000/ask ...`)
- [ ] Swagger UI loads (`http://localhost:8000/docs`)
- [ ] No error messages in console

## 🎉 You're Done!

Your RAG API is ready to use!

**Next steps:**
1. Start the server: `python app.py`
2. Visit Swagger UI: http://localhost:8000/docs
3. Ask your first question
4. Explore the code and documentation
5. Deploy to production when ready

Happy querying! 🚀
