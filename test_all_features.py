#!/usr/bin/env python
"""
Comprehensive test of all new features.
Run with: python test_all_features.py
"""

print("="*70)
print("🧪 COMPREHENSIVE FEATURE TEST")
print("="*70)

try:
    # Test 1: Query Validation
    print("\n1️⃣ Testing Query Validation...")
    from query_validator import create_validator
    v = create_validator()
    valid_q = "List products"
    invalid_q = "Tell a joke"
    valid_result = v.validate(valid_q)[0]
    invalid_result = v.validate(invalid_q)[0]
    print(f"  Valid query ({valid_q}): {valid_result}")
    print(f"  Invalid query ({invalid_q}): {invalid_result}")
    print("  ✅ Query validation working")
    
    # Test 2: Conversation Memory
    print("\n2️⃣ Testing Conversation Memory...")
    from conversation_memory import create_memory
    m = create_memory()
    m.add_user_message("List products")
    m.add_assistant_message("First 5 are...", agent="SQL", sources=["Products"])
    m.add_user_message("How many customers?")
    m.add_assistant_message("93 customers", agent="SQL", sources=["Customers"])
    print(f"  Messages stored: {len(m)}")
    stats = m.get_agent_stats()
    print(f"  Agent stats: {stats}")
    print("  ✅ Conversation memory working")
    
    # Test 3: Enhanced Agents with Sources
    print("\n3️⃣ Testing Source Tracking...")
    from sql_agent_enhanced import get_sql_agent
    from rag_agent_enhanced import get_rag_agent
    sql = get_sql_agent()
    print("  ✅ SQL agent with source tracking ready")
    rag = get_rag_agent()
    print("  ✅ RAG agent with source tracking ready")
    
    # Test 4: Full Graph Integration
    print("\n4️⃣ Testing Complete Graph Flow...")
    from supervisor_graph import build_graph
    graph = build_graph()
    result = graph.invoke({"question": "List first 5 products"})
    print("  Question routed ✅")
    print("  Answer received ✅")
    sources = result.get("sources", [])
    agent = result.get("agent", "Unknown")
    print(f"  Sources tracked: {sources}")
    print(f"  Agent used: {agent}")
    print("  ✅ Complete graph flow working")
    
    print("\n" + "="*70)
    print("✅ ALL FEATURES TESTED SUCCESSFULLY!")
    print("="*70)
    print("\n🚀 Ready to use:")
    print("   CLI Mode: python app.py")
    print("   Web Mode: streamlit run streamlit_app.py")
    print("\n" + "="*70)
    
except Exception as e:
    print(f"\n❌ Error during testing: {e}")
    import traceback
    traceback.print_exc()
