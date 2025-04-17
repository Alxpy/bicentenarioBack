from fastapi import APIRouter, Depends, HTTPException
from src.core.abstractions.services.multimedia_cultura_service_abstract import IMultimediaCulturaService
from src.core.dependency_injection.dependency_injection import build_multimedia_cultura_service
from src.presentation.dto.multimedia_cultura_dto import MultimediaCulturaDTO
from src.presentation.mappers.multimedia_cultura_mapper import map_multimedia_cultura_domain_to_dto
from src.core.models.multimedia_cultura_domain import MultimediaCulturaDomain

multimedia_cultura_controller = APIRouter(prefix="/api/v1", tags=["multimedia_cultura"])

@multimedia_cultura_controller.post("/multimedia_cultura")
async def create_multimedia_cultura(
    multimedia_cultura: MultimediaCulturaDTO,
    multimedia_cultura_service: IMultimediaCulturaService = Depends(build_multimedia_cultura_service)):
    try:
        return await multimedia_cultura_service.create_multimedia_cultura(multimedia_cultura)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@multimedia_cultura_controller.get("/multimedia_cultura")
async def get_multimedia_cultura(
    multimedia_cultura_service: IMultimediaCulturaService = Depends(build_multimedia_cultura_service)):
    try:
        return await multimedia_cultura_service.get_all_multimedia_cultura()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@multimedia_cultura_controller.get("/multimedia_cultura/{id}")
async def get_multimedia_cultura_by_id(
    id: int,
    multimedia_cultura_service: IMultimediaCulturaService = Depends(build_multimedia_cultura_service)):
    try:
        return await multimedia_cultura_service.get_multimedia_cultura_by_id_cultura(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@multimedia_cultura_controller.delete("/multimedia_cultura/{id}")
async def delete_multimedia_cultura(
    id: int,
    multimedia_cultura_service: IMultimediaCulturaService = Depends(build_multimedia_cultura_service)):
    try:
        return await multimedia_cultura_service.delete_multimedia_cultura(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
