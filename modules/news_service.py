import requests
import time

class NewsService:
    def __init__(self, config):
        self.config = config
        self.api_key = config.get('news', {}).get('api_key', '')
        self.source = config.get('news', {}).get('source', 'bbc-news')
        self.update_interval = config.get('news', {}).get('update_interval_min', 30) * 60
        self.last_update = 0
        self.cached_headlines = []
        
    def update(self):
        """Update news data if interval has passed"""
        current_time = time.time()
        if current_time - self.last_update > self.update_interval or not self.cached_headlines:
            self._fetch_news()
            self.last_update = current_time
    
    def _fetch_news(self):
        """Fetch news headlines from API"""
        if not self.api_key or self.api_key == 'YOUR_NEWSAPI_KEY':
            self.cached_headlines = ["API Key Required - Configure in config.json"]
            return
            
        try:
            url = f"https://newsapi.org/v2/top-headlines"
            params = {
                'sources': self.source,
                'apiKey': self.api_key
            }
            response = requests.get(url, params=params, timeout=5)
            if response.status_code == 200:
                data = response.json()
                self.cached_headlines = [article['title'] for article in data.get('articles', [])[:10]]
                if not self.cached_headlines:
                    self.cached_headlines = ["No news available"]
            else:
                self.cached_headlines = ["News API Error"]
        except Exception as e:
            print(f"News service error: {e}")
            self.cached_headlines = ["News service offline"]
    
    def get_headlines(self):
        """Get current headlines"""
        self.update()
        return self.cached_headlines

