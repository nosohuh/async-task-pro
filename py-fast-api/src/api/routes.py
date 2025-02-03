# api/routes.py
from fastapi import APIRouter, UploadFile, File, Form
from src.api.handler.pdf import upload_pdf

app = APIRouter()

@app.post("/pdf/")
async def handle_upload_pdf(file: UploadFile = File(...), prompt: str = Form(None)):
    return await upload_pdf(file, prompt)
