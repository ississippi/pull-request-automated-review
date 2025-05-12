import os
import json
import time
import boto3
import git_provider
import sonnet_client
import bedrock_retrieve
import prompt_engine
from dotenv import load_dotenv
from pathlib import Path

# Create an SSM client
ssm = boto3.client('ssm')
def get_parameter(name):
    """Fetch parameter value from Parameter Store"""
    response = ssm.get_parameter(
        Name=name,
        WithDecryption=True
    )
    return response['Parameter']['Value']
# Load secrets from AWS at cold start
PR_REVIEWS_TABLE = get_parameter("/prreview/PR_REVIEWS_TABLE")
if PR_REVIEWS_TABLE is None:
    raise ValueError("PR_REVIEWS_TABLE was not found in the parameter store.")
PR_REVIEW_TOPIC_ARN = get_parameter("/prreview/PR_REVIEW_TOPIC_ARN")
if PR_REVIEW_TOPIC_ARN is None:
    raise ValueError("PR_REVIEW_TOPIC_ARN was not found in the parameter store.")

# Create an SNS client
sns_client = boto3.client('sns')
# Initialize DynamoDB
dynamodb = boto3.resource('dynamodb')
pr_reviews_table = dynamodb.Table(PR_REVIEWS_TABLE)

def lambda_handler(event, context):
    for record in event.get("Records", []):
        if record.get("EventSource") == "aws:sns":
            sns_message = record["Sns"]["Message"]
            print(f"Received PR Request: {sns_message}")
            # print(f'event: {event}')
            try:
                request_data = json.loads(sns_message)
                repo = request_data.get("repo")
                pr_number = request_data.get("pr_number")
                pr_state = request_data.get("pr_state", "unknown")

                # 1. Get the diff for this PR
                diffs = git_provider.get_supported_diffs(repo, pr_number)
                if diffs is None:
                    raise Exception(f'No supported diffs returned for for PR #{pr_number} in {repo}...') 

                # 2. Get context from the vector DB
                
                # 3. Submit the diffs to the code review system to get a code review
                start_time = time.time()
                review = sonnet_client.get_code_review(diffs)
                end_time = time.time()
                elapsed_time = end_time - start_time
                print(f"==ELAPSED TIME==: Anthropic Code Review for PR #{pr_number} in {repo} took {elapsed_time:.4f} seconds")
                print("==USAGE==:", review.usage)
                if review is None:
                    raise Exception(f'No review returned for for PR #{pr_number} in {repo}...')
                review_text = review.content[0].text

                # 4. Build review SNS message 
                review_title = f'Review for PR #{pr_number} in {repo}: {request_data.get("pr_title", "No Title Provided")}'
                review_message = {
                    "reviewTitle": review_title,
                    "metadata": request_data,  # << KEEP as dictionary, NOT json.dumps!
                    "review": review.content[0].text
                }
                print(f"--Review-- from LLM for PR #{pr_number} in {repo}: {review_message}")

                # 5. Now publish to SNS "review" topic
                sns_client.publish(
                    TopicArn=PR_REVIEW_TOPIC_ARN,
                    Message=json.dumps(review_message)  # << Here is where the full serialization happens
                )
                print(f"Published Review for PR #{pr_number} in {repo}: {review_title}")

                # 6. Store the review in the DynamoDB PRReviews table
                pr_id = f"{repo}#{pr_number}"
                item = {
                    "prId": pr_id,
                    "prState": pr_state,
                    "reviewTitle": review_title,
                    "metadata": request_data,
                    "review": review_text
                }
                pr_reviews_table.put_item(Item=item)
                
            except json.JSONDecodeError:
                print(f"Invalid JSON in SNS Message: {sns_message}")
            except Exception as e:
                print(f"Error processing PR Request: {e}")
    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Processed PR Requests"})
    }

# Sample incoming SNS message:

# {
#     "reviewTitle": "Review for PR #9 in ississippi/pull-request-automated-review: get_pr_files rafactoring",
#     "metadata": {
#         "pr_event_type": "reopened",
#         "pr_number": "9",
#         "repo": "ississippi/pull-request-automated-review",
#         "pr_title": "get_pr_files rafactoring",
#         "user_login": "ississippi",
#         "created_at": "2025-05-07T15:26:25Z",
#         "pr_state": "open",
#         "pr_body": "",
#         "html_url": "https://github.com/ississippi/pull-request-automated-review/pull/9",
#         "head_sha": "68c1e0d03ba0148e9c2095b8a310c40895c9032a",
#         "base_ref": "main"
#     },
#     "review": "# Diff Review - Files and Status\n\n- **Modified Files:**\n  - `pr_review/app.py`\n  - `pr_review/bedrock_retr


if __name__ == "__main__":
    repo = "ississippi/pull-request-test-repo"
    pr_number = 16    
    # For local testing, you can simulate an event
    test_event = {
        "Records": [
            {
                "EventSource": "aws:sns",
                "Sns": {
                    "Message": json.dumps({
                        "repo": "ississippi/pull-request-test-repo",
                        "pr_number": 16,
                        "pr_title": "Fix issue with code review",
                        "pr_state": "open",
                        "user_login": "ississippi",
                        "created_at": "2025-05-07T15:26:25Z",
                        "pr_body": ""
                    })
                }
            }
        ]
    }
    lambda_handler(test_event, None)  # Call the handler with the test event
    print("Local test completed.")