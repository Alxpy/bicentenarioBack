from fastapi import APIRouter, Depends, HTTPException, status, Form
from src.core.abstractions.services.presidente_service_abstract import IPresidenteService
from src.core.dependency_injection.dependency_injection import build_presidente_service
from src.presentation.dto.presidente_dto import *
from src.presentation.mappers.presidente_mapper import map_presidente_domain_to_dto
from src.core.models.presidente_domain import PresidenteDomain


presidente_controller = APIRouter(prefix="/api/v1", tags=["presidente"])

@presidente_controller.post("/presidente")
async def create_presidente(
    presidente: PresidenteDTO,
    presidente_service: IPresidenteService = Depends(build_presidente_service)):
    try:
        return await presidente_service.create_presidente(presidente)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@presidente_controller.get("/presidentes")
async def get_presidentes(
    presidente_service: IPresidenteService = Depends(build_presidente_service)):
    try:
        return await presidente_service.get_all_presidentes()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@presidente_controller.get("/presidente/{id}")
async def get_presidente(
    id: int,
    presidente_service: IPresidenteService = Depends(build_presidente_service)):
    try:
        return await presidente_service.get_presidente_by_id(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@presidente_controller.get("/presidente/nombre/{nombre}")
async def get_presidente_by_nombre(
    nombre: str,
    presidente_service: IPresidenteService = Depends(build_presidente_service)):
    try:
        return await presidente_service.get_presidente_by_nombre(nombre)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@presidente_controller.put("/presidente/{id}")
async def update_presidente(
    id: int,
    presidente: PresidenteDTO,
    presidente_service: IPresidenteService = Depends(build_presidente_service)):
    try:
        return await presidente_service.update_presidente(id, presidente)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@presidente_controller.delete("/presidente/{id}")
async def delete_presidente(
    id: int,
    presidente_service: IPresidenteService = Depends(build_presidente_service)):
    try:
        return await presidente_service.delete_presidente(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
