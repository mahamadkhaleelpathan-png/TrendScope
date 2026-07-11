import os
import requests

api_key = os.environ.get("GNEWS_API_KEY", "")
if not api_key:
    raise ValueError("GNEWS_API_KEY environment variable not set")
url = "https://gnews.io/api/v4/search"

params = {
    "q": "AI",
    "lang": "en",
    "max": 5,
    "apikey": api_key
}

response = requests.get(url, params=params, timeout=30)
data = response.json()
articles = data.get("articles", [])

for i, a in enumerate(articles):
    title = a.get("title", "No title")
    image = a.get("image", "")
    print(f"[{i+1}] {title}")
    print(f"    Image URL: {image}")
    print()