from rag_agent import get_rag_agent

rag = get_rag_agent()

while True:

    query = input("\nAsk a question: ")

    if query.lower() == "exit":
        break

    answer = rag(query)

    print("\nAnswer:")
    print(answer)