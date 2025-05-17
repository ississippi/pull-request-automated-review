import os
import shutil
import chromadb
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# Style Guides
style_guides = {
        "python": "https://google.github.io/styleguide/pyguide.html",
        "javascript": "https://google.github.io/styleguide/jsguide.html",
        "angularjs": "https://google.github.io/styleguide/angularjs-google-style.html",
        "java": "https://google.github.io/styleguide/jsguide.html",
        "csharp": "https://google.github.io/styleguide/csharpguide.html",
        "html": "https://google.github.io/styleguide/htmlcssguide.html",
        "css": "https://google.github.io/styleguide/htmlcssguide.html",
        "cpp": "https://google.github.io/styleguide/cppguide.html",
        "go": "https://google.github.io/styleguide/goforjs.html",
        "typescript": "https://google.github.io/styleguide/jsguide.html"
}
persist_directory = "../chroma_server/chroma_style_guide_store"

# Clean up previous store (optional)
if os.path.exists(persist_directory) and not os.environ.get("DOCKER_VOLUME_MOUNTED"):
    print(f"Removing existing vector store at: {persist_directory}")
    shutil.rmtree(persist_directory)

# Step 1: Load webpage
chroma_client = chromadb.PersistentClient(path=persist_directory)
for guide in style_guides:
    URL = style_guides[guide]
    print(f"Loading {guide} style guide from: {URL}")
    loader = WebBaseLoader(URL)
    documents = loader.load()
    print(f"Loaded {len(documents)} document(s)")

    # Step 2: Split documents
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = splitter.split_documents(documents)
    print(f"Split into {len(docs)} chunks")

    # Step 3: Embed using HuggingFace
    embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # Step 4: Create and persist Chroma store
    collection_name = f"{guide}_style_guide"
    print("Creating vector store...")
    vectordb = Chroma(
        client=chroma_client,
        collection_name=collection_name,
        embedding_function=embedding,
        persist_directory=persist_directory
    )
    vectordb.add_documents(docs)
    print("Document count:", vectordb._collection.count())
    print(f"✅ Vector store persisted to: {persist_directory} for collection: {collection_name}.")

if __name__ == "__main__":
    # Uncomment the following line to see the full response
    # response = get_collection()
    # body = response.get("body")
    # documents = json.loads(body).get("documents", [])
    # for doc in documents:
    #     print("Document:", doc)
    pass
