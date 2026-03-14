# Multi-Source Agentic AI System

A sophisticated multi-agent Q&A system that integrates SQL database queries and document retrieval using RAG (Retrieval-Augmented Generation). Built with LangChain, LangGraph, and Groq's high-speed LLM inference.

**🚀 [Live Demo on Streamlit Cloud](https://share.streamlit.io/YOUR_GITHUB_USERNAME/multi_source_agentic_ai/main/streamlit_app.py)** *(Update after deployment)*

## Features

✅ **Intelligent Query Routing** - Automatically routes questions to SQL database or document retrieval  
✅ **Query Validation** - Filters off-topic queries before processing  
✅ **Conversation Memory** - Maintains chat history with statistics and context  
✅ **Source Citations** - Shows exactly which tables/documents were used for answers  
✅ **Dual Interfaces** - CLI and beautiful Streamlit web UI  
✅ **Production-Ready** - Tested end-to-end with comprehensive test suite  

## System Architecture

```
User Query
    ↓
Query Validator (checks business relevance)
    ↓
Supervisor Agent (routes to specialized agent)
    ├→ SQL Agent (Northwind database with 13 tables)
    ├→ RAG Agent (Document retrieval with ChromaDB)
    └→ Invalid Query Handler
    ↓
Conversation Memory (stores history + statistics)
    ↓
Response with Citations
```

## Quick Start

### Prerequisites
- Python 3.10+
- Groq API key ([Get one free](https://console.groq.com))
- HuggingFace API token (optional, for embeddings)

### 1. Clone Repository

```bash
cd multi_source_agentic_ai
```

### 2. Create Virtual Environment

```bash
python -m venv venv
.\venv\Scripts\activate  # On Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
# API Keys
GROQ_API_KEY=your_groq_api_key_here
HF_TOKEN=your_huggingface_token_here  # Optional: for higher HF rate limits

# LLM Configuration
LLM_MODEL=llama-3.3-70b-versatile
TEMPERATURE=0

# Vector Store Configuration
VECTOR_STORE_TYPE=chroma
VECTOR_STORE_PATH=./vectorstore
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# Database Configuration
DATABASE_URL=sqlite:///database/northwind.db

# RAG Configuration
RAG_CHUNK_SIZE=1000
RAG_CHUNK_OVERLAP=200
RAG_TOP_K=3

# Logging
LOG_LEVEL=INFO
LOG_FILE=./logs/app.log
```

### 5. Get Your Groq API Key

1. Visit [Groq Console](https://console.groq.com)
2. Create an account and get your API key
3. Add it to the `.env` file

### 6. Prepare the Database

The Northwind SQLite database should be placed at `database/northwind.db`. The system will create this directory if it doesn't exist.

### 7. Generate Sample Documents (Optional)

To generate sample company documents for the RAG system:

```bash
python generate_docs.py
```

## 🎮 Usage

### Interactive Mode

Run the interactive Q&A assistant:

```bash
python app.py
```

Then ask questions like:

```
Ask a question: List the first 5 products
Ask a question: How many customers do we have?
Ask a question: What are the company policies?
Ask a question: exit
```

### Test the System

Run the test script to verify both SQL and RAG agents:

```bash
python test_graph.py
```

## 🔄 How It Works

### Query Routing Logic

The Supervisor Agent uses keyword matching to route queries:

**Routes to SQL Agent if query contains:**
- `product`, `order`, `employee`, `customer`, `supplier`
- `list`, `count`, `how many`, `total`, `sum`, `average`

**Routes to RAG Agent for:**
- Document-based questions
- Questions about company policies
- General knowledge questions

### SQL Agent Flow

1. Analyzes user query
2. Inspects database schema
3. Generates SQL query
4. Executes query
5. Returns results in natural language

Example:
```
Query: "List the first 5 products"
↓
SQL: SELECT ProductID, ProductName FROM Products LIMIT 5
↓
Answer: "The first 5 products are: 1. Chai 2. Chang 3. Aniseed Syrup..."
```

### RAG Agent Flow

1. Retrieves relevant documents from vector store
2. Extracts context from documents
3. Generates answer using LLM
4. Returns answer with source documents

## 🛠️ Customization

### Adding More SQL Keywords

Edit the `supervisor_node` function in `supervisor_graph.py`:

```python
sql_keywords = [
    "your_keyword_1",
    "your_keyword_2",
    # ...
]
```

### Changing the LLM Model

Update the `.env` file:

```env
LLM_MODEL=your_model_name
```

### Adjusting RAG Settings

Modify `config.py` or `.env`:

```env
RAG_CHUNK_SIZE=1500        # Document chunk size
RAG_CHUNK_OVERLAP=300      # Chunk overlap
RAG_TOP_K=5                # Number of documents to retrieve
```

## 📊 Available Database Tables (Northwind)

- `Products` - Product information
- `Customers` - Customer data
- `Orders` - Order details
- `Employees` - Employee information
- `Categories` - Product categories
- `Suppliers` - Supplier information
- `Regions`, `Territories`, `Shippers` - Lookup tables

## 🐛 Troubleshooting

### Issue: "Groq Key not loaded"
- **Solution**: Ensure `GROQ_API_KEY` is set in `.env` file

### Issue: "Vector store not found"
- **Solution**: Run `python generate_docs.py` to create sample documents

### Issue: "Database connection failed"
- **Solution**: Verify `database/northwind.db` exists and the database URL in `.env` is correct

### Issue: "Warning: Unauthenticated requests to HF Hub"
- **Solution**: Set `HF_TOKEN` in `.env` for higher rate limits (optional but recommended)

## 📈 Performance Tips

1. **Increase RAG_TOP_K** if you want more document context (uses more tokens)
2. **Decrease TEMPERATURE** for more consistent, deterministic answers
3. **Use smaller embedding models** for faster responses (trade-off with accuracy)
4. **Cache vector store** - it's persistent, so queries run faster after first use

## 🔒 Security Considerations

- Never commit `.env` file with real API keys
- Use separate keys for development and production
- Consider rate limiting for production deployments
- Validate user inputs for SQL injection prevention

## 📝 License

[Your License Here]

## 🤝 Contributing

[Your Contributing Guidelines Here]

## 📞 Support

For issues and questions, please refer to the documentation above or check the debug output by setting `LOG_LEVEL=DEBUG` in `.env`.

---

**System Status Check:**

To verify everything is working:

```bash
python test_graph.py
```

This will test:
- ✅ Graph initialization
- ✅ SQL agent functionality
- ✅ RAG agent functionality
- ✅ Supervisor routing logic
