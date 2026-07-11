import requests
import os
from dotenv import load_dotenv
load_dotenv()
key = os.getenv('NEWSAPI_KEY')
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
url = 'https://newsapi.org/v2/everything?q=trump&apiKey=' + key + '&language=en&sortBy=publishedAt&pageSize=5'
response = requests.get(url, headers=headers)
print('NewsAPI Status:', response.status_code)
data = response.json()
print('Articles found:', len(data.get('articles', [])))
if response.status_code == 200 and data.get('articles'):
    for i, art in enumerate(data['articles'][:3]):
        print(f'{i+1}. {art['title']}')
else:
    print('Error details:', data)
