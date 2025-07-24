from flask import Flask, request, jsonify, render_template_string, send_file
import requests
import os
from config import Config
from cache import get_cache, set_cache
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configuración de Swagger UI
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Weather API"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

@app.route('/static/swagger.json')
def swagger_json():
    swagger_doc = {
        "swagger": "2.0",
        "info": {
            "title": "Weather API",
            "description": "API para consultar el clima actual y pronóstico",
            "version": "1.0.0"
        },
        "basePath": "/",
        "schemes": ["http"],
        "paths": {
            "/weather": {
                "get": {
                    "summary": "Obtener clima actual",
                    "description": "Retorna datos del clima actual para una ciudad",
                    "parameters": [
                        {
                            "name": "city",
                            "in": "query",
                            "description": "Nombre de la ciudad",
                            "required": True,
                            "type": "string"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Datos del clima"
                        },
                        "400": {
                            "description": "Parámetro city requerido"
                        },
                        "404": {
                            "description": "Ciudad no encontrada o error en la API"
                        }
                    }
                }
            },
            "/forecast": {
                "get": {
                    "summary": "Obtener pronóstico de 5 días",
                    "description": "Retorna pronóstico del clima para los próximos 5 días",
                    "parameters": [
                        {
                            "name": "city",
                            "in": "query",
                            "description": "Nombre de la ciudad",
                            "required": True,
                            "type": "string"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Datos del pronóstico"
                        },
                        "400": {
                            "description": "Parámetro city requerido"
                        },
                        "404": {
                            "description": "Ciudad no encontrada o error en la API"
                        }
                    }
                }
            }
        }
    }
    return jsonify(swagger_doc)

@app.route('/')
def home():
    # Redireccionar directamente al dashboard
    from flask import redirect
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Weather API Dashboard</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                max-width: 1000px;
                margin: 0 auto;
                padding: 30px;
                line-height: 1.6;
                background-color: #f9f9f9;
                color: #333;
            }
            h1 {
                color: #2c3e50;
                border-bottom: 2px solid #3498db;
                padding-bottom: 15px;
                font-size: 2.5em;
                text-align: center;
                margin-bottom: 30px;
            }
            .container {
                display: flex;
                flex-wrap: wrap;
                justify-content: space-between;
                gap: 20px;
            }
            .endpoint {
                background: white;
                padding: 25px;
                border-radius: 8px;
                margin-bottom: 25px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                flex: 1 1 45%;
                transition: transform 0.3s ease, box-shadow 0.3s ease;
                border-left: 5px solid #3498db;
            }
            .endpoint:hover {
                transform: translateY(-5px);
                box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
            }
            .endpoint h2 {
                color: #3498db;
                margin-top: 0;
                font-size: 1.8em;
            }
            .endpoint p {
                margin-bottom: 15px;
                font-size: 1.1em;
            }
            .example-link {
                display: inline-block;
                background: #f2f2f2;
                padding: 8px 15px;
                border-radius: 4px;
                text-decoration: none;
                color: #333;
                font-family: monospace;
                font-size: 1.1em;
                border: 1px solid #ddd;
                transition: background 0.3s ease;
            }
            .example-link:hover {
                background: #e6e6e6;
            }
            .btn {
                display: block;
                background: #3498db;
                color: white;
                padding: 15px 25px;
                text-decoration: none;
                border-radius: 6px;
                margin: 30px auto 0;
                text-align: center;
                font-size: 1.2em;
                font-weight: bold;
                transition: background 0.3s ease;
                width: 300px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
            .btn:hover {
                background: #2980b9;
                box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
            }
            .header-icon {
                font-size: 1.2em;
                margin-right: 10px;
                color: #3498db;
            }
            .api-info {
                text-align: center;
                margin-bottom: 30px;
                font-size: 1.2em;
                line-height: 1.8;
                color: #555;
                background: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }
        </style>
    </head>
    <body>
        <h1>☁️ Weather API Dashboard</h1>

        <div class="api-info">
            <p>Bienvenido a la API del clima. Esta API proporciona datos meteorológicos actuales y pronósticos de manera sencilla y eficiente.</p>
            <p>Utiliza caché para mejorar el rendimiento y ofrece datos en formato JSON para fácil integración.</p>
        </div>

        <div class="container">
            <div class="endpoint">
                <h2>🌤️ Clima Actual</h2>
                <p>Obtén información detallada sobre el clima actual en cualquier ciudad del mundo.</p>
                <p><strong>Endpoint:</strong> /weather?city={nombre_ciudad}</p>
                <p><strong>Ejemplo:</strong> <a class="example-link" href="/weather?city=Madrid">/weather?city=Madrid</a></p>
            </div>

            <div class="endpoint">
                <h2>📅 Pronóstico de 5 días</h2>
                <p>Consulta el pronóstico del tiempo para los próximos 5 días con intervalos de 3 horas.</p>
                <p><strong>Endpoint:</strong> /forecast?city={nombre_ciudad}</p>
                <p><strong>Ejemplo:</strong> <a class="example-link" href="/forecast?city=Madrid">/forecast?city=Madrid</a></p>
            </div>
        </div>

        <div style="display: flex; justify-content: center; gap: 20px;">
            <a href="/swagger" class="btn">📚 Explorar Swagger UI</a>
            <a href="/docs" class="btn" style="background: #27ae60;">📖 Guía Completa de la API</a>
        </div>
    </body>
    </html>
    ''')

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

@app.route('/forecast')
def get_forecast():
    city = request.args.get('city')
    if not city:
        return jsonify({'error': 'City parameter is required'}), 400

    cache_key = f'forecast:{city.lower()}'
    cached = get_cache(cache_key)
    if cached:
        return jsonify({'source': 'cache', 'data': eval(cached)})

    url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={Config.API_KEY}&units=metric&lang=es'
    response = requests.get(url)
    if response.status_code != 200:
        return jsonify({'error': 'City not found or API error'}), 404

    data = response.json()
    set_cache(cache_key, str(data), ex=300)  # cache for 5 min
    return jsonify({'source': 'api', 'data': data})

@app.route('/docs')
def docs():
    docs_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'docs.html')
    return send_file(docs_path)

if __name__ == '__main__':
    # Obtener el puerto del entorno o usar 8080 por defecto (para Cloud Run)
    port = int(os.environ.get('PORT', 5000))
    # En producción, deshabilitar el modo debug
    debug = os.environ.get('FLASK_ENV', 'development') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)
