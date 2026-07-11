import os
import requests

api_key = os.environ.get("NEWSDATA_API_KEY", "")
if not api_key:
    raise ValueError("NEWSDATA_API_KEY environment variable not set")
url = "https://newsdata.io/api/1/news"

# Test WITHOUT date filter first
params = {
    "apikey": api_key,
    "q": "artificial intelligence OR AI",
    "language": "en",
    "size": 5
}

print("Testing NewsData.io WITHOUT date filter...")
response = requests.get(url, params=params, timeout=30)
print(f"Status: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    articles = data.get("results", [])
    print(f"Articles found: {len(articles)}")
    
    if articles:
        for i, a in enumerate(articles):
            title = a.get("title", "No title")
            content = a.get("content", "") or a.get("description", "")
            pub_date = a.get("pubDate", "No date")
            print(f"\n[{i+1}] {title}")
            print(f"Date: {pub_date}")
            print(f"Content length: {len(content)} chars")
            print(f"Content preview: {content[:150]}...")
    else:
        print("No articles found!")
        print(f"Full response: {data}")
else:
    print(f"Error: {response.text}")