from fastapi import APIRouter, Depends, HTTPException
from src.core.abstractions.services.categoria_historia_service_abstract import ICategoriaHistoriaService
from src.core.dependency_injection.dependency_injection import build_categoria_historia_service
from src.presentation.dto.categoria_historia_dto import CategoriaHistoriaDTO
from src.presentation.responses.base_response import Response
from src.core.models.categoria_historia_domain import CategoriaHistoriaDomain

history_category_router = APIRouter(
    prefix="/api/v1/historyCategories",
    tags=["History Categories"],
    responses={404: {"description": "Category not found"}}
)

@history_category_router.post(
    "",
    response_model=Response[None],
    summary="Create history category",
    description="Creates a new category for historical content classification. Requires unique category name."
)
async def create_history_category(
    category: CategoriaHistoriaDTO,
    service: ICategoriaHistoriaService = Depends(build_categoria_historia_service)
):
    try:
        return await service.create_categoria_historia(category)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@history_category_router.get(
    "",
    response_model=Response[list[CategoriaHistoriaDomain]],
    summary="List all history categories",
    description="Retrieves complete list of available historical content categories."
)
async def get_all_history_categories(
    service: ICategoriaHistoriaService = Depends(build_categoria_historia_service)
):
    try:
        return await service.get_all_categorias_historia()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@history_category_router.get(
    "/{id}",
    response_model=Response[CategoriaHistoriaDomain],
    summary="Get history category details",
    description="Retrieves complete information about a specific historical content category."
)
async def get_history_category(
    id: int,
    service: ICategoriaHistoriaService = Depends(build_categoria_historia_service)
):
    try:
        return await service.get_categoria_historia(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@history_category_router.put(
    "/{id}",
    response_model=Response[None],
    summary="Update history category",
    description="Modifies the name and description of an existing historical content category."
)
async def update_history_category(
    id: int,
    category_update: CategoriaHistoriaDTO,
    service: ICategoriaHistoriaService = Depends(build_categoria_historia_service)
):
    try:
        updated_category = CategoriaHistoriaDomain(
            nombre=category_update.nombre,
            descripcion=category_update.descripcion
        )
        return await service.update_categoria_historia(id, updated_category)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@history_category_router.delete(
    "/{id}",
    response_model=Response[None],
    summary="Delete history category",
    description="Removes a historical content category. Category must not be associated with any content."
)
async def delete_history_category(
    id: int,
    service: ICategoriaHistoriaService = Depends(build_categoria_historia_service)
):
    try:
        return await service.delete_categoria_historia(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))