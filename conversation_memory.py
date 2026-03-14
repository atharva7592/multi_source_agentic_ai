"""
Conversation memory system for maintaining context across interactions.
"""
from typing import List, Dict, Any
from datetime import datetime


class ConversationMemory:
    """Manages conversation history and context."""
    
    def __init__(self, max_history: int = 50):
        self.messages: List[Dict[str, Any]] = []
        self.max_history = max_history
    
    def add_message(self, role: str, content: str, agent: str = None, sources: List[str] = None):
        """
        Add a message to conversation history.
        
        Args:
            role: "user" or "assistant"
            content: Message content
            agent: Which agent processed it (SQL/RAG/None)
            sources: List of sources used
        """
        message = {
            "timestamp": datetime.now().isoformat(),
            "role": role,
            "content": content,
            "agent": agent,
            "sources": sources or []
        }
        
        self.messages.append(message)
        
        # Keep history within limit
        if len(self.messages) > self.max_history:
            self.messages = self.messages[-self.max_history:]
    
    def add_user_message(self, query: str):
        """Add a user query to history."""
        self.add_message("user", query)
    
    def add_assistant_message(self, answer: str, agent: str = None, sources: List[str] = None):
        """Add an assistant response to history."""
        self.add_message("assistant", answer, agent=agent, sources=sources)
    
    def get_context(self, num_messages: int = 5) -> str:
        """
        Get conversation context for the LLM.
        
        Returns:
            Formatted conversation history
        """
        recent = self.messages[-num_messages:]
        
        context = "Recent Conversation History:\n"
        for msg in recent:
            role = msg["role"].upper()
            content = msg["content"]
            agent = f" [{msg['agent']}]" if msg["agent"] else ""
            context += f"{role}{agent}: {content[:100]}...\n" if len(content) > 100 else f"{role}{agent}: {content}\n"
        
        return context
    
    def get_summary(self) -> str:
        """Get a text summary of the conversation."""
        if not self.messages:
            return "No conversation history yet."
        
        summary = f"Conversation with {len(self.messages)} messages:\n\n"
        
        for i, msg in enumerate(self.messages, 1):
            role = "User" if msg["role"] == "user" else "Assistant"
            content = msg["content"][:80]
            agent = f" via {msg['agent']}" if msg["agent"] else ""
            summary += f"{i}. {role}{agent}: {content}...\n"
        
        return summary
    
    def get_messages_formatted(self) -> List[Dict[str, str]]:
        """Get messages in chat format."""
        return [
            {
                "role": msg["role"],
                "content": msg["content"]
            }
            for msg in self.messages
        ]
    
    def clear(self):
        """Clear conversation history."""
        self.messages = []
    
    def get_last_user_query(self) -> str:
        """Get the last user question."""
        for msg in reversed(self.messages):
            if msg["role"] == "user":
                return msg["content"]
        return ""
    
    def get_agent_stats(self) -> Dict[str, int]:
        """Get statistics about which agents were used."""
        stats = {"SQL": 0, "RAG": 0, "No Agent": 0}
        
        for msg in self.messages:
            if msg["role"] == "assistant":
                agent = msg["agent"] or "No Agent"
                if agent in stats:
                    stats[agent] += 1
        
        return stats
    
    def __len__(self) -> int:
        """Get number of messages in history."""
        return len(self.messages)
    
    def __repr__(self) -> str:
        """Return string representation."""
        return f"ConversationMemory({len(self.messages)} messages)"


def create_memory(max_history: int = 50) -> ConversationMemory:
    """Factory function to create conversation memory."""
    return ConversationMemory(max_history=max_history)


if __name__ == "__main__":
    # Test the conversation memory
    memory = ConversationMemory()
    
    # Simulate a conversation
    memory.add_user_message("List the first 5 products")
    memory.add_assistant_message(
        "The first 5 products are: Chai, Chang, Aniseed Syrup, Chef Anton's Cajun Seasoning, Chef Anton's Gumbo Mix",
        agent="SQL",
        sources=["Products table"]
    )
    
    memory.add_user_message("How many of them are in stock?")
    memory.add_assistant_message(
        "I need to query the database for stock information",
        agent="SQL",
        sources=["Products table - UnitsInStock column"]
    )
    
    # Display summary
    print(memory.get_summary())
    print("\nAgent Statistics:", memory.get_agent_stats())
