import os
import time
import prompt_engine
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from openai import OpenAI
from dotenv import load_dotenv

def get_code_review(code: str) -> str:
    model = 'gpt-4-turbo'
    print(f"============= CODE REVIEW USING OPEN AI MODEL: {model} ================")
    # Create an OpenAI client
    load_dotenv()  # Load from .env in current directory
    api_key = os.environ.get("OPEN_API_KEY")

    prompt = prompt_engine.buildCodeReviewPrompt(code)

    client = OpenAI(api_key=api_key)
    openai_response = client.chat.completions.create(model = model,
        messages = [
            {"role": "user", "content": prompt}
        ],
        temperature = 0.7,
        max_tokens = 1500)
    return openai_response






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
    print(f"==ELAPSED TIME== Open AI Code Review took {elapsed_time:.4f} seconds")
    print("==CHOICES==:",len(review.choices))
    print("==USAGE==:",review.usage)
    print("\n==CONTENT==\n",review.choices[0].message.content)

