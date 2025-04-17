from fastapi import APIRouter, Depends, HTTPException
from src.core.abstractions.services.categoriaNoticia_service_abstract import ICategoriaNoticiaService
from src.core.dependency_injection.dependency_injection import build_categoriaNoticia_service
from src.presentation.dto.categoriaNoticia_dto import CategoriaNoticiaDTO
from src.core.models.categoriaNoticia_domain import CategoriaNoticiaDomain
from src.presentation.responses.base_response import Response

category_router = APIRouter(
    prefix="/api/v1/categories",
    tags=["News Categories"],
    responses={404: {"description": "Not found"}}
)

@category_router.post(
    "",
    response_model=Response[None],
    summary="Create a news category",
    description="Adds a new category for news classification to the system. Requires unique category name."
)
async def create_category(
    category_dto: CategoriaNoticiaDTO,
    category_service: ICategoriaNoticiaService = Depends(build_categoriaNoticia_service)
):
    try:
        return await category_service.create_categoria_noticia(category_dto)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@category_router.get(
    "",
    response_model=Response[list[CategoriaNoticiaDomain]],
    summary="List all news categories",
    description="Retrieves a complete list of all available news categories in the system."
)
async def get_all_categories(
    category_service: ICategoriaNoticiaService = Depends(build_categoriaNoticia_service)
):
    try:
        return await category_service.get_all_categorias_noticia()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@category_router.get(
    "/{id}",
    response_model=Response[CategoriaNoticiaDomain],
    summary="Get category by ID",
    description="Retrieves detailed information about a specific news category using its unique identifier."
)
async def get_category_by_id(
    id: int,
    category_service: ICategoriaNoticiaService = Depends(build_categoriaNoticia_service)
):
    try:
        return await category_service.get_categoria_noticia(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@category_router.put(
    "/{id}",
    response_model=Response[None],
    summary="Update news category",
    description="Modifies the name of an existing news category. The new name must be unique."
)
async def update_category(
    id: int,
    category_dto: CategoriaNoticiaDTO,
    category_service: ICategoriaNoticiaService = Depends(build_categoriaNoticia_service)
):
    try:
        updated_category = CategoriaNoticiaDomain(
            nombre_categoria=category_dto.nombre_categoria
        )
        return await category_service.update_categoria_noticia(id, updated_category)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@category_router.delete(
    "/{id}",
    response_model=Response[None],
    summary="Delete news category",
    description="Permanently removes a news category from the system. Note: Cannot delete categories with associated news items."
)
async def delete_category(
    id: int,
    category_service: ICategoriaNoticiaService = Depends(build_categoriaNoticia_service)
):
    try:
        return await category_service.delete_categoria_noticia(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    