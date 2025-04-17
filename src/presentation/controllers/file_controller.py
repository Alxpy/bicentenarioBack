from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from fastapi.responses import JSONResponse
import shutil
import os
from pathlib import Path
from typing import Optional
from src.core.services.file_storage_service import FileStorageService
from src.core.dependency_injection.dependency_injection import build_file_storage_service
from src.presentation.dto.file_dto import FileDTO, ResponseFileDTO
from src.presentation.responses.base_response import Response

file_router = APIRouter(
    prefix="/api/v1/files",
    tags=["File Storage"],
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "Invalid file or upload failed"},
        status.HTTP_413_REQUEST_ENTITY_TOO_LARGE: {"description": "File too large"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"}
    }
)

@file_router.post(
    "/upload",
    response_model=Response[ResponseFileDTO],
    status_code=status.HTTP_201_CREATED,
    summary="Upload a file",
    description="Uploads a file to the storage service and returns its access URL.",
    response_description="The URL of the uploaded file"
)
async def upload_file(
    file: UploadFile = File(..., description="The file to upload"),
    file_service: FileStorageService = Depends(build_file_storage_service),
    max_file_size: int = 10 * 1024 * 1024  
):
    try:
        file.file.seek(0, os.SEEK_END)
        file_size = file.file.tell()
        if file_size > max_file_size:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File too large. Max size is {max_file_size} bytes"
            )
        file.file.seek(0)

        temp_dir = Path("temp")
        temp_dir.mkdir(exist_ok=True)
        temp_path = temp_dir / file.filename

        try:
            with open(temp_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            upload_result = await file_service.upload_file(
                FileDTO(file=str(temp_path), file_name=file.filename)
            )

            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content=upload_result.dict()
            )

        finally:
            if temp_path.exists():
                temp_path.unlink()

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload file: {str(e)}"
        )