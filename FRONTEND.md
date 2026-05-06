# RAG Chat Frontend

Clean, modern chat interface for the RAG API backend. Built with vanilla HTML, CSS, and JavaScript (no frameworks).

## Features

✅ **Chat Interface** - Modern, ChatGPT-like design
✅ **Real-time Messages** - Instant feedback and responses
✅ **Loading States** - "Thinking..." indicator while waiting
✅ **Source Attribution** - Shows which documents contributed to the answer
✅ **Error Handling** - Graceful error messages
✅ **Responsive Design** - Works on desktop, tablet, and mobile
✅ **Keyboard Support** - Send with Enter key
✅ **Auto-scroll** - Automatically scrolls to latest messages
✅ **Input Validation** - Prevents empty message submission

## Files

- **index.html** - Page structure and layout
- **style.css** - Responsive styling (ChatGPT-like theme)
- **script.js** - Chat logic and API communication

## Setup

### Option 1: Serve from FastAPI (Recommended)

The frontend files are served directly from your FastAPI backend:

1. Start your FastAPI server:
   ```bash
   cd /home/zyphor/coding/rag-api
   python app.py
   ```

2. Open your browser:
   ```
   http://localhost:8000
   ```

The backend automatically serves `index.html` when you visit the root URL.

### Option 2: Serve Locally (Development)

Use Python's built-in HTTP server:

```bash
# In the rag-api directory
python -m http.server 8080
```

Then open: `http://localhost:8080`

## Configuration

Edit **script.js** to change the backend URL:

```javascript
const BASE_URL = 'http://localhost:8000';
```

Change `localhost:8000` to your backend URL if deployed elsewhere.

## How It Works

1. **User enters a question** and clicks "Send" or presses Enter
2. **Input is validated** (must not be empty)
3. **Loading indicator** appears ("Thinking...")
4. **API request** is sent to `POST /ask`
5. **Response** with answer and sources is received
6. **Messages appear** in chat with proper formatting
7. **Sources** are displayed with relevance scores
8. **Input is cleared** and ready for next question

## Code Structure

### HTML (`index.html`)
- Header with title
- Chat messages container (dynamically populated)
- Loading indicator
- Input area with send button

### CSS (`style.css`)
- Modern gradient colors (green theme)
- ChatGPT-like message bubbles
- Responsive grid layout
- Smooth animations and transitions
- Mobile-optimized design
- Custom scrollbar styling

### JavaScript (`script.js`)
Key functions:
- `sendMessage()` - Main handler for sending messages
- `queryRagBackend()` - Calls the RAG API
- `appendMessage()` - Adds message to chat
- `renderSources()` - Creates source badges
- `appendErrorMessage()` - Shows errors
- `setLoadingState()` - Toggles loading UI
- `scrollToBottom()` - Auto-scrolls chat

## Styling

### Colors
- **Primary Green**: `#10a37f` (send button, highlights)
- **Text**: `#343541` (dark gray)
- **Bot Background**: `#f7f7f7` (light gray)
- **User Background**: `#10a37f` (green)

### Responsive Breakpoints
- **Desktop**: Full width layout
- **Tablet** (≤768px): Adjusted padding and font sizes
- **Mobile** (≤480px): Compact view, larger touch targets

## Features Explained

### Loading State
While waiting for the backend:
- Input field is disabled
- Send button is disabled
- Animated loading indicator shows "Thinking..."
- Prevents multiple simultaneous requests

### Error Handling
If an error occurs:
- Network error → "Failed to connect"
- Server error → Error message from backend
- Empty input → Silently ignored (no request sent)
- User-friendly error format with ❌ icon

### Auto-scroll
Chat automatically scrolls to the bottom when:
- New message is added
- Loading indicator appears
- Response is received

Uses `requestAnimationFrame` for smooth scrolling.

### Source Attribution
After each response, sources are shown:
- File name (📎 icon)
- Relevance score as percentage (0-100%)
- Color-coded badges
- Sorted by score (highest first)

## Customization

### Change Color Scheme
Edit variables in `style.css`:
```css
:root {
    --primary-color: #10a37f;      /* Main color */
    --primary-dark: #0d8866;        /* Darker shade */
    --user-bg: #10a37f;             /* User message bg */
    --bot-bg: #f7f7f7;              /* Bot message bg */
}
```

### Change Welcome Message
Edit in `index.html`:
```html
<div class="message bot-message welcome-message">
    <div class="message-content">
        <p>Your custom welcome message here</p>
    </div>
</div>
```

### Change API Base URL
Edit in `script.js`:
```javascript
const BASE_URL = 'https://your-api-domain.com';
```

## Browser Compatibility

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

Uses modern CSS and JavaScript features:
- CSS Grid & Flexbox
- Fetch API
- ES6+ JavaScript
- CSS Custom Properties

## Performance

- **No dependencies** - Pure vanilla code
- **Lightweight** - ~20KB total (HTML + CSS + JS)
- **Fast loading** - Instantly responsive
- **Smooth animations** - 60fps transitions
- **Efficient rendering** - DOM updates only when needed

## Troubleshooting

### "Network error" or "Failed to get response"
- Check that FastAPI backend is running
- Verify `BASE_URL` in `script.js` is correct
- Check browser console (F12) for CORS errors

### Messages not appearing
- Check browser console for JavaScript errors
- Verify the `/ask` endpoint in backend works
- Test with `curl`:
  ```bash
  curl -X POST http://localhost:8000/ask \
    -H "Content-Type: application/json" \
    -d '{"question": "test"}'
  ```

### Input field won't focus on mobile
- Clear browser cache
- Try a different browser
- Check if there's a keyboard overlay

### Scrolling is jumpy
- This is a known issue on some mobile browsers
- Workaround: Close the on-screen keyboard

## Future Enhancements

Possible additions:
- [ ] Dark mode toggle
- [ ] Message timestamps
- [ ] Copy answer to clipboard
- [ ] Export conversation as PDF
- [ ] Message history persistence
- [ ] Typing indicator
- [ ] Markdown formatting for responses
- [ ] Voice input (speech-to-text)
- [ ] Download sources
- [ ] Regenerate last response

## Files Structure

```
rag-api/
├── index.html      ← Main HTML structure
├── style.css       ← Styling and layout
├── script.js       ← Chat logic
├── app.py          ← FastAPI backend
├── rag_engine.py   ← RAG logic
├── ...
```

## Serving from FastAPI

To serve the frontend from your FastAPI backend, add this to `app.py`:

```python
from fastapi.staticfiles import StaticFiles

# Mount static files
app.mount("/", StaticFiles(directory=".", html=True), name="static")
```

This makes the frontend automatically available at `http://localhost:8000`.

---

Built with ❤️ for seamless RAG interactions.
