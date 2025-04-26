import json
import boto3
import os
import git_provider

sns_client = boto3.client('sns')

PR_REVIEW_TOPIC_ARN = os.environ.get('PR_REVIEW_TOPIC_ARN')

def lambda_handler(event, context):
    for record in event.get("Records", []):
        if record.get("EventSource") == "aws:sns":
            sns_message = record["Sns"]["Message"]
            print(f"Received PR Request: {sns_message}")
            
            try:
                request_data = json.loads(sns_message)

                # 1. Get the diff for this PR
                repo = request_data.get("repo")
                pr_number = request_data.get("pr_number")
                diff = git_provider.get_pr_diff(repo, pr_number)
                print(f'diff for PR #{pr_number} in {repo}...')

                # Build review message
                review_message = {
                    "reviewTitle": f"Review: {request_data.get('title')}",
                    "status": "Pending"
                }
                
                sns_client.publish(
                    TopicArn=PR_REVIEW_TOPIC_ARN,
                    Message=json.dumps(review_message)
                )
                print(f"Published PR Review: {review_message}")
                
            except json.JSONDecodeError:
                print(f"Invalid JSON in SNS Message: {sns_message}")
    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Processed PR Requests"})
    }
