from newsapi import NewsApiClient
import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv('NEWSAPI_KEY')
print(f'API Key: {api_key[:10]}...' if api_key else 'NOT FOUND')

newsapi = NewsApiClient(api_key=api_key)

# Test with broader keywords
articles = newsapi.get_everything(
    q='technology OR AI',
    from_param='2026-04-02',
    language='en',
    page_size=5
)

print(f'Found {len(articles["articles"])} articles')
if articles['articles']:
    print('First article:', articles['articles'][0]['title'])