import json
import boto3
import os

sns_client = boto3.client('sns')

PR_REQUEST_TOPIC_ARN = os.environ.get('PR_REQUEST_TOPIC_ARN')

def lambda_handler(event, context):
    try:
        body = json.loads(event.get('body', '{}'))
        
        # Optionally validate body here (title, description, etc.)
        print(f"Received PR Request: {json.dumps(body)}")
        sns_client.publish(
            TopicArn=PR_REQUEST_TOPIC_ARN,
            Message=json.dumps(body)
        )
        
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "PR Request published successfully"})
        }
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
