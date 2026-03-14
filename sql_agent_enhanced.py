"""
Enhanced SQL agent that returns source information.
"""
import os
from dotenv import load_dotenv
from typing import Dict, Any

from langchain_groq import ChatGroq
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits.sql.base import create_sql_agent

load_dotenv()


class EnhancedSQLAgent:
    """SQL agent that tracks which tables were queried."""
    
    def __init__(self):
        print("Initializing Enhanced SQL agent...")
        
        self.db = SQLDatabase.from_uri(
            "sqlite:///database/northwind.db",
            sample_rows_in_table_info=2
        )
        
        print("Connected tables:", self.db.get_usable_table_names())
        
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0,
            api_key=os.getenv("GROQ_API_KEY")
        )
        
        self.agent = create_sql_agent(
            llm=self.llm,
            db=self.db,
            verbose=False  # Set to False to reduce output
        )
        
        # Track tables used in queries
        self.last_tables_used = []
        self.all_available_tables = self.db.get_usable_table_names()
        
        print("Enhanced SQL agent ready!")
    
    def extract_tables_from_answer(self, answer: str) -> list:
        """
        Extract table names mentioned in the agent's reasoning.
        
        Args:
            answer: The agent's answer/reasoning
            
        Returns:
            List of table names that were used
        """
        tables_used = []
        answer_lower = answer.lower()
        
        for table in self.all_available_tables:
            if table.lower() in answer_lower:
                if table not in tables_used:
                    tables_used.append(table)
        
        return tables_used
    
    def invoke(self, input_dict: Dict[str, str]) -> Dict[str, Any]:
        """
        Invoke the SQL agent and return results with sources.
        
        Args:
            input_dict: {"input": query}
            
        Returns:
            {"output": answer, "sources": [tables_used]}
        """
        try:
            result = self.agent.invoke(input_dict)
            
            # Extract the final answer
            answer = result.get("output", "")
            
            # Try to extract tables from the answer
            # Common patterns: "from" keyword followed by table names
            tables_used = []
            answer_lower = answer.lower()
            
            # Check for explicit table mentions
            for table in self.all_available_tables:
                if f' {table.lower()} ' in f' {answer_lower} ' or f'"{table.lower()}"' in answer_lower:
                    if table not in tables_used:
                        tables_used.append(table)
            
            # If no tables found explicitly, infer from query context
            if not tables_used:
                query = input_dict.get("input", "").lower()
                for table in self.all_available_tables:
                    if table.lower() in query:
                        tables_used.append(table)
            
            self.last_tables_used = tables_used
            
            return {
                "output": answer,
                "sources": tables_used if tables_used else ["Database Query"]
            }
        except Exception as e:
            print(f"[ERROR] SQL agent error: {e}")
            return {
                "output": f"Error processing query: {str(e)}",
                "sources": ["Error"]
            }


def get_sql_agent() -> EnhancedSQLAgent:
    """Factory function to create an enhanced SQL agent."""
    return EnhancedSQLAgent()


if __name__ == "__main__":
    agent = get_sql_agent()
    
    # Test queries
    test_queries = [
        "List the first 5 products",
        "How many customers do we have?",
        "Show me the employees"
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        result = agent.invoke({"input": query})
        print(f"Answer: {result['output'][:100]}...")
        print(f"Sources: {result['sources']}")
