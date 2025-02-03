from fastapi import FastAPI, HTTPException
from services.redis import get_redis_connection

app = FastAPI()

redis_client = get_redis_connection()

@app.post("/set/{key}")
def set_value(key: str, value: str):
    try:
        redis_client.set(key, value)
        return {"message": f"{key} Redis'e kaydedildi."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Redis hatası: {e}")

@app.get("/get/{key}")
def get_value(key: str):
    value = redis_client.get(key)
    if value is None:
        raise HTTPException(status_code=404, detail=f"{key} bulunamadı.")
    return {"key": key, "value": value.decode()}

@app.on_event("shutdown")
def shutdown_event():
    redis_client.close()
    print('*Redis-Close*')
