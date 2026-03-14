import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits.sql.base import create_sql_agent

load_dotenv()

def get_sql_agent():

    print("Initializing SQL agent...")

    db = SQLDatabase.from_uri(
        "sqlite:///database/northwind.db",
        sample_rows_in_table_info=2
    )

    print("Connected tables:", db.get_usable_table_names())

    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0,
        api_key=os.getenv("GROQ_API_KEY")
    )

    agent = create_sql_agent(
        llm=llm,
        db=db,
        verbose=True
    )

    print("SQL agent ready!")

    return agent