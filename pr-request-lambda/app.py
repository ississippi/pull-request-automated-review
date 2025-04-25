import json

def lambda_handler(event, context):
    method = event.get("httpMethod")
    path = event.get("path")
    
    if method == "GET" and path == "/health":
        return {
            "statusCode": 200,
            "body": json.dumps({"status": "OK"})
        }
    
    elif method == "POST" and path == "/prrequest":
        try:
            body = json.loads(event.get("body", "{}"))
            # Do something with body
            response_message = {
                "message": "PR Request Received",
                "received": body
            }
            return {
                "statusCode": 200,
                "body": json.dumps(response_message)
            }
        except json.JSONDecodeError:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Invalid JSON"})
            }
    
    else:
        return {
            "statusCode": 404,
            "body": json.dumps({"error": "Not Found"})
        }
