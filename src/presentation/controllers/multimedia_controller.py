from fastapi import APIRouter, Depends, HTTPException
from src.core.abstractions.services.multimedia_service_abstract import IMultimediaService
from src.core.dependency_injection.dependency_injection import build_multimedia_service
from src.presentation.dto.multimedia_dto import MultimediaDTO
from src.presentation.responses.base_response import Response
from src.core.models.multimedia_domain import MultimediaDomain

multimedia_controller = APIRouter(
    prefix="/api/v1/multimedia",
    tags=["multimedia"]
)

@multimedia_controller.post("", response_model=Response[None])
async def create_multimedia(
    multimedia: MultimediaDTO,
    multimedia_service: IMultimediaService = Depends(build_multimedia_service)):
    try:
        return await multimedia_service.create_multimedia(multimedia)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@multimedia_controller.get("", response_model=Response[list[MultimediaDomain]])
async def get_all_multimedia(
    multimedia_service: IMultimediaService = Depends(build_multimedia_service)):
    try:
        return await multimedia_service.get_all_multimedia()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@multimedia_controller.get("/{id}", response_model=Response[MultimediaDomain])
async def get_multimedia_by_id(
    id: int,
    multimedia_service: IMultimediaService = Depends(build_multimedia_service)):
    try:
        return await multimedia_service.get_multimedia_by_id(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@multimedia_controller.put("/{id}", response_model=Response[None])
async def update_multimedia(
    id: int,
    multimedia: MultimediaDTO,
    multimedia_service: IMultimediaService = Depends(build_multimedia_service)):
    try:
        return await multimedia_service.update_multimedia(id, multimedia)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@multimedia_controller.delete("/{id}", response_model=Response[None])
async def delete_multimedia(
    id: int,
    multimedia_service: IMultimediaService = Depends(build_multimedia_service)):
    try:
        return await multimedia_service.delete_multimedia(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
