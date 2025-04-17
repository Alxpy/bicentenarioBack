from fastapi import APIRouter, Depends, HTTPException
from src.core.abstractions.services.historia_service_abstract import IHistoriaService
from src.core.dependency_injection.dependency_injection import build_historia_service
from src.presentation.dto.historia_dto import HistoriaPostDTO, HistoriaUpdateDTO
from src.presentation.responses.base_response import Response
from src.core.models.historia_domain import HistoriaDomain

historia_controller = APIRouter(
    prefix="/api/v1/history",
    tags=["historia"]
)

@historia_controller.post("", response_model=Response[None])
async def create_historia(
    historia: HistoriaPostDTO,
    historia_service: IHistoriaService = Depends(build_historia_service)):
    try:
        return await historia_service.create_historia(historia)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@historia_controller.get("", response_model=Response[list[HistoriaDomain]])
async def get_historias(
    historia_service: IHistoriaService = Depends(build_historia_service)):
    try:
        return await historia_service.get_all_historia()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@historia_controller.get("/{id}", response_model=Response[HistoriaDomain])
async def get_historia(
    id: int,
    historia_service: IHistoriaService = Depends(build_historia_service)):
    try:
        return await historia_service.get_historia_by_id(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@historia_controller.get("/titulo/{titulo}", response_model=Response[HistoriaDomain])
async def get_historia_by_titulo(
    titulo: str,
    historia_service: IHistoriaService = Depends(build_historia_service)):
    try:
        return await historia_service.get_historia_by_titulo(titulo)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@historia_controller.get("/ubicacion/{ubicacion}", response_model=Response[list[HistoriaDomain]])
async def get_historia_by_ubicacion(
    ubicacion: str,
    historia_service: IHistoriaService = Depends(build_historia_service)):
    try:
        return await historia_service.get_historia_by_ubicacion(ubicacion)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@historia_controller.get("/categoria/{categoria}", response_model=Response[list[HistoriaDomain]])
async def get_historia_by_categoria(
    categoria: str,
    historia_service: IHistoriaService = Depends(build_historia_service)):
    try:
        return await historia_service.get_historia_by_categoria(categoria)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@historia_controller.put("/{id}", response_model=Response[None])
async def update_historia(
    id: int,
    historia: HistoriaUpdateDTO,
    historia_service: IHistoriaService = Depends(build_historia_service)):
    try:
        return await historia_service.update_historia(id, historia)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@historia_controller.delete("/{id}", response_model=Response[None])
async def delete_historia(
    id: int,
    historia_service: IHistoriaService = Depends(build_historia_service)):
    try:
        return await historia_service.delete_historia(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
