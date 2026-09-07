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
Add this file in the root of your project directory.

---

## 📄 File 2: `templates/index.html`
Create a folder named `templates` in your project root, and place the `index.html` file inside it.

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
