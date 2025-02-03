from fastapi import File, UploadFile, HTTPException
import os
import google.generativeai as genai
import services.redis as redis 


redis_connection = redis.get_redis_connection()
model = genai.GenerativeModel('gemini-1.5-flash')

async def upload_pdf(file: UploadFile = File(...), prompt: str = None):
    if not prompt:
        prompt = "Bu dosyada kaç sayfa var?" 
    file_path = f"temp_{file.filename}"
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    try:
        sample_file = genai.upload_file(path=file_path, display_name=file.filename)
        print(f"Uploaded file '{sample_file.display_name}' as: {sample_file.uri}")
        response = model.generate_content([sample_file, prompt])
        if redis_connection:
            redis_connection.set(file.filename, file_path)
        return {"response": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating content: {str(e)}")
    finally:
        # Geçici dosya siliniyor
        if os.path.exists(file_path):
            os.remove(file_path)
