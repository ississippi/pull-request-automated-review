# Get Snippet
# Json snippets
#
# "snippets": [
#     "id"
#     "snippet"
#     "language"
#     "repo_file_name"
# ]
import os
import json
import random
import prompt_engine
from dotenv import load_dotenv
import os

def get_random_snippet():
    # Open and read the JSON file
    with open('C:\\Users\\issis\\source\\repos\\pull-request-automated-review\\test-data\\python-snippets.json', 'r') as file:
        data = json.load(file)
    # Randomly select a snippet from the list
    snippet_id = random.choice(range(len(data["snippets"])))
    snippet = data["snippets"][snippet_id]
    file.close()
    return snippet


def main():
    
    #load_dotenv("C:\\Users\\issis\\source\\repos\\pull-request-automated-review\\code-review-bot-python\\.env")  # defaults to loading from .env in current directory
    load_dotenv()  # Load from .env in current directory
    api_key = os.getenv('OPEN_API_KEY')
    print("api_key:", api_key)
    test_var = os.getenv('MY_SECRET')
    print("test_var:", test_var)
    print("Current dir:", os.getcwd())


    snippet = get_random_snippet()
    print(snippet)
    code_review = prompt_engine.buildCodeReviewPrompt(snippet)
    print(code_review)
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set.")
    print("API Key is set.", api_key)
if __name__ == "__main__":
    main()