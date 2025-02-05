from fastapi import File, UploadFile, HTTPException
import os
import google.generativeai as genai
import services.redis as redis
from db.db import get_db_connection
from db.log_model import log_ai_activity
from utils.message_loader import MessageLoader

# Load messages
message = MessageLoader()
# Redis
redis_connection = redis.get_redis_connection()
# Model
model = genai.GenerativeModel("gemini-1.5-flash")
# dir
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


# Dosya Yükle İlk Promt
async def upload_pdf(file: UploadFile = File(...), prompt: str = None):  # type: ignore
    print(prompt)
    if not prompt:
        prompt = message.get("pdf", "default_prompt")
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    try:
        # İşle
        sample_file = genai.upload_file(path=file_path, display_name=file.filename)
        print(f"Up.file: '{sample_file.display_name}' as: {sample_file.uri}")
        # içeriği dön
        response = model.generate_content([sample_file, prompt])
        # Redis'e yolu al
        if redis_connection:
            redis_connection.set(file.filename, file_path)
        # Geçmiş
        chat_history = f"User: {prompt}\nBot: {response.text}\n"
        redis_connection.set(f"chat_history_{file.filename}", chat_history)
        return {"response": response.text}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating content: {str(e)}"
        )


# Sohbet
async def continue_chat(file: UploadFile, user_input: str):
    if not user_input:
        raise HTTPException(
            status_code=400, detail=message.get("pdf", "user_input_required")
        )
    # Redis'ten dosya yolu al yoksa hata ver
    file_path = redis_connection.get(file.filename)
    if not file_path:
        raise HTTPException(
            status_code=404,
            detail=message.get("pdf", "file_not_found").format(file.filename),
        )
    file_path = file_path.decode("utf-8")
    chat_history = redis_connection.get(f"chat_history_{file.filename}")
    chat_history = chat_history.decode("utf-8") if chat_history else ""
    # Sohbeti biriktir
    chat_history += f"User: {user_input}\n"
    try:
        sample_file = genai.upload_file(path=file_path, display_name=file.filename)
        response = model.generate_content([sample_file, chat_history])
        # Sohbet geçmişine ve bot cevabını ekle
        chat_history += f"Bot: {response.text}\n"
        redis_connection.set(f"chat_history_{file.filename}", chat_history)
        return {"response": response.text}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating content: {str(e)}"
        )


# Sohbeti ve dosya temizliği db kayıt
async def end_chat(file: UploadFile):
    file_name = file.filename
    file_path = os.path.join(UPLOAD_DIR, file_name)
    # Redis'ten sohbet geçmişini al
    chat_history = redis_connection.get(f"chat_history_{file_name}")
    chat_history = chat_history.decode("utf-8") if chat_history else ""
    if not chat_history:
        raise HTTPException(
            status_code=400, detail=message.get("pdf", "chat_history_not_found")
        )
    try:
        # Dosyayı sil
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"file {file_name} delete.")
        else:
            print(f"{file_name} file not found.")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Dosya silinirken hata oluştu: {str(e)}"
        )
    # Redis'ten ilgili kayıtları sil
    if redis_connection:
        redis_connection.delete(file_name)
        redis_connection.delete(f"chat_history_{file_name}")
    # DB kayıt
    try:
        conn = get_db_connection()
        if conn:
            log_ai_activity(
                conn, file_name, "PDF", "gemini-1.5-flash", "UserIP", chat_history
            )
        else:
            raise HTTPException(status_code=500, detail="Db connection failed.")

        return {"message": message.get("pdf", "chat_ended")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Err logging activity: {str(e)}")
