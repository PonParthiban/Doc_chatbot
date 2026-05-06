# Frontend Quick Start

## 🚀 Start the Complete Stack

### Step 1: Ensure Backend is Running

```bash
cd /home/zyphor/coding/rag-api
python app.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
✓ Static files mounted from /home/zyphor/coding/rag-api
✓ RAG Engine initialized successfully!
```

### Step 2: Open Your Browser

```
http://localhost:8000
```

That's it! The frontend is now served directly from your FastAPI backend.

---

## 📝 What You See

1. **Header** - "RAG Chat" title
2. **Welcome Message** - Get started instructions
3. **Chat Area** - Empty (ready for your first message)
4. **Input Box** - Type your question
5. **Send Button** - Green button to send

---

## 🧪 Try It Out

1. **Type a question** about your documents
   - Example: "What is machine learning?"
   
2. **Press Enter or click the Send button**

3. **Watch the magic**
   - Loading indicator appears ("Thinking...")
   - AI generates an answer
   - Sources show which documents helped

---

## ⌨️ Keyboard Shortcuts

| Key | Action |
|-----|--------|
| Enter | Send message |
| Ctrl/Cmd + A | Select all text |
| Escape | (Clear input - not implemented) |

---

## 🎨 UI Components

### User Message
- Green bubble on the right
- Your question in white text

### AI Response
- Light gray bubble on the left
- Answer text with proper formatting

### Sources
- File name with 📎 icon
- Relevance score as percentage (0-100%)
- Green badges for scores

### Loading State
- Three bouncing dots
- "Thinking..." text
- Input disabled while loading

### Error Message
- Red text with ❌ icon
- Clear error message from backend

---

## 🔧 Configuration

### Change Backend URL

If your backend is not at `localhost:8000`:

Edit **script.js**:
```javascript
const BASE_URL = 'http://your-backend-url:8000';
```

### Change Colors

Edit **style.css**:
```css
:root {
    --primary-color: #10a37f;      /* Green */
    --user-bg: #10a37f;            /* User message color */
    --bot-bg: #f7f7f7;             /* Bot message background */
}
```

### Change Welcome Message

Edit **index.html**:
```html
<div class="message bot-message welcome-message">
    <div class="message-content">
        <p>Your custom welcome text here</p>
    </div>
</div>
```

---

## 📱 Mobile Experience

The frontend is fully responsive:

- **Desktop** (1024px+) - Full width layout
- **Tablet** (768px) - Adjusted spacing
- **Mobile** (480px) - Compact view with touch-friendly buttons

Works great on:
- iPhone/iPad
- Android phones
- Tablets
- Desktop browsers

---

## 🐛 Troubleshooting

### "Connection refused" or "Failed to connect"
- [ ] Is the FastAPI server running? (`python app.py`)
- [ ] Is it on `localhost:8000`?
- [ ] Try refreshing the page (Ctrl+R)

### Messages not appearing
- [ ] Check browser console (F12)
- [ ] Are there any JavaScript errors?
- [ ] Try a different browser
- [ ] Clear browser cache (Ctrl+Shift+Del)

### Input field not responding
- [ ] Click the input field first
- [ ] Check if it's disabled (grayed out)
- [ ] Try refreshing the page

### Slow response times
- [ ] This is normal for first request (building index)
- [ ] Check RAG backend logs
- [ ] Typical: 2-4 seconds per query

### Mobile keyboard not showing
- [ ] Try clicking the input field again
- [ ] Some browsers have keyboard issues
- [ ] Try a different mobile browser

---

## 💡 Tips

1. **First startup is slow** - Backend builds the index (2-5 min)
2. **Ask clear questions** - Better answers for specific queries
3. **Multiple documents** - Add more PDFs to `./data/` for richer context
4. **Error messages help** - They tell you what went wrong
5. **Sources matter** - Check which documents contributed to answers

---

## 🚀 Next Steps

1. ✅ Frontend is running
2. 📄 Add PDF documents to `./data/`
3. 🔄 Restart backend (Ctrl+C and `python app.py`)
4. ❓ Ask questions about your documents
5. 🚢 Deploy to production (see SETUP.md)

---

## 🎯 Full Feature List

✅ Chat interface
✅ Real-time responses
✅ Source attribution
✅ Loading states
✅ Error handling
✅ Responsive design
✅ Keyboard support
✅ Auto-scroll
✅ Input validation
✅ Error messages
✅ Mobile-optimized
✅ Accessibility features

---

## 📖 Documentation

- **FRONTEND.md** - Complete frontend documentation
- **README.md** - Project overview
- **CODE_REFERENCE.md** - Code patterns
- **SETUP.md** - Production deployment

---

## ❓ Common Questions

**Q: Can I deploy this to production?**
A: Yes! See SETUP.md for deployment options (Docker, Gunicorn, AWS, etc.)

**Q: Can I customize the colors/design?**
A: Yes! Edit `style.css` for colors or `index.html` for layout.

**Q: Does it work offline?**
A: No - it needs a connection to your RAG backend API.

**Q: Can I use it on my phone?**
A: Yes! It's fully responsive and mobile-friendly.

**Q: How do I add more documents?**
A: Add PDFs to `./data/` and restart the backend.

**Q: Can I export conversations?**
A: Not yet - but you can copy/paste messages. Could be a future feature.

---

**Ready to ask your first question?** 🎉

Open http://localhost:8000 and start chatting!
