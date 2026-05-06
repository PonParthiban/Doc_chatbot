/* ========================================
   RAG Chat UI - JavaScript Logic
   ======================================== */

// ========================================
// Configuration
// ========================================

const BASE_URL = 'http://localhost:8000';

// ========================================
// DOM Elements
// ========================================

const messagesContainer = document.getElementById('messagesContainer');
const questionInput = document.getElementById('questionInput');
const sendButton = document.getElementById('sendButton');
const loadingIndicator = document.getElementById('loadingIndicator');

// ========================================
// Event Listeners
// ========================================

/**
 * Initialize event listeners when DOM is ready
 */
document.addEventListener('DOMContentLoaded', function() {
    // Send on button click
    sendButton.addEventListener('click', sendMessage);

    // Send on Enter key (but not Shift+Enter)
    questionInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    // Focus input on load
    questionInput.focus();
});

// ========================================
// Main Functions
// ========================================

/**
 * Send a message to the RAG backend
 * Handles validation, API calls, and UI updates
 */
async function sendMessage() {
    const question = questionInput.value.trim();

    // Validate input
    if (!question) {
        return;
    }

    // Append user message to chat
    appendMessage('user', question);

    // Clear input and disable controls
    questionInput.value = '';
    setLoadingState(true);

    try {
        // Call RAG backend API
        const response = await queryRagBackend(question);

        // Append bot response with sources
        appendMessage('bot', response.answer, response.sources);
    } catch (error) {
        // Show error message
        console.error('Error:', error);
        appendErrorMessage(error.message);
    } finally {
        // Re-enable controls and focus input
        setLoadingState(false);
        questionInput.focus();
    }
}

/**
 * Query the RAG backend with a question
 * @param {string} question - The question to ask
 * @returns {Promise<Object>} - Response with answer and sources
 */
async function queryRagBackend(question) {
    const url = `${BASE_URL}/ask`;

    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            question: question,
        }),
    });

    if (!response.ok) {
        let errorMessage = 'Failed to get response from server';
        try {
            const errorData = await response.json();
            errorMessage = errorData.detail || errorMessage;
        } catch (e) {
            // If response is not JSON, use generic message
        }
        throw new Error(errorMessage);
    }

    const data = await response.json();
    return data;
}

/**
 * Append a message to the chat (user or bot)
 * Auto-scrolls to bottom
 * @param {string} sender - 'user' or 'bot'
 * @param {string} message - The message text
 * @param {Array} sources - Optional array of source objects {file, score}
 */
function appendMessage(sender, message, sources = null) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';

    // Create paragraph for message text
    const paragraph = document.createElement('p');
    paragraph.textContent = message;
    contentDiv.appendChild(paragraph);

    // Add sources if provided (for bot messages)
    if (sources && sources.length > 0) {
        const sourcesDiv = renderSources(sources);
        contentDiv.appendChild(sourcesDiv);
    }

    messageDiv.appendChild(contentDiv);
    messagesContainer.appendChild(messageDiv);

    // Auto-scroll to bottom
    scrollToBottom();
}

/**
 * Create and return sources HTML element
 * @param {Array} sources - Array of {file, score} objects
 * @returns {HTMLElement} - Sources container div
 */
function renderSources(sources) {
    const sourcesDiv = document.createElement('div');
    sourcesDiv.className = 'sources';

    // Sources label
    const label = document.createElement('div');
    label.className = 'sources-label';
    label.textContent = '📄 Sources';
    sourcesDiv.appendChild(label);

    // Source items
    sources.forEach(source => {
        const sourceItem = document.createElement('div');
        sourceItem.className = 'source-item';

        // Source icon and name
        const sourceInfo = document.createElement('div');
        sourceInfo.style.display = 'flex';
        sourceInfo.style.alignItems = 'center';
        sourceInfo.style.gap = '6px';
        sourceInfo.style.flex = '1';

        const icon = document.createElement('span');
        icon.className = 'source-icon';
        icon.textContent = '📎';

        const name = document.createElement('span');
        name.className = 'source-name';
        name.textContent = source.file;

        sourceInfo.appendChild(icon);
        sourceInfo.appendChild(name);

        // Score badge
        const score = document.createElement('span');
        score.className = 'source-score';
        score.textContent = `${(source.score * 100).toFixed(0)}%`;

        sourceItem.appendChild(sourceInfo);
        sourceItem.appendChild(score);

        sourcesDiv.appendChild(sourceItem);
    });

    return sourcesDiv;
}

/**
 * Append an error message to the chat
 * @param {string} errorText - The error message
 */
function appendErrorMessage(errorText) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot-message';

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';

    const paragraph = document.createElement('p');
    paragraph.style.color = '#dc2626';
    paragraph.style.fontWeight = '500';
    paragraph.textContent = '❌ Error: ' + errorText;

    contentDiv.appendChild(paragraph);
    messageDiv.appendChild(contentDiv);
    messagesContainer.appendChild(messageDiv);

    scrollToBottom();
}

/**
 * Set loading state - shows/hides spinner and disables controls
 * @param {boolean} isLoading - Whether we're loading
 */
function setLoadingState(isLoading) {
    if (isLoading) {
        // Show loading indicator
        loadingIndicator.style.display = 'flex';
        scrollToBottom();
    } else {
        // Hide loading indicator
        loadingIndicator.style.display = 'none';
    }

    // Disable/enable input controls
    questionInput.disabled = isLoading;
    sendButton.disabled = isLoading;
}

/**
 * Auto-scroll chat to the bottom
 * Smooth scroll for better UX
 */
function scrollToBottom() {
    // Use requestAnimationFrame for smooth scrolling
    requestAnimationFrame(() => {
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    });
}

// ========================================
// Utility Functions
// ========================================

/**
 * Format a timestamp (not used yet, but useful for future feature)
 * @param {Date} date - Date object
 * @returns {string} - Formatted time string
 */
function formatTime(date) {
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    return `${hours}:${minutes}`;
}
