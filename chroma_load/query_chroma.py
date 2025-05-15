from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from chromadb.config import Settings
from chromadb import Client

# Reuse the same persist directory and collection name
persist_directory = "./chroma_langchain_store"
collection_name = "web_docs"

# Reinitialize the embedding model
embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Reload the Chroma client and vector store
client_settings = Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory=persist_directory,
    anonymized_telemetry=False
)
client = Client(client_settings)

# Reconnect to the collection
vectordb = Chroma(
    client=client,
    collection_name=collection_name,
    embedding_function=embedding,
    persist_directory=persist_directory
)

# Perform a similarity search
query = "What are Python naming conventions?"
results = vectordb.similarity_search(query, k=3)

print(f"Top results for query: '{query}'\n")
for i, doc in enumerate(results, 1):
    print(f"Result {i}:{doc.page_content}{'-'*60}")
