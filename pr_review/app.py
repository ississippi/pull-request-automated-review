import os
import json
import time
import boto3
import git_provider
import sonnet_client
import bedrock_retrieve
import prompt_engine
from dotenv import load_dotenv

dynamodb = boto3.resource('dynamodb')
PR_REVIEWS_TABLE = os.environ.get('PR_REVIEWS_TABLE', 'PRReviews')  # Default if env not set
PR_REVIEW_TOPIC_ARN = os.environ.get('PR_REVIEW_TOPIC_ARN')
KB_ID = os.environ.get("BEDROCK_KB_ID")
#PR_REVIEWS_TABLE = get_parameter("/prreview/PR_REVIEWS_TABLE")
table = dynamodb.Table(PR_REVIEWS_TABLE)
sns_client = boto3.client('sns')

def lambda_handler(event, context):
    for record in event.get("Records", []):
        if record.get("EventSource") == "aws:sns":
            sns_message = record["Sns"]["Message"]
            print(f"Received PR Request: {sns_message}")
            # print(f'event: {event}')
            try:
                request_data = json.loads(sns_message)

                # 1. Get the diff for this PR
                repo = request_data.get("repo")
                pr_number = request_data.get("pr_number")
                diff = git_provider.get_pr_diff(repo, pr_number)
                print(f'diff for PR #{pr_number} in {repo}...')
                if diff is None:
                    raise Exception(f'No diff returned for for PR #{pr_number} in {repo}...') 
                                    
                # 2. Get context from the vector DB - Bedrock Opensearch
                context_prompt = prompt_engine.buildPythonContextPrompt()

                context = bedrock_retrieve.retrieve_from_knowledge_base(context_prompt)
                # print("Retrieved results from Bedrock KB:")
                # for i, result in enumerate(retrieve_results.get('retrievalResults', [])):
                #     print(f"Result {i+1}: {result.get('content', {}).get('text')}")
                #     print(f"Score: {result.get('score')}")
                #     print("-" * 40)                
                if context is None:
                    raise Exception(f'No bedrock results returned for for PR #{pr_number} in {repo}...')
                
                # 2. Submit the diff to the code review system
                start_time = time.time()
                # review = sonnet_client.get_code_review(diff)
                review = sonnet_client.get_code_review_augmented(diff, context)
                end_time = time.time()
                elapsed_time = end_time - start_time
                print(f"==ELAPSED TIME== Anthropic Code Review took {elapsed_time:.4f} seconds")
                print("==USAGE==:", review.usage)

                # Build review message
                review_title = f'Review for PR #{pr_number} in {repo}: {request_data.get("pr_title", "No Title Provided")}'
                print(f'{review_title}')
                #review_title = f'{request_data.get("pr_title", "No Title Provided")} in repo {repo}'

                review_message = {
                    "reviewTitle": review_title,
                    "metadata": request_data,  # << KEEP as dictionary, NOT json.dumps!
                    "review": review.content[0].text
                }

                # Now publish
                sns_client.publish(
                    TopicArn=PR_REVIEW_TOPIC_ARN,
                    Message=json.dumps(review_message)  # << Here is where the full serialization happens
                )

                print(f"Published PR Review: {review_title}")

                # Store the review in DynamoDB
                pr_id = f"{repo}#{pr_number}"
                item = {
                    "prId": pr_id,
                    "reviewTitle": review_title,
                    "metadata": request_data,
                    "review": review.content[0].text
                }
                table.put_item(Item=item)
                print(f"Stored PR Review in DynamoDB with prId: {pr_id}")

                
            except json.JSONDecodeError:
                print(f"Invalid JSON in SNS Message: {sns_message}")
            except Exception as e:
                print(f"Error processing PR Request: {e}")
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