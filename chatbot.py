"""
chatbot.py

This module interfaces with the Groq API using the OpenAI Python SDK.
It retrieves the API key, initializes the API client, and implements the core
logic for generating context-aware and engaging responses.
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Retrieve the API key from environment variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Check if the API key is set
if not GROQ_API_KEY:
    # We do not crash the import, but we'll raise an error or warn the user.
    # The Flask routes can catch this and show a descriptive setup warning.
    print("WARNING: GROQ_API_KEY is not set in the environment variables or .env file.")

def get_groq_client() -> OpenAI:
    """
    Initializes and returns the OpenAI client configured for the Groq API.
    
    Returns:
        OpenAI: The configured client instance.
        
    Raises:
        ValueError: If GROQ_API_KEY is not set.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError(
            "Groq API Key is missing. Please create a '.env' file in the root "
            "directory and add: GROQ_API_KEY=your_actual_groq_key"
        )
    
    # Initialize the client pointing to Groq's OpenAI-compatible base URL
    return OpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1"
    )

def generate_chatbot_response(history_messages: list) -> str:
    """
    Sends the complete conversation history to the LLM (Groq) and generates a response.
    
    Args:
        history_messages (list): A list of previous message dictionaries.
        
    Returns:
        str: The AI assistant's response.
    """
    client = get_groq_client()
    
    # Define a high-quality system prompt to guide the AI's behavior
    system_prompt = (
        "You are an advanced, friendly, helpful, and highly intelligent AI Chatbot. "
        "Your goal is to maintain natural, human-like, and engaging conversations. "
        "You have access to the entire conversation history during this chat session. "
        "Always follow these instructions:\n"
        "1. Understand the user's intent and give accurate, context-aware answers.\n"
        "2. Avoid hallucinations. If you don't know the answer, politely state so.\n"
        "3. Remember previous topics, facts, and user preferences mentioned in the chat. "
        "Seamlessly connect new questions with previous context when relevant.\n"
        "4. Be concise and direct for simple questions, but provide structured, detailed "
        "explanations for complex topics. Use clean Markdown (such as bullet points, bold text, "
        "and code blocks) to make your output highly readable.\n"
        "5. Maintain a professional yet warm, friendly, and approachable tone.\n"
        "6. Avoid robotic repetitions and boilerplate text.\n"
        "7. Ask relevant follow-up questions when natural to keep the user engaged."
    )
    
    # Construct the final message list starting with the system prompt
    messages = [{"role": "system", "content": system_prompt}] + history_messages
    
    try:
        # Use llama-3.3-70b-versatile, which is fast, accurate, and has a large context window.
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.7,
            max_tokens=2048,
            top_p=1.0,
            stream=False
        )
        
        # Extract the assistant's response content
        return response.choices[0].message.content
        
    except Exception as e:
        # Print the error for backend debugging
        print(f"Error calling Groq API: {str(e)}")
        # Raise the error to be handled gracefully by the web server
        raise e
