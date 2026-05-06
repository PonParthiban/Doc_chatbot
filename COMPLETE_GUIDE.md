# Complete RAG System - Backend + Frontend

Everything you need to run a production-ready RAG application with chat UI.

## 🎯 What You Have

**Backend (FastAPI + LlamaIndex)**
- RESTful API with `/ask` endpoint
- Vector index from PDF documents
- HuggingFace embeddings & LLM
- Index persistence to disk

**Frontend (Vanilla HTML/CSS/JavaScript)**
- Modern chat interface
- Real-time message exchange
- Loading states & error handling
- Source attribution
- Responsive mobile design

**Integration**
- Frontend served directly from backend
- CORS configured for web requests
- Ready for production deployment

## 🚀 Quickstart (3 Steps)

### Step 1: Install & Configure

```bash
cd /home/zyphor/coding/rag-api
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add HF_TOKEN
```

### Step 2: Add Documents

```bash
mkdir -p data
# Copy your PDF files to ./data/
cp /path/to/documents/*.pdf ./data/
```

### Step 3: Run Everything

```bash
python app.py
```

Then open: **http://localhost:8000**

## 📂 Project Structure

```
rag-api/
├── Backend (Python)
│   ├── app.py                  FastAPI app + static file serving
│   ├── rag_engine.py           RAG logic (indexing + querying)
│   ├── config.py               Environment configuration
│   ├── models.py               Pydantic request/response schemas
│   └── requirements.txt        Python dependencies
│
├── Frontend (Web UI)
│   ├── index.html              Chat interface structure
│   ├── style.css               Styling & animations
│   ├── script.js               Chat logic & API calls
│   └── FRONTEND.md             Frontend documentation
│
├── Configuration
│   ├── .env.example            Environment template
│   └── .gitignore              Git ignore patterns
│
└── Documentation
    ├── GETTING_STARTED.md      Backend setup guide
    ├── FRONTEND_QUICKSTART.md  Frontend guide
    ├── SETUP.md                Detailed setup & deployment
    ├── ARCHITECTURE.md         System design
    ├── CODE_REFERENCE.md       Code patterns
    └── README.md               Overview
```

## 🔌 API Endpoints

### User-Facing
- `GET /` - Serves frontend (index.html)
- `GET /docs` - Swagger API documentation
- `GET /redoc` - Alternative API documentation

### Backend API
- `POST /ask` - Query the RAG engine
  ```json
  Request: {"question": "What is X?"}
  Response: {
    "answer": "...",
    "sources": [
      {"file": "doc.pdf", "score": 0.95}
    ]
  }
  ```

### Health Check
- `GET /health` - Health check endpoint

## 💻 Frontend Features

### UI Components
- **Header** - Green gradient with title
- **Chat Area** - Message bubbles (user & bot)
- **Loading Indicator** - Animated spinner
- **Sources** - File names with relevance scores
- **Input Area** - Text input + send button
- **Error Messages** - Red error notifications

### Interactions
- Type question → Press Enter or click Send
- Waiting state shows "Thinking..." spinner
- Messages auto-scroll as they appear
- Input clears after sending
- Errors show in red with details

### Responsive Design
- Desktop (1024px+) - Full layout
- Tablet (768px) - Adjusted spacing
- Mobile (480px) - Compact touch-friendly

## ⚙️ Configuration

### Backend (.env)
```env
# Required
HF_TOKEN=hf_YOUR_TOKEN_HERE

# Optional (defaults provided)
MODEL_ID=meta-llama/Llama-3.1-8B-Instruct
EMBEDDING_MODEL=all-MiniLM-L6-v2
SIMILARITY_TOP_K=3
API_PORT=8000
CORS_ORIGINS=*
```

### Frontend (script.js)
```javascript
// Change backend URL if deployed elsewhere
const BASE_URL = 'http://localhost:8000';
```

### Styling (style.css)
```css
:root {
    --primary-color: #10a37f;      /* Green */
    --user-bg: #10a37f;            /* User message bg */
    --bot-bg: #f7f7f7;             /* Bot message bg */
}
```

## 🎯 Typical Usage Flow

1. **User opens browser**
   - http://localhost:8000 loads
   - Frontend displayed with welcome message
   - Input field focused and ready

2. **User types a question**
   - "What is machine learning?"
   - Hits Enter or clicks Send button

3. **Frontend sends request**
   - POST /ask with question
   - Shows loading indicator
   - Disables input/button

4. **Backend processes**
   - Loads RAG engine if first request
   - Embeds question (local)
   - Searches vector index
   - Calls LLM API
   - Extracts answer + sources

5. **Frontend receives response**
   - Hides loading indicator
   - Displays user message
   - Displays AI response
   - Shows sources with scores
   - Re-enables input
   - Auto-scrolls to bottom

6. **User can continue**
   - Ask follow-up questions
   - Pattern repeats

## 📊 Performance

| Metric | Value |
|--------|-------|
| First startup | 2-5 minutes |
| Subsequent startups | 10-30 seconds |
| Page load time | <1 second |
| Per-query latency | 2-4 seconds |
| Memory usage | ~1-2 GB |
| Concurrent users | Scales with hardware |

## 🔒 Security

- HF_TOKEN in .env (not in code)
- CORS configured
- Input validation (Pydantic)
- Error handling (no sensitive data in responses)
- HTTPS ready (configure for production)

## 🚀 Deployment Options

### Local Development
```bash
python app.py
# Open http://localhost:8000
```

### Production with Gunicorn
```bash
pip install gunicorn
gunicorn app:app --workers 4 --worker-class uvicorn.workers.UvicornWorker
```

### Docker
```bash
docker build -t rag-api .
docker run -p 8000:8000 -e HF_TOKEN=your_token rag-api
```

### Cloud Platforms
- AWS EC2 / ECS / Lambda
- Google Cloud Run
- Azure Container Instances
- Heroku
- DigitalOcean

## 📚 File Descriptions

### Backend Files
- **app.py** - FastAPI app with endpoints + static file serving
- **rag_engine.py** - RAG logic (document loading, indexing, querying)
- **config.py** - Environment variable management
- **models.py** - Pydantic request/response validation
- **requirements.txt** - Python package dependencies

### Frontend Files
- **index.html** - Chat UI HTML structure
- **style.css** - All styling and animations (490 lines)
- **script.js** - Chat logic and API communication (266 lines)

### Configuration
- **.env.example** - Environment variables template
- **.gitignore** - Git ignore patterns
- **requirements.txt** - Python dependencies

### Documentation
- **README.md** - Project overview
- **GETTING_STARTED.md** - Backend setup guide
- **FRONTEND_QUICKSTART.md** - Frontend quick start
- **SETUP.md** - Detailed setup and deployment
- **ARCHITECTURE.md** - System design and optimization
- **CODE_REFERENCE.md** - Code patterns and customization
- **FRONTEND.md** - Frontend feature documentation
- **INDEX.md** - Documentation index
- **COMPLETE_GUIDE.md** - This file

## 🛠️ Common Tasks

### Change LLM Model
Edit `.env`:
```env
MODEL_ID=mistralai/Mistral-7B-Instruct-v0.1
```

### Get More/Fewer Results
Edit `.env`:
```env
SIMILARITY_TOP_K=5  # More results
SIMILARITY_TOP_K=1  # Fewer results
```

### Change Colors
Edit `style.css`:
```css
:root {
    --primary-color: #your-color;
}
```

### Add Custom Welcome Message
Edit `index.html` welcome-message div.

### Deploy to Production
1. Set up environment variables securely
2. Configure CORS_ORIGINS
3. Use production deployment command
4. Set up monitoring/logging
5. Configure HTTPS

## 🐛 Troubleshooting

### Frontend won't load
- [ ] Is backend running? (`python app.py`)
- [ ] Try http://localhost:8000 (not 8001)
- [ ] Check browser console (F12)
- [ ] Refresh page (Ctrl+R)

### Messages not sending
- [ ] Check API is running
- [ ] Verify BASE_URL in script.js
- [ ] Look for JavaScript errors (F12)
- [ ] Test API with curl

### Slow responses
- [ ] First request builds index (2-5 min) - normal
- [ ] Check backend logs
- [ ] Typical latency: 2-4 seconds

### Connection refused
- [ ] Backend must be running
- [ ] Check port 8000 is available
- [ ] Try `lsof -i :8000` to check

## 📈 Scaling

### Single User
- Current setup handles this well
- 1-2 GB RAM sufficient

### Multiple Users
- Use Gunicorn with multiple workers
- Add load balancer (Nginx)
- Consider Redis for caching

### High Traffic
- Deploy to cloud (AWS, GCP)
- Use auto-scaling
- Add database for conversation history
- Monitor with Prometheus/Grafana

## 🎓 Learning Resources

- **FastAPI Docs** - https://fastapi.tiangolo.com/
- **LlamaIndex Docs** - https://docs.llamaindex.ai/
- **HuggingFace Docs** - https://huggingface.co/docs
- **Vanilla JS** - https://developer.mozilla.org/en-US/docs/Web/JavaScript

## 🤝 Contributing

Want to improve this? Consider:
- [ ] Dark mode toggle
- [ ] Message export to PDF
- [ ] Conversation history
- [ ] Copy answer button
- [ ] Voice input
- [ ] Markdown formatting
- [ ] Multi-language support

## 📞 Support

If you run into issues:
1. Check the documentation (see INDEX.md)
2. Review FRONTEND_QUICKSTART.md for quick answers
3. Check browser console (F12) for errors
4. Test backend API with curl
5. Review logs from `python app.py`

## ✅ Verification Checklist

Before going to production:
- [ ] Dependencies installed
- [ ] .env configured with HF_TOKEN
- [ ] PDFs added to ./data/
- [ ] Backend starts successfully
- [ ] Frontend loads at http://localhost:8000
- [ ] Can ask questions and get answers
- [ ] Sources appear correctly
- [ ] Error messages show on bad input
- [ ] Mobile view works
- [ ] No console errors (F12)

## 🎉 Ready to Go!

You now have a complete, production-ready RAG system with:
- ✅ FastAPI backend
- ✅ Modern chat UI
- ✅ Full documentation
- ✅ Error handling
- ✅ Responsive design
- ✅ Easy deployment

**Next step:** `python app.py` → Open http://localhost:8000

---

Built with ❤️ for seamless RAG interactions.
