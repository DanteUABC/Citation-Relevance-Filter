from flask import Flask, render_template, request, jsonify, session
from langchain_ollama import ChatOllama
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import uuid

app = Flask(__name__)
# A secret key is required to use Flask sessions securely
app.secret_key = "super_secret_ollama_key" 

# Dictionary to store chat histories in memory based on the session ID
chat_histories = {}

def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    """Retrieves or creates a message history for a given session."""
    if session_id not in chat_histories:
        chat_histories[session_id] = InMemoryChatMessageHistory()
    return chat_histories[session_id]

@app.route('/')
def index():
    # Assign a unique session ID to the user if they don't have one
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

    # 1. Initialize the specific Ollama model requested by the user
    llm = ChatOllama(model=model_name)

    # 2. Set up the prompt template with a placeholder for the chat history
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful, concise AI assistant."),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}")
    ])

    # 3. Chain the prompt and the LLM
    chain = prompt | llm

    # 4. Wrap the chain with LangChain's history manager
    chain_with_history = RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="question",
        history_messages_key="history",
    )

    try:
        # 5. Invoke the chain. LangChain automatically fetches the history for the session ID
        # passes it to the prompt, gets the response, and saves the new exchange.
        response = chain_with_history.invoke(
            {"question": user_message},
            config={"configurable": {"session_id": session_id}}
        )
        return jsonify({"response": response.content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)