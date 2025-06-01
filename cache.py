import redis
import logging
from config import Config

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializar cliente Redis con manejo de errores
try:
    redis_client = redis.StrictRedis.from_url(Config.REDIS_URL, decode_responses=True)
    # Verificar conexión
    redis_client.ping()
    logger.info(f"Conexión exitosa a Redis en {Config.REDIS_URL}")
    REDIS_AVAILABLE = True
except redis.ConnectionError as e:
    logger.warning(f"No se pudo conectar a Redis: {e}. La caché estará deshabilitada.")
    REDIS_AVAILABLE = False
except Exception as e:
    logger.warning(f"Error al inicializar Redis: {e}. La caché estará deshabilitada.")
    REDIS_AVAILABLE = False

def get_cache(key):
    """Obtiene un valor de la caché. Retorna None si la caché no está disponible o la clave no existe."""
    if not REDIS_AVAILABLE:
        return None
    
    try:
        return redis_client.get(key)
    except Exception as e:
        logger.error(f"Error al obtener clave {key} de Redis: {e}")
        return None

def set_cache(key, value, ex=300):
    """Guarda un valor en la caché. No hace nada si la caché no está disponible."""
    if not REDIS_AVAILABLE:
        return
    
    try:
        redis_client.set(key, value, ex=ex)
        logger.debug(f"Valor guardado en caché con clave {key} por {ex} segundos")
    except Exception as e:
        logger.error(f"Error al guardar clave {key} en Redis: {e}")