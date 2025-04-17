from fastapi import APIRouter, Depends, HTTPException
from src.core.abstractions.services.multimedia_historia_service_abstract import IMultimediaHistoriaService
from src.core.dependency_injection.dependency_injection import build_multimedia_historia_service
from src.presentation.dto.multimedia_historia_dto import MultimediaHistoriaDTO, MultimediaDatosHistoriaDTO
from src.presentation.responses.base_response import Response

multimedia_historia_router = APIRouter(
    prefix="/api/v1/multimedia_historia", 
    tags=["multimedia_historia"]
)

@multimedia_historia_router.post("", response_model=Response[None], summary="Create multimedia entry for history")
async def create_multimedia_history(
    multimedia_historia: MultimediaHistoriaDTO,
    multimedia_historia_service: IMultimediaHistoriaService = Depends(build_multimedia_historia_service)):
    """
    Creates a new multimedia entry associated with a historical record.
    """
    try:
        return await multimedia_historia_service.create_multimedia_historia(multimedia_historia)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@multimedia_historia_router.get("", response_model=Response[list[MultimediaDatosHistoriaDTO]], summary="Get all multimedia for history")
async def get_all_multimedia_history(
    multimedia_historia_service: IMultimediaHistoriaService = Depends(build_multimedia_historia_service)):
    """
    Retrieves all multimedia entries related to historical content.
    """
    try:
        return await multimedia_historia_service.get_all_multimedia_historia()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@multimedia_historia_router.get("/ByHistoriaId/{id}", response_model=Response[list[MultimediaDatosHistoriaDTO]], summary="Get multimedia by history ID")
async def get_multimedia_history_by_id(
    id: int,
    multimedia_historia_service: IMultimediaHistoriaService = Depends(build_multimedia_historia_service)):
    """
    Retrieves multimedia entries associated with a specific history entry by its ID.
    """
    try:
        return await multimedia_historia_service.get_multimedia_historia_by_id_historia(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@multimedia_historia_router.delete("/{id}", response_model=Response[None], summary="Delete multimedia entry by ID")
async def delete_multimedia_history(
    id: int,
    multimedia_historia_service: IMultimediaHistoriaService = Depends(build_multimedia_historia_service)):
    """
    Deletes a multimedia entry associated with a historical record by its ID.
    """
    try:
        return await multimedia_historia_service.delete_multimedia_historia(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
