from fastapi import APIRouter, Depends, HTTPException, status, Form
from src.core.abstractions.services.cultura_service_abstract import ICulturaService
from src.core.dependency_injection.dependency_injection import build_cultura_service
from src.presentation.dto.cultura_dto import CulturaDTO
from src.presentation.mappers.cultura_mapper import map_cultura_domain_to_dto
from src.core.models.cultura_domain import CulturaDomain

cultura_controller = APIRouter(prefix="/api/v1", tags=["cultura"])

@cultura_controller.post("/cultura")
async def create_cultura(
    cultura: CulturaDTO,
    cultura_service: ICulturaService = Depends(build_cultura_service)):
    try:
        return await cultura_service.create_cultura(cultura)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@cultura_controller.get("/culturas")
async def get_culturas(
    cultura_service: ICulturaService = Depends(build_cultura_service)):
    try:
        return await cultura_service.get_all_culturas()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@cultura_controller.get("/cultura/{id}")
async def get_cultura(
    id: int,
    cultura_service: ICulturaService = Depends(build_cultura_service)):
    try:
        return await cultura_service.get_cultura_by_id(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@cultura_controller.get("/cultura/nombre/{nombre}")
async def get_cultura_by_nombre(
    nombre: str,
    cultura_service: ICulturaService = Depends(build_cultura_service)):
    try:
        return await cultura_service.get_cultura_by_nombre(nombre)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@cultura_controller.get("/cultura/ubicacion/{ubicacion}")
async def get_cultura_by_ubicacion(
    ubicacion: str,
    cultura_service: ICulturaService = Depends(build_cultura_service)):
    try:
        return await cultura_service.get_cultura_by_ubicacion(ubicacion)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@cultura_controller.put("/cultura/{id}")
async def update_cultura(
    id: int,
    cultura: CulturaDTO,
    cultura_service: ICulturaService = Depends(build_cultura_service)):
    try:
        return await cultura_service.update_cultura(id, cultura)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@cultura_controller.delete("/cultura/{id}")
async def delete_cultura(
    id: int,
    cultura_service: ICulturaService = Depends(build_cultura_service)):
    try:
        return await cultura_service.delete_cultura(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
