# Weather API

API de clima construida con Flask y Redis para cache, que permite consultar el clima actual y pronóstico de 5 días utilizando datos de OpenWeatherMap.

## Características

- Consulta del clima actual para cualquier ciudad
- Pronóstico de 5 días con intervalos de 3 horas
- Caché de resultados para mejorar el rendimiento
- Documentación interactiva con Swagger UI
- Guía completa de la API con ejemplos de código

## Estructura del proyecto

```
weather-api/
│
├── app.py                  # Código principal del servidor Flask
├── config.py               # Configuración: claves, Redis, etc.
├── cache.py                # Módulo para el manejo de Redis
├── docs.html               # Documentación detallada con ejemplos
├── requirements.txt        # Paquetes necesarios
├── .env                    # Variables de entorno (API_KEY, etc.)
├── Dockerfile              # Configuración para Docker
├── .dockerignore           # Archivos a ignorar en Docker
├── app.yaml                # Configuración para Google Cloud
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

Accede a `http://localhost:5000/` para ver el dashboard principal de la API.

### Endpoints disponibles

- `/dashboard` - Panel informativo de la API
- `/swagger` - Documentación interactiva con Swagger UI
- `/docs` - Guía completa de la API con ejemplos de código
- `/weather?city={nombre_ciudad}` - Obtiene el clima actual
- `/forecast?city={nombre_ciudad}` - Obtiene el pronóstico de 5 días

### Ejemplos de consultas

- Clima actual de Lima, Perú:
  ```
  http://localhost:5000/weather?city=Lima,PE
  ```
- Clima actual de Buenos Aires, Argentina:
  ```
  http://localhost:5000/weather?city=Buenos%20Aires,AR
  ```
- Pronóstico de 5 días para Cusco, Perú:
  ```
  http://localhost:5000/forecast?city=Cusco,PE
  ```

**Nota:** Puedes cambiar el valor de `city` por cualquier ciudad y país (usa el código de país ISO 3166-1 alpha-2).

## Notas
- Asegúrate de tener un servidor Redis corriendo localmente o actualiza la variable `REDIS_URL` en `.env`.

## Despliegue en Google Cloud Run

### Preparación

1. Instalar [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)
2. Iniciar sesión: `gcloud auth login`
3. Configurar el proyecto: `gcloud config set project [ID_DEL_PROYECTO]`

### Despliegue con Dockerfile

1. Construir la imagen de Docker:
   ```bash
   gcloud builds submit --tag gcr.io/[ID_DEL_PROYECTO]/weather-api
   ```

2. Desplegar en Cloud Run:
   ```bash
   gcloud run deploy weather-api \
     --image gcr.io/[ID_DEL_PROYECTO]/weather-api \
     --platform managed \
     --region [REGION] \
     --allow-unauthenticated \
     --set-env-vars "API_KEY=[TU_API_KEY],REDIS_HOST=[REDIS_HOST],REDIS_PORT=[REDIS_PORT],REDIS_DB=0"
   ```

### Configuración de Variables de Entorno en Cloud Run

Para el correcto funcionamiento de la aplicación, debes configurar las siguientes variables de entorno en Cloud Run:

- `API_KEY`: Tu API key de OpenWeatherMap
- `REDIS_HOST`: Host de Redis (puedes usar Memorystore en GCP)
- `REDIS_PORT`: Puerto de Redis (generalmente 6379)
- `REDIS_DB`: Número de base de datos Redis (generalmente 0)

### Configuración de Redis en Google Cloud

Para entornos de producción, se recomienda utilizar Memorystore para Redis:

1. Crear una instancia de Memorystore para Redis:
   ```bash
   gcloud redis instances create weather-api-redis \
     --size=1 \
     --region=[REGION] \
     --redis-version=redis_6_x
   ```

2. Obtener la dirección IP de la instancia:
   ```bash
   gcloud redis instances describe weather-api-redis --region=[REGION]
   ```

3. Usar esta dirección IP como `REDIS_HOST` en la configuración de Cloud Run.