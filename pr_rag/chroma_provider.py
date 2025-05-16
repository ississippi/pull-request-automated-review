
import json
from chromadb import HttpClient

def get_collection():
    client = HttpClient(host="https://notifications.codeominous.com/api/v1")

    # Adjust collection name if needed
    collection = client.get_collection("web_docs")
    print("Total documents in collection:", collection.count())

    results = collection.query(query_texts=["What is Python style?"], n_results=3)

    return {
        "statusCode": 200,
        "body": json.dumps(results)
    }


if __name__ == "__main__":
    response = get_collection()
    body = response.get("body")
    documents = json.loads(body).get("documents", [])
    for doc in documents:
        print("Document:", doc)
        # Uncomment the following line to see the full response


