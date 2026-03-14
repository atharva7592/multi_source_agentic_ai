from sql_agent import get_sql_agent

agent = get_sql_agent()

while True:

    query = input("\nAsk database question: ")

    if query.lower() == "exit":
        break

    result = agent.invoke({"input": query})

    print("\nAnswer:")
    print(result["output"])