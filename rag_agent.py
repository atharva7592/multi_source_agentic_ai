import os
from dotenv import load_dotenv

# explicitly load .env
load_dotenv(".env")

print("Groq Key Loaded:", os.getenv("GROQ_API_KEY"))

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


load_dotenv()


def get_rag_agent():

    print("Initializing RAG agent...")

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectordb = Chroma(
        persist_directory="vectorstore",
        embedding_function=embeddings
    )

    retriever = vectordb.as_retriever(search_kwargs={"k": 3})

    import os

    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0,
        api_key=os.getenv("GROQ_API_KEY")
)

    prompt = ChatPromptTemplate.from_template(
        """
You are a business intelligence assistant.

Use the following context to answer the user's question.

Context:
{context}

Question:
{question}
"""
    )

    parser = StrOutputParser()

    def rag_pipeline(question):

        docs = retriever.invoke(question)

        context = "\n\n".join([doc.page_content for doc in docs])

        chain = prompt | llm | parser

        answer = chain.invoke({
            "context": context,
            "question": question
        })

        return answer

    print("RAG agent ready!")

    return rag_pipeline