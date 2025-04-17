from fastapi import APIRouter, UploadFile, File, Depends
import shutil
import os
from src.core.services.file_storage_service import FileStorageService
from src.core.dependency_injection.dependency_injection import build_file_storage_service
from src.presentation.dto.file_dto import UploadFileDTO, FileDTO,ResponseFileDTO
from src.presentation.responses.base_response import Response
routerfile = APIRouter(prefix="/api/v1/files", tags=["files"])

@routerfile.post("/upload", response_model=Response[ResponseFileDTO])
async def subir(file: UploadFile = File(...),
                file_service: FileStorageService= Depends(build_file_storage_service)
                ):
    temp_path = f"temp/{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    url = await file_service.upload_file(FileDTO(file=temp_path, file_name=file.filename))
    os.remove(temp_path)
    return url
