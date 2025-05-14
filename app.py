from flask import Flask, request, jsonify
import requests
from config import Config
from cache import get_cache, set_cache

app = Flask(__name__)

@app.route('/')
def home():
    return 'Weather API is running!'

@app.route('/weather')
def get_weather():
    city = request.args.get('city')
    if not city:
        return jsonify({'error': 'City parameter is required'}), 400

    cache_key = f'weather:{city.lower()}'
    cached = get_cache(cache_key)
    if cached:
        return jsonify({'source': 'cache', 'data': eval(cached)})

    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={Config.API_KEY}&units=metric&lang=es'
    response = requests.get(url)
    if response.status_code != 200:
        return jsonify({'error': 'City not found or API error'}), 404

    data = response.json()
    set_cache(cache_key, str(data), ex=300)  # cache for 5 min
    return jsonify({'source': 'api', 'data': data})

if __name__ == '__main__':
    app.run(debug=True) 