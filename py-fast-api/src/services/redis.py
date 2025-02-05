import redis  # type: ignore
from dotenv import load_dotenv  # type: ignore
import os  # type: ignore

load_dotenv()

redis_params = {
    "host": os.getenv("REDIS_HOST"),
    "port": os.getenv("REDIS_PORT"),
    "password": os.getenv("REDIS_PASSWORD"),
    "db": 0,  # Varsayılan veritabanı
    "decode_responses": True,  # Yanıtları düzgün formatta almak için
}


def get_redis_connection():
    r = None
    try:
        # Redis bağlantısı oluşturuluyor
        r = redis.Redis(**redis_params)
        if r.ping():  # Bağlantı kontrolü
            print("* Redis - Connected Successfully *")
            return r
        else:
            print("* Redis - Connection Failed *")
    except redis.ConnectionError as e:
        print(f"Connection error: {e}")
    except redis.AuthenticationError as e:
        print(f"Authentication error: {e}")
    except Exception as e:
        print(f"Error: {e}")
    return None
