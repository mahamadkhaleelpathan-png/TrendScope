import requests
import os
from dotenv import load_dotenv

load_dotenv(".env")

api_key = os.getenv("GROQ_API_KEY")
print(f"Key found: {api_key[:15]}..." if api_key else "NO KEY FOUND")
print(f"Current folder: {os.getcwd()}")

# Try direct read
with open(".env", "r") as f:
    content = f.read()
    print(f"File content: {content}")