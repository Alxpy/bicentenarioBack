from fastapi import APIRouter, Depends, HTTPException
from src.core.services.patrocinador_evento_service import PatrocinadorEventoService
from src.core.dependency_injection.dependency_injection import build_patrocinador_evento_service

from src.presentation.responses.base_response import Response
from src.core.models.patrocinador_evento_domain import PatrocinadorEvento
from src.presentation.dto.patrocinador_evento_dto import PatrocinadorEventoByEvento

patrocinador_evento_router = APIRouter(
    prefix="/api/v1/patrocinador_evento",
    tags=["Patrocinador Evento"],
    responses={404: {"description": "Patrocinador Evento not found"}}
)

@patrocinador_evento_router.post(
    "",
    response_model=Response[None],
    summary="Crear patrocinador evento",
    description="Crea un nuevo patrocinador evento en la base de datos."
)
async def create_patrocinador_evento(patrocinador_evento: PatrocinadorEvento, patrocinador_evento_service: PatrocinadorEventoService = Depends(build_patrocinador_evento_service)):
    try:
        return await patrocinador_evento_service.create_patrocinador_evento(patrocinador_evento)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@patrocinador_evento_router.get(
    "/evento/{id_evento}",
    response_model=Response[list[PatrocinadorEventoByEvento]],
    summary="Listar patrocinadores por evento",
    description="Obtiene una lista de todos los patrocinadores por evento."
)
async def get_patrocinador_by_evento(id_evento: int, patrocinador_evento_service: PatrocinadorEventoService = Depends(build_patrocinador_evento_service)):
    try:
        return await patrocinador_evento_service.get_patrocinador_by_evento(id_evento)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@patrocinador_evento_router.get(
    "/patrocinador/{id_patrocinador}",
    response_model=Response[list[PatrocinadorEvento]],
    summary="Listar eventos por patrocinador",
    description="Obtiene una lista de todos los eventos por patrocinador."
)
async def get_evento_by_patrocinador(id_patrocinador: int, patrocinador_evento_service: PatrocinadorEventoService = Depends(build_patrocinador_evento_service)):
    try:
        return await patrocinador_evento_service.get_evento_by_patrocinador(id_patrocinador)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    