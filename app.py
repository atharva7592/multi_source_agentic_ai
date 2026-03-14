from supervisor_graph import build_graph, format_answer_with_sources
from conversation_memory import create_memory

# Build graph
graph = build_graph()

# Create conversation memory
memory = create_memory(max_history=50)

print("\n" + "="*70)
print("🤖 Multi-Source Agentic Q&A Assistant")
print("="*70)
print("\nCommands:")
print("  • 'history' - Show conversation history")
print("  • 'stats'   - Show agent usage statistics")
print("  • 'clear'   - Clear conversation history")
print("  • 'exit'    - Exit the program")
print("\n" + "="*70 + "\n")

while True:
    
    try:
        question = input("\n🔍 Ask a question: ").strip()
        
        if not question:
            continue
        
        # Handle special commands
        if question.lower() == "exit":
            print("\n👋 Thank you for using the assistant. Goodbye!")
            break
        
        elif question.lower() == "history":
            print("\n" + "="*70)
            print("📜 Conversation History")
            print("="*70)
            print(memory.get_summary())
            continue
        
        elif question.lower() == "stats":
            print("\n" + "="*70)
            print("📊 Agent Usage Statistics")
            print("="*70)
            stats = memory.get_agent_stats()
            for agent, count in stats.items():
                print(f"  {agent}: {count} queries")
            print(f"  Total Messages: {len(memory)}")
            print("="*70)
            continue
        
        elif question.lower() == "clear":
            memory.clear()
            print("✅ Conversation history cleared")
            continue
        
        # Add user question to memory
        memory.add_user_message(question)
        
        # Process the question
        result = graph.invoke({"question": question})
        
        answer = result.get("answer", "No answer")
        sources = result.get("sources", [])
        agent = result.get("agent", "Unknown")
        
        # Add to memory
        memory.add_assistant_message(answer, agent=agent, sources=sources)
        
        # Format and display answer
        print("\n" + "="*70)
        print("✨ Answer:")
        print("="*70)
        print(answer)
        
        # Show sources
        if sources and sources[0] != "Error":
            print("\n" + "-"*70)
            print(f"📎 Sources Used ({agent}):")
            for i, source in enumerate(sources, 1):
                print(f"   {i}. {source}")
        
        print("="*70)
        
    except KeyboardInterrupt:
        print("\n\n👋 Session interrupted. Goodbye!")
        break
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()