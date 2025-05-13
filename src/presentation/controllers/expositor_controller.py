from fastapi import APIRouter, Depends, HTTPException, status
from src.core.services.expositor_service import ExpositorService
from src.core.dependency_injection.dependency_injection import build_expositor_service
from src.presentation.dto.expositor_dto import ExpositorCreate
from src.core.models.expositor_domain import ExpositorDomain
from src.resources.responses.response import Response

expositor_router = APIRouter(
    prefix="/api/v1/expositor",
    tags=["expositor"]
)

@expositor_router.post("", response_model=Response[ExpositorDomain], summary="Create expositor")
async def create_expositor(expositor: ExpositorCreate, expositor_service: ExpositorService = Depends(build_expositor_service)):
    return await expositor_service.create_expositor(expositor)

@expositor_router.get("", response_model=Response[list[ExpositorDomain]], summary="Get all expositores")
async def get_all_expositores(expositor_service: ExpositorService = Depends(build_expositor_service)):
    return await expositor_service.get_all_expositores()

@expositor_router.get("/byEventoId/{id}", response_model=Response[list[ExpositorDomain]], summary="Get expositor by event ID")
async def get_expositores_by_evento_id(id: int, expositor_service: ExpositorService = Depends(build_expositor_service)):
    return await expositor_service.get_all_expositores_by_evento(id)

@expositor_router.post("/evento/{id_evento}/expositor/{id_expositor}", response_model=Response[ExpositorDomain], summary="Create expositor for event")
async def create_expositor_evento(id_evento: int, id_expositor: int, expositor_service: ExpositorService = Depends(build_expositor_service)):
    return await expositor_service.create_expositor_evento(id_evento, id_expositor)

@expositor_router.delete("/evento/{id_evento}/expositor/{id_expositor}", response_model=Response[ExpositorDomain], summary="Delete expositor for event")
async def delete_expositor_evento(id_evento: int, id_expositor: int, expositor_service: ExpositorService = Depends(build_expositor_service)):
    return await expositor_service.delete_expositor_evento(id_evento, id_expositor)