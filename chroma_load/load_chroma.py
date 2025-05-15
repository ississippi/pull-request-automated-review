import os
import shutil
import chromadb
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# Settings
URL = "https://google.github.io/styleguide/pyguide.html"  # Replace with your desired webpage
persist_directory = "./chroma_langchain_store"

# Clean up previous store (optional)
# if os.path.exists(persist_directory) and not os.environ.get("DOCKER_VOLUME_MOUNTED"):
#     print(f"Removing existing vector store at: {persist_directory}")
#     shutil.rmtree(persist_directory)

# Step 1: Load webpage
print(f"Loading webpage: {URL}")
loader = WebBaseLoader(URL)
documents = loader.load()
print(f"Loaded {len(documents)} document(s)")

# Step 2: Split documents
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = splitter.split_documents(documents)
print(f"Split into {len(docs)} chunks")

# Step 3: Embed using HuggingFace
embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Step 4: Create Chroma client and collection
client = chromadb.PersistentClient(path=persist_directory)

# collection = client.get_collection(name="chroma_docs")
# results = collection.get(ids=["page"])["documents"]
# print(results) # Not found []

# Step 5: Create and persist Chroma store
print("Creating vector store...")
vectordb = Chroma(
    client=client,
    collection_name="web_docs",
    embedding_function=embedding,
    persist_directory=persist_directory
)

# vectordb.add_documents(docs)
# vectordb.persist()
print(f"Vector store files: {os.listdir(persist_directory)}")
print(f"✅ Vector store created and persisted to: {persist_directory}")
