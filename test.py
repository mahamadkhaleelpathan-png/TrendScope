import os
from dotenv import load_dotenv
load_dotenv()
print('🔍 ENV TEST RESULTS:')
print('NEWSAPI_KEY:', '✅ LOADED' if os.getenv('NEWSAPI_KEY') else '❌ NOT LOADED')
print('GROQ_API_KEY:', '✅ LOADED' if os.getenv('GROQ_API_KEY') else '❌ NOT LOADED')
print('Full NEWSAPI_KEY preview:', os.getenv('NEWSAPI_KEY')[:10] + '...' if os.getenv('NEWSAPI_KEY') else 'MISSING')
