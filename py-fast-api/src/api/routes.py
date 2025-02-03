from fastapi import APIRouter, UploadFile, File
from api.handler.file_upload import upload_file 

pdf_router = APIRouter()

@pdf_router.post("/uploadfile/")
async def upload_file_route(file: UploadFile = File(...)):
    return await upload_file(file)
