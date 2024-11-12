from typing import List
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.chat_history import BaseChatMessageHistory

class CustomChatMessageHistory(BaseChatMessageHistory):
    def __init__(self):
        self.messages = []
    
    def add_message(self, message):
        self.messages.append(message)
    
    def clear(self):
        self.messages = []
    
    def get_messages(self) -> List:
        return self.messages

class SessionManager:
    def __init__(self):
        self.sessions = {}
    
    def get_session(self, session_id: str) -> CustomChatMessageHistory:
        if session_id not in self.sessions:
            self.sessions[session_id] = CustomChatMessageHistory()
        return self.sessions[session_id]