# Weather API

API de clima construida con Flask y Redis para cache.

## Estructura del proyecto

```
weather-api/
│
├── app.py                  # Código principal del servidor Flask
├── config.py               # Configuración: claves, Redis, etc.
├── cache.py                # Módulo para el manejo de Redis
├── requirements.txt        # Paquetes necesarios
├── .env                    # Variables de entorno (API_KEY, etc.)
└── README.md               # Instrucciones para el repositorio
```

## Instalación

1. Clona el repositorio y entra al directorio:
   ```bash
   git clone <repo_url>
   cd weather-api
   ```
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Crea un archivo `.env` con tu API_KEY y la URL de Redis:
   ```env
   API_KEY=your_api_key_here
   REDIS_URL=redis://localhost:6379/0
   ```
4. Ejecuta la aplicación:
   ```bash
   python app.py
   ```

## Uso

Accede a `http://localhost:5000/` para verificar que la API está corriendo.

## Notas
- Asegúrate de tener un servidor Redis corriendo localmente o actualiza la variable `REDIS_URL` en `.env`. 