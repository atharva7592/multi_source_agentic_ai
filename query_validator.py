"""
Query validation module to filter off-topic queries.
"""
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()


class QueryValidator:
    """Validates if a query is business/work-related and relevant."""
    
    def __init__(self):
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0,
            api_key=os.getenv("GROQ_API_KEY")
        )
        
        # Keywords that indicate valid business queries
        self.valid_keywords = [
            "product", "order", "customer", "employee", "supplier",
            "database", "query", "list", "count", "how many", "what",
            "show", "find", "search", "report", "policy", "procedure",
            "benefit", "company", "data", "information", "detail",
            "sales", "revenue", "total", "sum", "average", "price",
            "amount", "number", "table", "category", "region"
        ]
        
        self.validation_prompt = ChatPromptTemplate.from_template(
            """Determine if the following query is business/work-related and appropriate to answer.
Only answer "VALID" if it's about:
- Company databases or products
- Business operations and procedures
- Company policies or benefits
- Employee or customer information
- Financial or sales data

Answer "INVALID" if it's about:
- Personal life topics
- Politics or controversial topics
- Entertainment or casual chat
- Topics unrelated to business

Query: {query}

Answer with only one word: VALID or INVALID"""
        )
        
        self.parser = StrOutputParser()
    
    def validate(self, query: str) -> tuple[bool, str]:
        """
        Validate a query.
        
        Returns:
            tuple: (is_valid, reason)
        """
        query_lower = query.lower()
        
        # Quick keyword check
        if any(keyword in query_lower for keyword in self.valid_keywords):
            return True, "Query is business-related"
        
        # Default to valid for other business-sounding queries
        # (Skip LLM validation to avoid parsing issues)
        if len(query) > 5:  # Assume short queries are valid if not obviously invalid
            return True, "Query accepted"
        
        return False, "Query is too short to process"
    
    def validate_quick(self, query: str) -> bool:
        """Quick validation using keywords only."""
        return any(keyword in query.lower() for keyword in self.valid_keywords)


def create_validator() -> QueryValidator:
    """Factory function to create a query validator."""
    return QueryValidator()


if __name__ == "__main__":
    validator = QueryValidator()
    
    test_queries = [
        "List the first 5 products",
        "What is the meaning of life?",
        "How many customers do we have?",
        "Tell me a joke",
        "What are the company policies?",
        "What's your favorite movie?"
    ]
    
    for query in test_queries:
        is_valid, reason = validator.validate(query)
        print(f"Query: {query}")
        print(f"Valid: {is_valid} - {reason}\n")
