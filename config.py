import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env si existe
load_dotenv()
 
class Config:
    # API Key para OpenWeatherMap
    API_KEY = os.getenv('API_KEY')
    
    # Configuración de Redis
    # Primero intentamos obtener la URL completa
    REDIS_URL = os.getenv('REDIS_URL')
    
    # Si no hay URL, construimos la conexión a partir de componentes individuales
    if not REDIS_URL:
        REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
        REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
        REDIS_DB = int(os.getenv('REDIS_DB', 0))
        REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', '')
        
        # Construir URL de Redis
        if REDIS_PASSWORD:
            REDIS_URL = f'redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}'
        else:
            REDIS_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}'
    
    # Entorno de la aplicación
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')