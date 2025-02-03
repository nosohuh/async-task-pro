from services.redis import get_redis_connection
from db.db import get_db_connection
from fastapi import UploadFile, File


async def upload_file(file: UploadFile = File(...)):
    r = get_redis_connection()
    conn = get_db_connection()

    if not r or not conn:
        return {"error": "Redis or Database connection failed"}

    file_location = f"./uploads/{file.filename}"
    with open(file_location, "wb") as f:
        f.write(file.file.read())

    try:
        r.set(file.filename, file_location)
        print(f"Dosya yolu Redis'e kaydedildi: {file.filename}")
    except Exception as e:
        print(f"Error saving to Redis: {e}")

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO file_upload (file_name, file_path, status) 
                VALUES (%s, %s, %s)
                """, 
                (file.filename, file_location, "completed")
            )
            conn.commit()
            print(f"Dosya veritabanına kaydedildi: {file.filename}")
    except Exception as e:
        print(f"Error saving to database: {e}")

    return {"filename": file.filename, "file_path": file_location}