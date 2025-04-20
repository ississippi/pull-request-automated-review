import anthropic
import os
import time
import prompt_engine
from dotenv import load_dotenv

def get_code_review(code):
    model = 'claude-3-7-sonnet-20250219'
    print(f"============= CODE REVIEW USING ANTHROPIC MODEL: {model} ================")
    
    # Create a prompt for the code review
    prompt = prompt_engine.buildCodeReviewPrompt(code)
    
    # Create an OpenAI client
    load_dotenv()  # Load from .env in current directory
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    
    client = anthropic.Anthropic(api_key=api_key)
    
    message = client.messages.create(
        model=model,
        max_tokens=1500,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    return message


if __name__ == "__main__":
    # Example usage
    example_code = """
    def add(a, b):
        return a + b
    """
    start_time = time.time()
    review = get_code_review(example_code)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"==ELAPSED TIME== Anthropic Code Review took {elapsed_time:.4f} seconds")
    print("==USAGE==:", review.usage)
    print("==CONTENT==\n")
    print(review.content[0].text)
