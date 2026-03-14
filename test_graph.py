#!/usr/bin/env python
"""Quick test of the supervisor graph"""

from supervisor_graph import build_graph

# Build the graph
graph = build_graph()

# Test query
test_queries = [
    "List the first 5 products",
    "What is the company policy?",
    "How many customers do we have?",
]

for query in test_queries:
    print(f"\n{'='*60}")
    print(f"Query: {query}")
    print('='*60)
    
    try:
        result = graph.invoke({"question": query})
        print(f"\n✓ Answer:\n{result.get('answer', 'No answer')}")
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
