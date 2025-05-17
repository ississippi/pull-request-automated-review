import os
import anthropic
import boto3
import time
import prompt_engine
from dotenv import load_dotenv

# Create an SSM client
ssm = boto3.client('ssm')
def get_parameter(name):
    """Fetch parameter value from Parameter Store"""
    response = ssm.get_parameter(
        Name=name,
        WithDecryption=True
    )
    return response['Parameter']['Value']
# Load secrets at cold start
ANTHROPIC_API_KEY = get_parameter("/prreview/ANTHROPIC_API_KEY")
if ANTHROPIC_API_KEY is None:
    raise ValueError("ANTHROPIC_API_KEY not found in parameter store.")

def get_code_review(diffs):
    try:
        model = 'claude-3-7-sonnet-20250219'
        print(f"============= CODE REVIEW USING ANTHROPIC MODEL: {model} ================")
        
        # Create a prompt for the code review
        prompt = prompt_engine.buildDiffReviewPrompt(diffs)
        
        # Create an OpenAI client
        load_dotenv()  # Load from .env in current directory
        # print(f"Using Anthropic API Key: {api_key}")
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        
        message = client.messages.create(
            model=model,
            max_tokens=1500,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
    except Exception as e:
        print(f"Error in get_code_review(): {e}")
        message = None
    
    return message

def get_code_review_augmented(diffs, rag_context):
    try:
        model = 'claude-3-7-sonnet-20250219'
        print(f"============= CODE REVIEW USING ANTHROPIC MODEL: {model} ================")
        
        # Create a prompt for the code review
        prompt = prompt_engine.buildDiffReviewPromptAugmented(diffs, rag_context)
        
        # Create an OpenAI client
        load_dotenv()  # Load from .env in current directory
        # print(f"Using Anthropic API Key: {api_key}")
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        
        message = client.messages.create(
            model=model,
            max_tokens=1500,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
    except Exception as e:
        print(f"Error in get_code_review(): {e}")
        message = None

    return message


if __name__ == "__main__":
    # Example usage
    #example_code = """
    #def add(a, b):
    #    return a + b
    #"""
    example_code = """
    diff --git a/ts/src/base/Exchange.ts b/ts/src/base/Exchange.ts
    index a4dc8e150b95b..5d76858ab6a11 100644
    --- a/ts/src/base/Exchange.ts
    +++ b/ts/src/base/Exchange.ts
    @@ -7226,7 +7226,12 @@ export default class Exchange {
                if (currentSince >= current) {
                    break;
                }
    -            tasks.push (this.safeDeterministicCall (method, symbol, currentSince, maxEntriesPerRequest, timeframe, params));
    +            const checkEntry = await this.safeDeterministicCall (method, symbol, currentSince, maxEntriesPerRequest, timeframe, params);
    +            if ((checkEntry.length) === (maxEntriesPerRequest - 1)) {
    +                tasks.push (this.safeDeterministicCall (method, symbol, currentSince, maxEntriesPerRequest + 1, timeframe, params));
    +            } else {
    +                tasks.push (checkEntry);
    +            }
                currentSince = this.sum (currentSince, step) - 1;
            }
            const results = await Promise.all (tasks);
    """
    start_time = time.time()
    review = get_code_review(example_code)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"==ELAPSED TIME== Anthropic Code Review took {elapsed_time:.4f} seconds")
    print("==USAGE==:", review.usage)
    print("==CONTENT==\n")
    print(review.content[0].text)
