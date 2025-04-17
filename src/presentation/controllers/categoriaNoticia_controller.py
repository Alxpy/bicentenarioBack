from fastapi import APIRouter, Depends, HTTPException
from src.core.abstractions.services.categoriaNoticia_service_abstract import ICategoriaNoticiaService
from src.core.dependency_injection.dependency_injection import build_categoriaNoticia_service
from src.presentation.dto.categoriaNoticia_dto import CategoriaNoticiaDTO
from src.core.models.categoriaNoticia_domain import CategoriaNoticiaDomain
from src.presentation.responses.base_response import Response

category_controller = APIRouter(prefix="/api/v1/categories", tags=["categories"])

@category_controller.post("", response_model=Response[None])
async def create_category(
    category_dto: CategoriaNoticiaDTO,
    category_service: ICategoriaNoticiaService = Depends(build_categoriaNoticia_service)
):
    try:
        return await category_service.create_categoria_noticia(category_dto)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@category_controller.get("", response_model=Response[list[CategoriaNoticiaDomain]])
async def get_all_categories(
    category_service: ICategoriaNoticiaService = Depends(build_categoriaNoticia_service)
):
    try:
        return await category_service.get_all_categorias_noticia()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@category_controller.get("/{id}", response_model=Response[CategoriaNoticiaDomain])
async def get_category_by_id(
    id: int,
    category_service: ICategoriaNoticiaService = Depends(build_categoriaNoticia_service)
):
    try:
        return await category_service.get_categoria_noticia(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@category_controller.put("/{id}", response_model=Response[None])
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


@category_controller.delete("/{id}", response_model=Response[None])
async def delete_category(
    id: int,
    category_service: ICategoriaNoticiaService = Depends(build_categoriaNoticia_service)
):
    try:
        return await category_service.delete_categoria_noticia(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
