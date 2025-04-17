from fastapi import APIRouter, Depends, HTTPException
from src.core.abstractions.services.noticia_service_abstract import INoticiaService
from src.core.dependency_injection.dependency_injection import build_noticia_service
from src.presentation.dto.noticia_dto import NoticiaDTO, NoticiaUpdateDTO
from src.core.models.noticia_domain import NoticiaDomain
from src.presentation.responses.base_response import Response

news_router = APIRouter(prefix="/api/v1/news", tags=["news"])

@news_router.post("", response_model=Response[None], summary="Create a news entry")
async def create_news(
    noticia: NoticiaDTO,
    noticia_service: INoticiaService = Depends(build_noticia_service)
):
    """
    Creates a new news article.
    """
    try:
        return await noticia_service.create_noticia(noticia)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@news_router.get("", response_model=Response[list[NoticiaDomain]], summary="Get all news")
async def get_all_news(
    noticia_service: INoticiaService = Depends(build_noticia_service)
):
    """
    Retrieves all news articles.
    """
    try:
        return await noticia_service.get_all_noticias()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@news_router.get("/{id}", response_model=Response[NoticiaDomain], summary="Get news by ID")
async def get_news_by_id(
    id: int,
    noticia_service: INoticiaService = Depends(build_noticia_service)
):
    """
    Retrieves a news article by its ID.
    """
    try:
        return await noticia_service.get_noticia_by_id(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@news_router.get("/ByDate/{publicationDate}", response_model=Response[list[NoticiaDomain]], summary="Get news by publication date")
async def get_news_by_date(
    publicationDate: str,
    noticia_service: INoticiaService = Depends(build_noticia_service)
):
    """
    Retrieves news articles by their publication date.
    """
    try:
        return await noticia_service.get_noticia_by_fecha(publicationDate)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@news_router.get("/ByCategory/{categoryName}", response_model=Response[list[NoticiaDomain]], summary="Get news by category")
async def get_news_by_category(
    categoryName: str,
    noticia_service: INoticiaService = Depends(build_noticia_service)
):
    """
    Retrieves news articles filtered by category name.
    """
    try:
        return await noticia_service.get_noticia_by_categoria(categoryName)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@news_router.get("/ByTitle/{title}", response_model=Response[NoticiaDomain], summary="Get news by title")
async def get_news_by_title(
    title: str,
    noticia_service: INoticiaService = Depends(build_noticia_service)
):
    """
    Retrieves a news article by its title.
    """
    try:
        return await noticia_service.get_noticia_by_title(title)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@news_router.put("/{id}", response_model=Response[None], summary="Update news")
async def update_news(
    id: int,
    noticia_update: NoticiaUpdateDTO,
    noticia_service: INoticiaService = Depends(build_noticia_service)
):
    """
    Updates a news article by its ID.
    """
    try:
        noticia: NoticiaDomain = await noticia_service.get_noticia_by_id(id)
        updated_noticia = NoticiaDomain(
            titulo=noticia_update.titulo,
            resumen=noticia_update.resumen,
            contenido=noticia_update.contenido,
            imagen=noticia_update.imagen,
            id_Categoria=noticia_update.id_Categoria,
            fecha_publicacion=noticia_update.fecha_publicacion,
        )
        return await noticia_service.update_noticia(id, updated_noticia)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@news_router.delete("/{id}", response_model=Response[None], summary="Delete news")
async def delete_news(
    id: int,
    noticia_service: INoticiaService = Depends(build_noticia_service)
):
    """
    Deletes a news article by its ID.
    """
    try:
        return await noticia_service.delete_noticia(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
