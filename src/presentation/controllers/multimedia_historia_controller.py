from fastapi import APIRouter, Depends, HTTPException
from src.core.abstractions.services.multimedia_historia_service_abstract import IMultimediaHistoriaService
from src.core.dependency_injection.dependency_injection import build_multimedia_historia_service
from src.presentation.dto.multimedia_historia_dto import MultimediaHistoriaDTO
from src.presentation.mappers.multimedia_historia_mapper import map_multimedia_historia_domain_to_dto
from src.core.models.multimedia_historia_domain import MultimediaHistoriaDomain

multimedia_historia_controller = APIRouter(prefix="/api/v1", tags=["multimedia_historia"])


@multimedia_historia_controller.post("/multimedia_historia")
async def create_multimedia_historia(
    multimedia_historia: MultimediaHistoriaDTO,
    multimedia_historia_service: IMultimediaHistoriaService = Depends(build_multimedia_historia_service)):
    try:
        return await multimedia_historia_service.create_multimedia_historia(multimedia_historia)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@multimedia_historia_controller.get("/multimedia_historia")
async def get_multimedia_historia(
    multimedia_historia_service: IMultimediaHistoriaService = Depends(build_multimedia_historia_service)):
    try:
        return await multimedia_historia_service.get_all_multimedia_historia()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@multimedia_historia_controller.get("/multimedia_historia/{id}")
async def get_multimedia_historia_by_id(
    id: int,
    multimedia_historia_service: IMultimediaHistoriaService = Depends(build_multimedia_historia_service)):
    try:
        return await multimedia_historia_service.get_multimedia_historia_by_id_historia(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@multimedia_historia_controller.delete("/multimedia_historia/{id}")
async def delete_multimedia_historia(
    id: int,
    multimedia_historia_service: IMultimediaHistoriaService = Depends(build_multimedia_historia_service)):
    try:
        return await multimedia_historia_service.delete_multimedia_historia(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
