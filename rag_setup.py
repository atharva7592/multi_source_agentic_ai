import os
from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

print("Loading documents...")

# Get data path - works on local and Streamlit Cloud
data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "company_docs")

loader = DirectoryLoader(
    data_path,
    glob="*.txt"
)

documents = loader.load()

print(f"Documents loaded: {len(documents)}")

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

chunks = splitter.split_documents(documents)

print(f"Chunks created: {len(chunks)}")

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

print("Creating vector database...")

# Get vectorstore path - works on local and Streamlit Cloud
vectorstore_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vectorstore")

vectordb = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory=vectorstore_path
)

print("Vector database created successfully!")