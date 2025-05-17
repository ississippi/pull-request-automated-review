import os
import boto3
import json
from dotenv import load_dotenv
from botocore.exceptions import ClientError

ssm = boto3.client('ssm')
def get_parameter(name):
    """Fetch parameter value from Parameter Store"""
    response = ssm.get_parameter(
        Name=name,
        WithDecryption=True
    )
    return response['Parameter']['Value']
# Load secrets at cold start
BEDROCK_KB_ID = get_parameter("/prreview/BEDROCK_KB_ID")
if BEDROCK_KB_ID is None:
    raise Exception("bedrock_retrieve: BEDROCK_KB_ID environment variable not set")

def retrieve_from_knowledge_base(query_text, region="us-east-1"):
    """
    Use the AWS Bedrock Retrieve API to query a knowledge base.
    
    Args:
        query_text (str): The text query to send to the knowledge base
        knowledge_base_id (str): The ID of the knowledge base to query
        region (str): AWS region where the knowledge base is located
    
    Returns:
        dict: The response from the knowledge base
    """
    # Create a Bedrock Agent Runtime client
    bedrock_agent_runtime = boto3.client('bedrock-agent-runtime', region_name=region)
    
    try:
        # Call the retrieve API
        response = bedrock_agent_runtime.retrieve(
            knowledgeBaseId=BEDROCK_KB_ID,
            retrievalQuery={
                'text': query_text
            },
            # Optional: Configure vector search parameters
            retrievalConfiguration={
                'vectorSearchConfiguration': {
                    'numberOfResults': 5  # Number of results to return
                    # You can add filters here if needed
                }
            }
        )
        
        return response
    except ClientError as e:
        print(f"Error querying knowledge base: {e}")
        raise

def retrieve_and_generate(query_text, knowledge_base_id, model_arn, region="us-east-1"):
    """
    Use the AWS Bedrock Retrieve and Generate API to query a knowledge base and generate
    a response based on the retrieved content.
    
    Args:
        query_text (str): The text query to send to the knowledge base
        knowledge_base_id (str): The ID of the knowledge base to query
        model_arn (str): The ARN of the foundation model to use for generation
        region (str): AWS region where the knowledge base is located
    
    Returns:
        dict: The response from the model
    """
    # Create a Bedrock Agent Runtime client
    bedrock_agent_runtime = boto3.client('bedrock-agent-runtime', region_name=region)
    
    try:
        # Call the retrieve_and_generate API
        response = bedrock_agent_runtime.retrieve_and_generate(
            input={
                'text': query_text
            },
            retrieveAndGenerateConfiguration={
                'type': 'KNOWLEDGE_BASE',
                'knowledgeBaseConfiguration': {
                    'knowledgeBaseId': knowledge_base_id,
                    'modelArn': model_arn
                }
            }
        )
        
        return response
    except ClientError as e:
        print(f"Error in retrieve and generate: {e}")
        raise

# Example usage
if __name__ == "__main__":
 
    # Example for Claude model ARN
    MODEL_ARN = "arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-sonnet-20240229-v1:0"
    
    # Example query
    queryRetrieveOnly = ''' What are the Python naming conventions?
    '''
    queryRandG = '''You are a Senior software engineer. 
    Please evaluate the following code snippet for bugs and style. 
    Reference the Python style guide and site relevant style guide section numbers in your response."
code:
    src/DynamoService.cs
﻿using Amazon.DynamoDBv2;
using Amazon.DynamoDBv2.Model;
using System;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace NotificationsService.Services
{
    public class DynamoService
    {
        private readonly IAmazonDynamoDB _dynamoDbClient;
        private readonly string _tableName = "PRReviews";
        private readonly ILogger<PrController> _logger;

        public DynamoService(ILogger<PrController> logger)
        {
            _dynamoDbClient = new AmazonDynamoDBClient(); // uses default credentials and region
            _logger = logger;
        }

        public async Task<Dictionary<string, AttributeValue>> GetReviewByIdAsync(int prNumber, string repo)
        {
            // Build the DDB partition key.
            var partitionKey = $"{repo}#{prNumber}";
            _logger.LogInformation($"partitionKey: {partitionKey}");
            var request = new GetItemRequest
            {
                TableName = _tableName,
                Key = new Dictionary<string, AttributeValue>
                {
                    { "prId", new AttributeValue { S = partitionKey } } // use the actual partition key name
                }
            };

            var response = await _dynamoDbClient.GetItemAsync(request);

            if (response.Item == null || response.Item.Count == 0)
            {
                Console.WriteLine("No item found with the specified ID.");
                return null;
            }

            return response.Item;
        }

        // Optionally: scan or query by other attributes
        public async Task<List<Dictionary<string, AttributeValue>>> GetAllReviewsAsync()
        {
            var request = new ScanRequest
            {
                TableName = _tableName,
                Limit = 10 // avoid accidental full table scan
            };

            var response = await _dynamoDbClient.ScanAsync(request);
            return response.Items;
        }
    }
}
     '''
    # Example 1: Just retrieve information from the knowledge base
    retrieve_results = retrieve_from_knowledge_base(queryRetrieveOnly, BEDROCK_KB_ID)
    print("Retrieved results:")
    for i, result in enumerate(retrieve_results.get('retrievalResults', [])):
        print(f"Result {i+1}: {result.get('content', {}).get('text')}")
        print(f"Score: {result.get('score')}")
        print("-" * 40)
    
    # # Example 2: Retrieve and generate a response
    # generate_response = retrieve_and_generate(query, KB_ID, MODEL_ARN)
    # print("\nGenerated response:")
    # print(generate_response.get('output', {}).get('text'))