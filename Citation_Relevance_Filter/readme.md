# Local AI Hub 🧠💬

A lightweight, dark-mode web application that lets you chat with your local LLMs. Built with Python Flask, LangChain, and Ollama, this app allows you to seamlessly switch between different AI models mid-conversation without losing your chat history context.

## ✨ Features
* **Multi-Model Support:** Switch between Gemma, Qwen, and Ministral on the fly.
* **Context Retention:** LangChain manages your session history, so if you switch models, the new AI remembers what the previous one said.
* **100% Local:** Private and secure. No data leaves your machine.
* **Clean UI:** A responsive, dark-mode interface built with raw HTML/CSS/JS.

---

## 📋 Prerequisites

Before you begin, ensure you have the following installed on your machine:
1. **[Python 3.8+](https://www.python.org/downloads/)**
2. **[Ollama](https://ollama.com/)** (Running in the background)

---

## 🚀 Installation & Setup

### 1. Download Local AI Models
Open your terminal or command prompt and pull the specific models this app uses via Ollama:

```bash
ollama pull gemma3:4b
ollama pull qwen3:4b
ollama pull ministral-3:3b
```

### 2. Set Up the Project
Create a project folder (e.g., `ollama-flask-chat`), and inside it, create the following two files: `app.py` and `templates/index.html`.

### 3. Create a Virtual Environment (Recommended)
**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install flask langchain langchain-ollama langchain-core
```

---

## 📄 File 1: `app.py`
Create this file in the root of your project directory:

```python
from flask import Flask, render_template, request, jsonify, session
from langchain_ollama import ChatOllama
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import uuid

app = Flask(__name__)
app.secret_key = "super_secret_ollama_key" 

chat_histories = {}

def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    # Retrieves or creates a message history for a given session.
    if session_id not in chat_histories:
        chat_histories[session_id] = InMemoryChatMessageHistory()
    return chat_histories[session_id]

@app.route('/')
def index():
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message')
    model_name = data.get('model', 'gemma3:4b')
    session_id = session.get('session_id')

    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    llm = ChatOllama(model=model_name)

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful, concise AI assistant."),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}")
    ])

    chain = prompt | llm

    chain_with_history = RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="question",
        history_messages_key="history",
    )

    try:
        response = chain_with_history.invoke(
            {"question": user_message},
            config={"configurable": {"session_id": session_id}}
        )
        return jsonify({"response": response.content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

---

## 📄 File 2: `templates/index.html`
Create a folder named `templates` in your project root, and place this `index.html` file inside it:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Local AI Hub</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background-color: #1e1e2e; color: #cdd6f4; margin: 0; display: flex; height: 100vh; }
        .sidebar { width: 250px; background-color: #181825; padding: 20px; border-right: 1px solid #313244; }
        .sidebar h2 { font-size: 1.2rem; margin-top: 0; }
        select { width: 100%; padding: 10px; background: #313244; color: white; border: none; border-radius: 5px; font-size: 1rem; margin-top: 10px; outline: none; }
        .chat-container { flex: 1; display: flex; flex-direction: column; padding: 20px; max-width: 800px; margin: 0 auto; }
        .chat-box { flex: 1; overflow-y: auto; display: flex; flex-direction: column; gap: 15px; padding-bottom: 20px; }
        .message { padding: 12px 16px; border-radius: 8px; max-width: 80%; line-height: 1.5; }
        .user-msg { background-color: #89b4fa; color: #11111b; align-self: flex-end; }
        .ai-msg { background-color: #313244; color: #cdd6f4; align-self: flex-start; }
        .input-area { display: flex; gap: 10px; margin-top: auto; }
        input[type="text"] { flex: 1; padding: 15px; border-radius: 8px; border: 1px solid #313244; background-color: #181825; color: white; font-size: 1rem; outline: none;}
        button { padding: 15px 25px; border: none; border-radius: 8px; background-color: #a6e3a1; color: #11111b; font-weight: bold; cursor: pointer; transition: 0.2s;}
        button:hover { background-color: #94e2d5; }
        .loading { display: none; align-self: flex-start; color: #a6adc8; font-style: italic; font-size: 0.9rem;}
    </style>
</head>
<body>

    <div class="sidebar">
        <h2>Model Selection</h2>
        <label for="model-select">Active AI:</label>
        <select id="model-select">
            <option value="gemma3:4b">Gemma 3 (4B)</option>
            <option value="qwen3:4b">Qwen 3 (4B)</option>
            <option value="ministral-3:3b">Ministral 3 (3B)</option>
        </select>
    </div>

    <div class="chat-container">
        <div class="chat-box" id="chat-box">
            <div class="message ai-msg">Hello! I'm ready. You can swap models anytime in the sidebar and I'll remember our chat.</div>
        </div>
        <div class="loading" id="loading-indicator">The AI is thinking...</div>
        
        <div class="input-area">
            <input type="text" id="user-input" placeholder="Type your prompt here..." onkeypress="handleEnter(event)">
            <button onclick="sendMessage()">Send</button>
        </div>
    </div>

    <script>
        const chatBox = document.getElementById('chat-box');
        const userInput = document.getElementById('user-input');
        const modelSelect = document.getElementById('model-select');
        const loadingIndicator = document.getElementById('loading-indicator');

        function handleEnter(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }

        async function sendMessage() {
            const message = userInput.value.trim();
            if (!message) return;

            addMessage(message, 'user-msg');
            userInput.value = '';
            loadingIndicator.style.display = 'block';

            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ 
                        message: message,
                        model: modelSelect.value
                    })
                });

                const data = await response.json();
                loadingIndicator.style.display = 'none';

                if (response.ok) {
                    addMessage(data.response, 'ai-msg');
                } else {
                    addMessage("Error: " + data.error, 'ai-msg');
                }
            } catch (error) {
                loadingIndicator.style.display = 'none';
                addMessage("Connection error. Is the Flask server running?", 'ai-msg');
            }
        }

        function addMessage(text, className) {
            const msgDiv = document.createElement('div');
            msgDiv.className = `message ${className}`;
            msgDiv.textContent = text;
            chatBox.appendChild(msgDiv);
            chatBox.scrollTop = chatBox.scrollHeight;
        }
    </script>
</body>
</html>
```

---

## 💻 Running the App

1. Ensure Ollama is actively running on your system.
2. Start the Flask server:
   ```bash
   python app.py
   ```
3. Open your favorite web browser and navigate to:
   **`http://127.0.0.1:5000`**

## 🛠️ Troubleshooting
* **"Connection refused" / "Ollama not found":** Make sure the Ollama application is open and running in your system tray or background before starting the Flask app.
* **Model not found error:** Ensure you ran the `ollama pull` commands completely before trying to chat with that specific model in the UI.
