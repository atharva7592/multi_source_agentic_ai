from langgraph.graph import StateGraph, END

from sql_agent_enhanced import get_sql_agent
from rag_agent_enhanced import get_rag_agent
from query_validator import create_validator
from conversation_memory import create_memory


# Initialize agents
sql_agent = get_sql_agent()
rag_agent = get_rag_agent()
query_validator = create_validator()

# Initialize conversation memory (optional, for maintaining context)
conversation_memory = None  # Will be created per session


# -------------------------
# Query Validation Node
# -------------------------
def validation_node(state):
    """Validates if the query is business-related"""
    
    question = state.get("question", "")
    
    print(f"[DEBUG] Validating query: {question[:50]}...")
    
    # Quick validation
    is_valid, reason = query_validator.validate(question)
    
    if not is_valid:
        print(f"[DEBUG] Query rejected: {reason}")
        state["is_valid"] = False
        state["validation_reason"] = reason
        return state
    
    print(f"[DEBUG] Query validated: {reason}")
    state["is_valid"] = True
    state["validation_reason"] = reason
    return state


# -------------------------
# Supervisor Router Node
# -------------------------
def supervisor_node(state):
    """Supervisor node that analyzes the query and routes it"""
    
    question = state.get("question", "").lower()
    
    # Define SQL-specific keywords
    sql_keywords = [
        "product", "products",
        "order", "orders",
        "employee", "employees",
        "customer", "customers",
        "supplier", "suppliers",
        "list", "count", "how many",
        "total", "sum", "average", "max", "min"
    ]
    
    print(f"[DEBUG] Supervisor analyzing: {question[:50]}...")
    
    # Determine routing
    if any(word in question for word in sql_keywords):
        next_agent = "sql"
        print("[DEBUG] Route decision: SQL agent")
    else:
        next_agent = "rag"
        print("[DEBUG] Route decision: RAG agent")
    
    # Add routing decision to state
    state["next_agent"] = next_agent
    return state


# -------------------------
# Routing Functions
# -------------------------
def route_to_agent(state):
    """Extract routing decision from state"""
    is_valid = state.get("is_valid", True)
    
    if not is_valid:
        return "invalid"
    
    return state.get("next_agent", "rag")


def route_after_sql(state):
    """Route after SQL processing"""
    return END


def route_after_rag(state):
    """Route after RAG processing"""
    return END


# -------------------------
# Invalid Query Node
# -------------------------
def invalid_query_node(state):
    """Handle invalid queries"""
    
    reason = state.get("validation_reason", "Query is not business-related")
    
    state["answer"] = f"I can only answer business-related questions. {reason}"
    state["sources"] = []
    state["agent"] = "Query Validator"
    
    return state


# -------------------------
# SQL Node
# -------------------------
def sql_node(state):
    """SQL agent node for database queries"""
    
    question = state.get("question", "")
    
    print(f"[DEBUG] SQL node processing: {question[:50]}...")
    
    try:
        result = sql_agent.invoke({"input": question})
        answer = result.get("output", "No result from SQL agent")
        sources = result.get("sources", [])
        
        # Format sources for display
        sources_str = ", ".join(sources) if sources else "Database"
        
        state["answer"] = answer
        state["sources"] = sources
        state["sources_str"] = sources_str
        state["agent"] = "SQL"
        
    except Exception as e:
        print(f"[ERROR] SQL agent error: {e}")
        state["answer"] = f"Error: {str(e)}"
        state["sources"] = ["Error"]
        state["agent"] = "SQL"
    
    return state


# -------------------------
# RAG Node
# -------------------------
def rag_node(state):
    """RAG agent node for document-based queries"""
    
    question = state.get("question", "")
    
    print(f"[DEBUG] RAG node processing: {question[:50]}...")
    
    try:
        result = rag_agent.invoke(question)
        answer = result.get("output", "No result from RAG agent")
        sources = result.get("sources", [])
        
        # Format sources for display
        sources_str = ", ".join(sources) if sources else "Documents"
        
        state["answer"] = answer
        state["sources"] = sources
        state["sources_str"] = sources_str
        state["agent"] = "RAG"
        
    except Exception as e:
        print(f"[ERROR] RAG agent error: {e}")
        state["answer"] = f"Error: {str(e)}"
        state["sources"] = ["Error"]
        state["agent"] = "RAG"
    
    return state


# -------------------------
# Build Graph
# -------------------------
def build_graph():
    """Build the supervisor graph for agent orchestration with validation"""
    
    graph = StateGraph(dict)
    
    # Add nodes
    graph.add_node("validator", validation_node)
    graph.add_node("supervisor", supervisor_node)
    graph.add_node("sql", sql_node)
    graph.add_node("rag", rag_node)
    graph.add_node("invalid", invalid_query_node)
    
    # Set entry point to validator
    graph.set_entry_point("validator")
    
    # Routes: validator -> supervisor or invalid
    graph.add_conditional_edges(
        "validator",
        lambda state: "invalid" if not state.get("is_valid", True) else "supervisor",
        {
            "invalid": "invalid",
            "supervisor": "supervisor"
        }
    )
    
    # Routes: supervisor -> sql or rag
    graph.add_conditional_edges(
        "supervisor",
        route_to_agent,
        {
            "sql": "sql",
            "rag": "rag"
        }
    )
    
    # Final edges to END
    graph.add_edge("invalid", END)
    graph.add_edge("sql", END)
    graph.add_edge("rag", END)
    
    print("[DEBUG] Graph built successfully with validation and source tracking")
    
    return graph.compile()


# -------------------------
# Utility Functions
# -------------------------
def format_answer_with_sources(answer: str, sources: list, agent: str) -> str:
    """Format answer with source citations"""
    
    formatted = f"{answer}\n\n"
    formatted += f"📊 **Agent Used:** {agent}\n"
    
    if sources and sources[0] != "Error":
        formatted += f"📎 **Sources:** {', '.join(sources)}\n"
    
    return formatted