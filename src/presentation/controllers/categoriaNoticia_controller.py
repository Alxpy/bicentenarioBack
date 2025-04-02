from fastapi import APIRouter, Depends, HTTPException, status, Form
from src.core.abstractions.services.categoriaNoticia_service_abstract import ICategoriaNoticiaService
from src.core.dependency_injection.dependency_injection import build_categoriaNoticia_service
from src.presentation.dto.categoriaNoticia_dto import CategoriaNoticiaDTO
from src.presentation.mappers.categoriaNoticia_mapper import map_categoriaNoticia_domain_to_dto
from src.core.models.categoriaNoticia_domain import CategoriaNoticiaDomain

categoriaNoticia_controller = APIRouter(prefix="/api/v1", tags=["categoriaNoticia"])

@categoriaNoticia_controller.post("/categoriaNoticia")
async def create_categoriaNoticia(
    categoriaNoticia: CategoriaNoticiaDTO,
    categoriaNoticia_service: ICategoriaNoticiaService = Depends(build_categoriaNoticia_service)):
    try:
        return await categoriaNoticia_service.create_categoria_noticia(categoriaNoticia)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@categoriaNoticia_controller.get("/categoriaNoticias")
async def get_categoriaNoticias(
    categoriaNoticia_service: ICategoriaNoticiaService = Depends(build_categoriaNoticia_service)):
    try:
        return await categoriaNoticia_service.get_all_categorias_noticia()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@categoriaNoticia_controller.get("/categoriaNoticia/{id}")
async def get_categoriaNoticia(
    id: int,
    categoriaNoticia_service: ICategoriaNoticiaService = Depends(build_categoriaNoticia_service)):
    try:
        return await categoriaNoticia_service.get_categoria_noticia(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@categoriaNoticia_controller.put("/categoriaNoticia/{id}")
async def update_categoriaNoticia(
    id: int,
    categoriaNoticiaUpdate: CategoriaNoticiaDTO,
    categoriaNoticia_service: ICategoriaNoticiaService = Depends(build_categoriaNoticia_service)):
    try:
        updateCategoriaNoticia = CategoriaNoticiaDomain(
            nombre_categoria=categoriaNoticiaUpdate.nombre_categoria,
        )
        return await categoriaNoticia_service.update_categoria_noticia(id, updateCategoriaNoticia)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@categoriaNoticia_controller.delete("/categoriaNoticia/{id}")
async def delete_categoriaNoticia(
    id: int,
    categoriaNoticia_service: ICategoriaNoticiaService = Depends(build_categoriaNoticia_service)):
    try:
        return await categoriaNoticia_service.delete_categoria_noticia(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))