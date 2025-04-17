from fastapi import APIRouter, Depends, HTTPException
from src.core.abstractions.services.presidente_service_abstract import IPresidenteService
from src.core.dependency_injection.dependency_injection import build_presidente_service
from src.presentation.dto.presidente_dto import *
from src.presentation.mappers.presidente_mapper import map_presidente_domain_to_dto
from src.core.models.presidente_domain import PresidenteDomain
from src.presentation.responses.base_response import Response

presidente_controller = APIRouter(prefix="/api/v1/president", tags=["president"])

@presidente_controller.post("", response_model=Response[None])
async def create_president(
    presidente: PresidenteDTO,
    presidente_service: IPresidenteService = Depends(build_presidente_service)):
    try:
        return await presidente_service.create_presidente(presidente)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@presidente_controller.get("/getAll", response_model=Response[list[PresidenteDomain]])
async def get_all_presidents(
    presidente_service: IPresidenteService = Depends(build_presidente_service)):
    try:
        return await presidente_service.get_all_presidentes()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@presidente_controller.get("/getById/{id}", response_model=Response[PresidenteDomain])
async def get_president_by_id(
    id: int,
    presidente_service: IPresidenteService = Depends(build_presidente_service)):
    try:
        return await presidente_service.get_presidente_by_id(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@presidente_controller.get("/getByName/{name}", response_model=Response[PresidenteDomain])
async def get_president_by_name(
    name: str,
    presidente_service: IPresidenteService = Depends(build_presidente_service)):
    try:
        return await presidente_service.get_presidente_by_nombre(name)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@presidente_controller.put("/{id}", response_model=Response[None])
async def update_president(
    id: int,
    presidente: PresidenteDTO,
    presidente_service: IPresidenteService = Depends(build_presidente_service)):
    try:
        return await presidente_service.update_presidente(id, presidente)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@presidente_controller.delete("/{id}", response_model=Response[None])
async def delete_president(
    id: int,
    presidente_service: IPresidenteService = Depends(build_presidente_service)):
    try:
        return await presidente_service.delete_presidente(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
