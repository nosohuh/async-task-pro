from fastapi import APIRouter, UploadFile, File, Form
from src.api.handler.pdf import upload_pdf, continue_chat, end_chat

app = APIRouter()


# PDF yükle
@app.post("/pdf/")
async def handle_upload_pdf(file: UploadFile = File(...), prompt: str = Form(None)):
    return await upload_pdf(file, prompt)


# PDF sonrası chat
@app.post("/chat/")
async def handle_continue_chat(
    file: UploadFile = File(...), user_input: str = Form(...)
):
    return await continue_chat(file, user_input)


# sohbet bitir ve kayıt sil
@app.post("/end-chat/")
async def handle_end_chat(file: UploadFile = File(...)):
    return await end_chat(file)
