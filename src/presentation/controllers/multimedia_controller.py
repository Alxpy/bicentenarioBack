from fastapi import APIRouter, Depends, HTTPException
from src.core.abstractions.services.multimedia_service_abstract import IMultimediaService
from src.core.dependency_injection.dependency_injection import build_multimedia_service
from src.presentation.dto.multimedia_dto import MultimediaDTO
from src.presentation.responses.base_response import Response
from src.core.models.multimedia_domain import MultimediaDomain

multimedia_router = APIRouter(
    prefix="/api/v1/multimedia",
    tags=["multimedia"]
)

@multimedia_router.post("", response_model=Response[None], summary="Create a new multimedia entry")
async def create_multimedia(
    multimedia: MultimediaDTO,
    multimedia_service: IMultimediaService = Depends(build_multimedia_service)):
    """
    Creates a new multimedia resource.
    """
    try:
        return await multimedia_service.create_multimedia(multimedia)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@multimedia_router.get("", response_model=Response[list[MultimediaDomain]], summary="Get all multimedia entries")
async def get_all_multimedia(
    multimedia_service: IMultimediaService = Depends(build_multimedia_service)):
    """
    Retrieves all multimedia resources.
    """
    try:
        return await multimedia_service.get_all_multimedia()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@multimedia_router.get("/{id}", response_model=Response[MultimediaDomain], summary="Get multimedia entry by ID")
async def get_multimedia_by_id(
    id: int,
    multimedia_service: IMultimediaService = Depends(build_multimedia_service)):
    """
    Retrieves a specific multimedia resource by its ID.
    """
    try:
        return await multimedia_service.get_multimedia_by_id(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@multimedia_router.put("/{id}", response_model=Response[None], summary="Update multimedia entry")
async def update_multimedia(
    id: int,
    multimedia: MultimediaDTO,
    multimedia_service: IMultimediaService = Depends(build_multimedia_service)):
    """
    Updates a multimedia resource by its ID.
    """
    try:
        return await multimedia_service.update_multimedia(id, multimedia)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@multimedia_router.delete("/{id}", response_model=Response[None], summary="Delete multimedia entry")
async def delete_multimedia(
    id: int,
    multimedia_service: IMultimediaService = Depends(build_multimedia_service)):
    """
    Deletes a multimedia resource by its ID.
    """
    try:
        return await multimedia_service.delete_multimedia(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
