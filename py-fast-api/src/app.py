from fastapi import FastAPI
from db.db import get_db_connection, get_import_db_table
from services.redis import get_redis_connection
from api.routes import pdf_router  

app = FastAPI(
    title="PDF Upload API",
    version="0.1.0",
    description="Veritabanı ve Redis bağlantılı FastAPI uygulaması"
)

# db ve reds connect
db_conn = get_db_connection()
redis_conn = get_redis_connection()

# Router
app.include_router(pdf_router)

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
