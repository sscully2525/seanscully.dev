"""
Memory Management
Handles conversation persistence and context retrieval.
"""

import json
import redis
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage


class ConversationMemory:
    """Redis-backed conversation memory."""
    
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis_client = redis.from_url(redis_url, decode_responses=True)
        self.ttl = 86400 * 7  # 7 days
    
    def _get_key(self, session_id: str) -> str:
        return f"conversation:{session_id}"
    
    def save_message(self, session_id: str, role: str, content: str, metadata: Dict = None):
        """Save a message to conversation history."""
        key = self._get_key(session_id)
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        
        self.redis_client.lpush(key, json.dumps(message))
        self.redis_client.expire(key, self.ttl)
    
    def get_history(self, session_id: str, limit: int = 20) -> List[Dict]:
        """Retrieve conversation history."""
        key = self._get_key(session_id)
        messages = self.redis_client.lrange(key, 0, limit - 1)
        return [json.loads(m) for m in messages][::-1]  # Reverse to chronological
    
    def clear_history(self, session_id: str):
        """Clear conversation history."""
        key = self._get_key(session_id)
        self.redis_client.delete(key)
    
    def get_context_summary(self, session_id: str) -> str:
        """Generate a summary of conversation context."""
        history = self.get_history(session_id, limit=10)
        if not history:
            return "No previous context"
        
        # Simple summarization - in production use LLM
        topics = set()
        for msg in history:
            if msg["role"] == "user":
                # Extract key terms (simplified)
                words = msg["content"].lower().split()[:5]
                topics.update(words)
        
        return f"Previous topics: {', '.join(list(topics)[:5])}"
