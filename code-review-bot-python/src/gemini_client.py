from google import genai
import os
import time
import prompt_engine
from dotenv import load_dotenv

def get_code_review(code: str) -> str:
    model_str = 'gemini-1.5-pro-latest'
    print(f"============= CODE REVIEW USING GOOGLE GEMINI MODEL: {model_str} ================")
    
    # Create a prompt for the code review
    prompt = prompt_engine.buildCodeReviewPrompt(code)
    
    # Create a Google Generative AI clientpython gemi
    load_dotenv()  # Load from .env in current directory
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=model_str, contents=prompt
    )
    #print(response)
    return response

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
    print(f"==ELAPSED TIME== Gemini Code Review took {elapsed_time:.4f} seconds")
    print("==USAGE==:")
    print("Prompt tokens:", review.usage_metadata.prompt_token_count)
    print("Completion tokens:", review.usage_metadata.candidates_token_count)
    print("Total tokens:", review.usage_metadata.total_token_count)    
    print("==CONTENT==\n")
    print(review.text)


