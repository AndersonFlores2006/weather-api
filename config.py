import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_KEY = os.getenv('API_KEY')
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0') 