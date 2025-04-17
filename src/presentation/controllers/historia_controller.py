from fastapi import APIRouter, Depends, HTTPException, status, Form
from src.core.abstractions.services.historia_service_abstract import IHistoriaService
from src.core.dependency_injection.dependency_injection import build_historia_service
from src.presentation.dto.historia_dto import *
from src.presentation.mappers.historia_mapper import map_historia_domain_to_dto
from src.core.models.historia_domain import HistoriaDomain

historia_controller = APIRouter(prefix="/api/v1", tags=["historia"])

@historia_controller.post("/historia")
async def create_historia(
    historia: HistoriaPostDTO,
    historia_service: IHistoriaService = Depends(build_historia_service)):
    try:
        return await historia_service.create_historia(historia)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@historia_controller.get("/historias")
async def get_historias(
    historia_service: IHistoriaService = Depends(build_historia_service)):
    try:
        return await historia_service.get_all_historia()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@historia_controller.get("/historia/{id}")
async def get_historia(
    id: int,
    historia_service: IHistoriaService = Depends(build_historia_service)):
    try:
        return await historia_service.get_historia_by_id(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@historia_controller.get("/historia/titulo/{titulo}")
async def get_historia_by_titulo(
    titulo: str,
    historia_service: IHistoriaService = Depends(build_historia_service)):
    try:
        return await historia_service.get_historia_by_titulo(titulo)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@historia_controller.get("/historia/ubicacion/{ubicacion}")
async def get_historia_by_ubicacion(
    ubicacion: str,
    historia_service: IHistoriaService = Depends(build_historia_service)):
    try:
        return await historia_service.get_historia_by_ubicacion(ubicacion)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@historia_controller.get("/historia/categoria/{categoria}")
async def get_historia_by_categoria(
    categoria: str,
    historia_service: IHistoriaService = Depends(build_historia_service)):
    try:
        return await historia_service.get_historia_by_categoria(categoria)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@historia_controller.put("/historia/{id}")
async def update_historia(
    id: int,
    historia: HistoriaUpdateDTO,
    historia_service: IHistoriaService = Depends(build_historia_service)):
    try:
        return await historia_service.update_historia(id, historia)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@historia_controller.delete("/historia/{id}")
async def delete_historia(
    id: int,
    historia_service: IHistoriaService = Depends(build_historia_service)):
    try:
        return await historia_service.delete_historia(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))