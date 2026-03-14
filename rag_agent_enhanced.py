"""
Enhanced RAG agent that returns source information and documents.
"""
import os
from dotenv import load_dotenv
from typing import Dict, Any, List

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

load_dotenv()


class EnhancedRAGAgent:
    """RAG agent that tracks which documents were retrieved."""
    
    def __init__(self):
        print("Initializing Enhanced RAG agent...")
        
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        
        self.vectordb = Chroma(
            persist_directory="vectorstore",
            embedding_function=self.embeddings
        )
        
        self.retriever = self.vectordb.as_retriever(search_kwargs={"k": 3})
        
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0,
            api_key=os.getenv("GROQ_API_KEY")
        )
        
        self.prompt = ChatPromptTemplate.from_template(
            """You are a business intelligence assistant.

Use the following context to answer the user's question.

Context:
{context}

Question:
{question}
"""
        )
        
        self.parser = StrOutputParser()
        
        # Track last retrieved documents
        self.last_sources = []
        
        print("Enhanced RAG agent ready!")
    
    def retrieve_with_sources(self, question: str) -> tuple[str, List[str]]:
        """
        Retrieve documents and extract source information.
        
        Args:
            question: User question
            
        Returns:
            tuple: (context_text, sources_list)
        """
        docs = self.retriever.invoke(question)
        
        sources = []
        context_parts = []
        
        for i, doc in enumerate(docs, 1):
            # Extract source filename
            source = doc.metadata.get("source", "Unknown")
            if source not in sources:
                sources.append(source)
            
            # Build context with source reference
            context_parts.append(f"[Source {i}: {source}]\n{doc.page_content}")
        
        context = "\n\n".join(context_parts)
        self.last_sources = sources
        
        return context, sources
    
    def invoke(self, question: str) -> Dict[str, Any]:
        """
        Invoke the RAG agent and return results with sources.
        
        Args:
            question: User question
            
        Returns:
            {
                "output": answer,
                "sources": [document_names],
                "num_sources": count
            }
        """
        try:
            context, sources = self.retrieve_with_sources(question)
            
            chain = self.prompt | self.llm | self.parser
            
            answer = chain.invoke({
                "context": context,
                "question": question
            })
            
            return {
                "output": answer,
                "sources": sources,
                "num_sources": len(sources)
            }
        except Exception as e:
            print(f"[ERROR] RAG agent error: {e}")
            return {
                "output": f"Error processing query: {str(e)}",
                "sources": ["Error"],
                "num_sources": 0
            }


def get_rag_agent() -> EnhancedRAGAgent:
    """Factory function to create an enhanced RAG agent."""
    return EnhancedRAGAgent()


if __name__ == "__main__":
    agent = get_rag_agent()
    
    test_query = "What is the company policy?"
    result = agent.invoke(test_query)
    
    print(f"Query: {test_query}")
    print(f"Answer: {result['output'][:100]}...")
    print(f"Sources: {result['sources']}")
    print(f"Number of sources: {result['num_sources']}")
