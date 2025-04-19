from dotenv import load_dotenv
import os

print("Working directory:", os.getcwd())

load_dotenv()  # Load from .env in current directory
print("MY_SECRET:", os.getenv("MY_SECRET"))
print("OPEN_API_KEY:", os.getenv("OPEN_API_KEY"))
