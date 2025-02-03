from fastapi import FastAPI
from db.db import get_db_connection, get_import_db_table
from services.redis import get_redis_connection
from api.routes import app as router  
import google.generativeai as genai
import os
from dotenv import load_dotenv


# Load env variables
load_dotenv()

app = FastAPI(
    title="PDF Upload API",
    version="0.1.0",
    description="Veritabanı ve Redis bağlantılı FastAPI uygulaması"
)
# Genie Api
gemini = os.getenv("GEMINI_API_KEY")
if not gemini:
    raise ValueError("API anahtarı bulunamadı. Lütfen .env dosyasını kontrol edin.")
genai.configure(api_key=gemini)



# db ve redis bağlantıları
db_conn = None
redis_conn = None
try:
    db_conn = get_db_connection()
    redis_conn = get_redis_connection()
except Exception as e:
    print(f"Bağlantı hatası: {e}")


# Router
app.include_router(router)

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "PDF Aİ"}

# tabloları oluştur
@app.on_event("startup")
def on_startup():
    get_import_db_table()  

# Uygulama kapandığında bağlantıları temizle
@app.on_event("shutdown")
def shutdown_event():
    if db_conn:
        db_conn.close()
        print("***DB bağlantısı kapatıldı***")
    if redis_conn:
        redis_conn.close()
        print("***Redis bağlantısı kapatıldı***")
