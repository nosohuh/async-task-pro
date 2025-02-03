import io
import google.generativeai as genai
from services.redis import get_redis_connection
from db.db import get_db_connection
from fastapi import UploadFile, HTTPException

async def process_salt_pdf(file: UploadFile):
    try:
        # Redis
        redis_client = get_redis_connection()
        # DB
        db_conn = get_db_connection()
        # Belleğe Al
        file_content = await file.read()
        doc_data = io.BytesIO(file_content)
        # PDF Gönder
        sample_doc = genai.upload_file(data=doc_data, mime_type='application/pdf')
        # AI'den İçerik Al
        prompt = "Summarize this document"
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content([sample_doc, prompt])
        # Redis de sakla
        redis_client.set(file.filename, response.text)
        print("AI yanıtı Redis'e kaydedildi.")
        # Yant Dön
        return {"filename": file.filename, "summary": response.text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Hata oluştu: {e}")
