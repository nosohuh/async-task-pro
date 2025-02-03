import redis
from dotenv import load_dotenv
import os

load_dotenv()

redis_params = {
    'host': os.getenv('REDIS_HOST'),
    'port': os.getenv('REDIS_PORT'),
    'password': os.getenv('REDIS_PASSWORD')
}


def get_redis_connection():
    r = None
    try:
        r = redis.Redis(**redis_params)
        print('*Redis-Connect*')
        return r
    except Exception as e:
        print(f'Error: {e}')
    return None
