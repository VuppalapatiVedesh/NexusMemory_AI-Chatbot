"""
memory.py

This module manages the long-term conversation memory of the chatbot during a chat session.
To avoid Flask's browser cookie size limit (which is typically 4KB and would break 
long conversations), this implementation keeps conversation history in-memory on the server
and maps it to a unique session ID stored in the user's browser.
"""

class ConversationMemory:
    """
    Represents the conversation history for a single chat session.
    """
    def __init__(self):
        # List of message dictionaries, e.g., [{"role": "user", "content": "hello"}]
        self.messages = []

    def add_message(self, role: str, content: str):
        """
        Adds a message to the conversation history.
        
        Args:
            role (str): The role of the speaker, either 'user' or 'assistant'.
            content (str): The text content of the message.
        """
        self.messages.append({
            "role": role,
            "content": content
        })

    def get_messages(self) -> list:
        """
        Returns the complete conversation history.
        
        Returns:
            list: List of message dictionaries.
        """
        return self.messages

    def clear(self):
        """
        Resets and clears the conversation history.
        """
        self.messages = []


# Global dictionary storing active memories, keyed by session_id (string UUID)
# In production, this could be backed by Redis or a database, but for a college
# project, an in-memory dictionary is simple and perfectly suited.
_active_sessions = {}

def get_memory(session_id: str) -> ConversationMemory:
    """
    Retrieves the ConversationMemory object associated with the session ID.
    If the session doesn't exist, a new memory object is created.
    
    Args:
        session_id (str): The unique session ID for the user.
        
    Returns:
        ConversationMemory: The memory object for the session.
    """
    if session_id not in _active_sessions:
        _active_sessions[session_id] = ConversationMemory()
    return _active_sessions[session_id]

def clear_memory(session_id: str):
    """
    Clears the conversation memory for the given session ID.
    
    Args:
        session_id (str): The unique session ID.
    """
    if session_id in _active_sessions:
        _active_sessions[session_id].clear()

def add_message_to_session(session_id: str, role: str, content: str):
    """
    Helper function to directly append a message to a session's history.
    
    Args:
        session_id (str): The unique session ID.
        role (str): 'user' or 'assistant'.
        content (str): The message text.
    """
    memory = get_memory(session_id)
    memory.add_message(role, content)

def get_session_history(session_id: str) -> list:
    """
    Helper function to get the message history list for a session.
    
    Args:
        session_id (str): The unique session ID.
        
    Returns:
        list: The message list.
    """
    memory = get_memory(session_id)
    return memory.get_messages()
