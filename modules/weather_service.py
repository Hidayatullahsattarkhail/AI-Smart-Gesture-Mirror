import requests
import time
from datetime import datetime

class WeatherService:
    def __init__(self, config):
        self.config = config
        self.api_key = config.get('weather', {}).get('api_key', '')
        self.city = config.get('weather', {}).get('city', 'New York')
        self.units = config.get('weather', {}).get('units', 'metric')
        self.update_interval = config.get('weather', {}).get('update_interval_min', 10) * 60
        self.last_update = 0
        self.cached_data = None
        
    def update(self):
        """Update weather data if interval has passed"""
        current_time = time.time()
        if current_time - self.last_update > self.update_interval or self.cached_data is None:
            self._fetch_weather()
            self.last_update = current_time
    
    def _fetch_weather(self):
        """Fetch weather data from API"""
        if not self.api_key or self.api_key == 'YOUR_OPENWEATHERMAP_API_KEY':
            self.cached_data = {
                'temp': '--',
                'condition': 'API Key Required',
                'city': self.city
            }
            return
            
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather"
            params = {
                'q': self.city,
                'appid': self.api_key,
                'units': self.units
            }
            response = requests.get(url, params=params, timeout=5)
            if response.status_code == 200:
                data = response.json()
                self.cached_data = {
                    'temp': int(data['main']['temp']),
                    'condition': data['weather'][0]['description'].title(),
                    'city': data['name']
                }
            else:
                self.cached_data = {
                    'temp': '--',
                    'condition': 'Error',
                    'city': self.city
                }
        except Exception as e:
            print(f"Weather service error: {e}")
            self.cached_data = {
                'temp': '--',
                'condition': 'Offline',
                'city': self.city
            }
    
    def get_current_weather(self):
        """Get current weather data"""
        self.update()
        return self.cached_data

