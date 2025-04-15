from fastapi import APIRouter, Depends, HTTPException, status, Form
from src.core.abstractions.services.ubicacion_service_abstract import IUbicacionService
from src.core.dependency_injection.dependency_injection import build_ubicacion_service
from src.presentation.dto.ubicacion_dto import UbicacionDTO
from src.presentation.mappers.ubicacion_mapper import map_ubicacion_domain_to_dto
from src.core.models.ubicacion_domain import UbicacionDomain

ubicacion_controller = APIRouter(prefix="/api/v1", tags=["ubicacion"])

@ubicacion_controller.post("/ubicacion")
async def create_ubicacion(
    ubicacion: UbicacionDTO,
    ubicacion_service: IUbicacionService = Depends(build_ubicacion_service)):
    try:
        return await ubicacion_service.create_ubicacion(ubicacion)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@ubicacion_controller.get("/ubicaciones")
async def get_ubicaciones(
    ubicacion_service: IUbicacionService = Depends(build_ubicacion_service)):
    try:
        return await ubicacion_service.get_all_ubicaciones()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@ubicacion_controller.get("/ubicacion/{id}")
async def get_ubicacion(
    id: int,
    ubicacion_service: IUbicacionService = Depends(build_ubicacion_service)):
    try:
        return await ubicacion_service.get_ubicacion_by_id(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@ubicacion_controller.get("/ubicacion/nombre/{nombre}")
async def get_ubicacion_by_name(
    nombre: str,
    ubicacion_service: IUbicacionService = Depends(build_ubicacion_service)):
    try:
        return await ubicacion_service.get_ubicacion_by_name(nombre)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@ubicacion_controller.put("/ubicacion/{id}")
async def update_ubicacion(
    id: int,
    ubicacion: UbicacionDTO,
    ubicacion_service: IUbicacionService = Depends(build_ubicacion_service)):
    try:
        return await ubicacion_service.update_ubicacion(id, ubicacion)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@ubicacion_controller.delete("/ubicacion/{id}")
async def delete_ubicacion(
    id: int,
    ubicacion_service: IUbicacionService = Depends(build_ubicacion_service)):
    try:
        return await ubicacion_service.delete_ubicacion(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

