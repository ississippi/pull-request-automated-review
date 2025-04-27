import json
import boto3
import os
import git_provider
import sonnet_client
import time



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

                # 2. Submit the diff to the code review system
                start_time = time.time()
                review = sonnet_client.get_code_review(diff)
                end_time = time.time()
                elapsed_time = end_time - start_time
                print(f"==ELAPSED TIME== Anthropic Code Review took {elapsed_time:.4f} seconds")
                print("==USAGE==:", review.usage)                
                
                # Build review message
                review_message = {
                    "reviewTitle": f'Review for PR #{pr_number} in {repo}: {request_data.get("title", "No Title Provided")}',
                    "metadata": request_data,
                    "review": review
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

if __name__ == "__main__":
    # For local testing, you can simulate an event
    test_event = {
        "Records": [
            {
                "EventSource": "aws:sns",
                "Sns": {
                    "Message": json.dumps({
                        "repo": "example/repo",
                        "pr_number": 123,
                        "title": "Fix issue with code review"
                    })
                }
            }
        ]
    }
    lambda_handler(test_event, None)  # Call the handler with the test event
    print("Local test completed.")