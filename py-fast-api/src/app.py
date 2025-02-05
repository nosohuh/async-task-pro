from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db.db import get_db_connection, get_import_db_table
from services.redis import get_redis_connection
from api.routes import app as router
import google.generativeai as genai
import os
from dotenv import load_dotenv
from utils.message_loader import MessageLoader

# Load messages
message = MessageLoader()
# Load env variables
load_dotenv()
app = FastAPI(
    title=message.get("fastapi", "title"),
    version=message.get("fastapi", "version"),
    description=message.get("fastapi", "description"),
)
# Genie Api
gemini = os.getenv("GEMINI_API_KEY")
if not gemini:
    raise ValueError("API anahtarı bulunamadı. Lütfen .env dosyasını kontrol edin.")
genai.configure(api_key=gemini)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # İzin verilen domainler
    allow_credentials=True,
    allow_methods=["*"],  # Tüm HTTP metodlarına izin ver
    allow_headers=["*"],  # Tüm başlıklara izin ver
)
# db ve redis
db_conn = None
redis_conn = None
try:
    db_conn = get_db_connection()
    redis_conn = get_redis_connection()
except Exception as e:
    print(f"connect error: {e}")

# Router
app.include_router(router)


# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Aİ SERV..."}


# tables endpoint
@app.on_event("startup")
def on_startup():
    get_import_db_table()


# Shutdown event
@app.on_event("shutdown")
def shutdown_event():
    if db_conn:
        db_conn.close()
        print("***DB Closed***")
    if redis_conn:
        redis_conn.close()
        print("***Redis Closed***")
