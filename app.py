"""
app.py

The main Flask application entry point. 
It defines the routes for rendering the web interface, sending chat messages, 
retrieving session-based chat history, and clearing the chat session memory.
"""

import os
import uuid
from flask import Flask, render_template, request, jsonify, session
from dotenv import load_dotenv

# Import our custom modules
import memory
import chatbot

# Load environment variables
load_dotenv()

# Initialize Flask application
app = Flask(__name__)

# Set the secret key for session management.
# Try to get it from environment variables first; default to a fallback for development.
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev_session_secret_key_99887766")

def get_or_create_session_id() -> str:
    """
    Checks if a session ID exists in the Flask session cookie.
    If not, generates a new unique UUID and stores it.
    
    Returns:
        str: The user's unique session ID.
    """
    if "session_id" not in session:
        session["session_id"] = uuid.uuid4().hex
    return session["session_id"]

@app.route("/")
def index():
    """
    Renders the main chatbot user interface.
    Generates a new session ID if one doesn't exist yet.
    """
    get_or_create_session_id()
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    """
    Accepts user messages, adds them to the conversation memory,
    calls the Groq chatbot API, saves the response, and returns JSON.
    """
    session_id = get_or_create_session_id()
    data = request.get_json() or {}
    
    user_message = data.get("message", "").strip()
    
    # Validation
    if not user_message:
        return jsonify({
            "status": "error",
            "message": "Message content cannot be empty."
        }), 400
        
    try:
        # 1. Add user message to session memory
        memory.add_message_to_session(session_id, "user", user_message)
        
        # 2. Get the full conversation history for this session
        history = memory.get_session_history(session_id)
        
        # 3. Call the Groq API to generate a response
        ai_response = chatbot.generate_chatbot_response(history)
        
        # 4. Add the assistant's response to session memory
        memory.add_message_to_session(session_id, "assistant", ai_response)
        
        # 5. Return success and the response text
        return jsonify({
            "status": "success",
            "response": ai_response
        })
        
    except ValueError as ve:
        # Handle configuration errors (e.g. missing API key)
        return jsonify({
            "status": "error",
            "message": str(ve),
            "type": "configuration_error"
        }), 500
        
    except Exception as e:
        # Handle general errors (API timeout, server issues, etc.)
        return jsonify({
            "status": "error",
            "message": f"An unexpected error occurred: {str(e)}",
            "type": "server_error"
        }), 500

@app.route("/history", methods=["GET"])
def get_history():
    """
    Retrieves the raw conversation history for the current session.
    Useful for debugging or loading chat history upon page reload.
    """
    session_id = get_or_create_session_id()
    history = memory.get_session_history(session_id)
    return jsonify({
        "status": "success",
        "history": history
    })

@app.route("/clear", methods=["POST"])
def clear_chat():
    """
    Clears the long-term memory stored for the user's session.
    """
    session_id = get_or_create_session_id()
    memory.clear_memory(session_id)
    return jsonify({
        "status": "success",
        "message": "Conversation history successfully cleared."
    })

if __name__ == "__main__":
    # In development, run local server on http://127.0.0.1:5000
    # Set debug=True for hot reloading and descriptive logs
    app.run(host="127.0.0.1", port=5000, debug=True)
