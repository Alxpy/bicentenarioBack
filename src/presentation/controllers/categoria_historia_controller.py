from fastapi import APIRouter, Depends, HTTPException
from src.core.abstractions.services.categoria_historia_service_abstract import ICategoriaHistoriaService
from src.core.dependency_injection.dependency_injection import build_categoria_historia_service
from src.presentation.dto.categoria_historia_dto import CategoriaHistoriaDTO
from src.presentation.responses.base_response import Response
from src.core.models.categoria_historia_domain import CategoriaHistoriaDomain

categoria_historia_controller = APIRouter(
    prefix="/api/v1/categories_history",
    tags=["categoria_historia"]
)

@categoria_historia_controller.post("", response_model=Response[None])
async def create_categoria_historia(
    categoria_historia: CategoriaHistoriaDTO,
    categoria_historia_service: ICategoriaHistoriaService = Depends(build_categoria_historia_service)):
    try:
        return await categoria_historia_service.create_categoria_historia(categoria_historia)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@categoria_historia_controller.get("", response_model=Response[list[CategoriaHistoriaDomain]])
async def get_categoria_historia(
    categoria_historia_service: ICategoriaHistoriaService = Depends(build_categoria_historia_service)):
    try:
        return await categoria_historia_service.get_all_categorias_historia()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@categoria_historia_controller.get("/{id}", response_model=Response[CategoriaHistoriaDomain])
async def get_categoria_historia_by_id(
    id: int,
    categoria_historia_service: ICategoriaHistoriaService = Depends(build_categoria_historia_service)):
    try:
        return await categoria_historia_service.get_categoria_historia(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@categoria_historia_controller.put("/{id}", response_model=Response[None])
async def update_categoria_historia(
    id: int,
    categoria_historia_update: CategoriaHistoriaDTO,
    categoria_historia_service: ICategoriaHistoriaService = Depends(build_categoria_historia_service)):
    try:
        update_categoria_historia = CategoriaHistoriaDomain(
            nombre=categoria_historia_update.nombre,
            descripcion=categoria_historia_update.descripcion
        )
        return await categoria_historia_service.update_categoria_historia(id, update_categoria_historia)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@categoria_historia_controller.delete("/{id}", response_model=Response[None])
async def delete_categoria_historia(
    id: int,
    categoria_historia_service: ICategoriaHistoriaService = Depends(build_categoria_historia_service)):
    try:
        return await categoria_historia_service.delete_categoria_historia(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
