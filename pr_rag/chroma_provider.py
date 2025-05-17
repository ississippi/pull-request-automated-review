import os
import json
import sys
sys.path.append("../utils")
import helpers
from chromadb import HttpClient
from chromadb import PersistentClient

LANGUAGE_MAP = {
    ".py": "python", 
    ".js": "javascript",
    ".ts": "typescript",
    ".java": "java",
    ".cs": "csharp",
    ".html": "html",
    ".css": "css",
    ".cpp": "cpp",
    ".go": "go"
}

def get_collection(file_extension):
    client = HttpClient(host="https://notifications.codeominous.com/api/v1")

    language = LANGUAGE_MAP.get(file_extension)
    collection_name = f"{language}_style_guide"
    # Adjust collection name if needed
    collection = client.get_collection(collection_name)
    print("Total documents in collection:", collection.count())

    results = collection.query(query_texts=["What are the naming standards"], n_results=3)

    return {
        "statusCode": 200,
        "body": json.dumps(results)
    }

def test_collections_query():
    # client = HttpClient(host="https://notifications.codeominous.com/api/v1")
    # print(client.list_collections())
    client = PersistentClient(path="../chroma_server/chroma_style_guide_store")
    collections = client.list_collections()
    for col in collections:
        results = col.query(query_texts=[f"What are the {col.name} naming standards"], n_results=3)
        # json_structure = helpers.get_json_structure(results)
        helpers.write_json_to_file(results, f"query_results_{col.name}.json")

    return {
        "statusCode": 200,
        "body": collections
    }

def print_collection_contents():
    client = PersistentClient(path="../chroma_server/chroma_style_guide_store")
    collections = client.list_collections()
    for col in collections:
        print(f"{col.name} - {col.metadata}")

    return {
        "statusCode": 200,
        "body": collections
    }

if __name__ == "__main__":
    # response = get_collection('.py')
    # body = response.get("body")
    # documents = json.loads(body).get("documents", [])
    # for doc in documents:
    #     print("Document:", doc)
    # result = print_collection_contents()
    result = test_collections_query()

