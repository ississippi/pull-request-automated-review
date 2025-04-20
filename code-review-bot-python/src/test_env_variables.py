import os
from dotenv import load_dotenv

def main():
    # Load environment variables from .env file
    load_dotenv()  # defaults to loading from .env in current directory
    
    # Retrieve the API key from environment variables
    load_dotenv()  # Load from .env in current directory
    mysecret = os.getenv('MY_SECRET')
    print("MY_SECRET:", mysecret)
    anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
    print("ANTHROPIC_API_KEY:", anthropic_api_key)
    gemini_api_key = os.getenv('GEMINI_API_KEY')
    print("GEMINI_API_KEY:", gemini_api_key)    
    openai_api_key = os.getenv('OPEN_API_KEY')
    print("OPEN_API_KEY:", openai_api_key)
  
    #if not api_key:
    #    raise ValueError("OPENAI_API_KEY environment variable is not set.")
    #print("API Key is set:", api_key)

if __name__ == "__main__":
    main()