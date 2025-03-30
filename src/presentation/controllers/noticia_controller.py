from fastapi import APIRouter, Depends, HTTPException, status, Form
from src.core.abstractions.services.noticia_service_abstract import INoticiaService
from src.core.dependency_injection.dependency_injection import build_noticia_service
from src.presentation.dto.noticia_dto import NoticiaDTO
from src.presentation.mappers.noticia_mapper import map_noticia_domain_to_dto
from src.core.models.noticia_domain import NoticiaDomain

noticia_controller = APIRouter(prefix="/api/v1", tags=["noticia"])

@noticia_controller.post("/noticia")
async def create_noticia(
    noticia: NoticiaDTO,
    noticia_service: INoticiaService = Depends(build_noticia_service)):
    try:
        return await noticia_service.create_noticia(noticia)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@noticia_controller.get("/noticias")
async def get_noticias(
    noticia_service: INoticiaService = Depends(build_noticia_service)):
    try:
        return await noticia_service.get_all_noticias()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@noticia_controller.get("/noticia/{id}")
async def get_noticia(
    id: int,
    noticia_service: INoticiaService = Depends(build_noticia_service)):
    try:
        return await noticia_service.get_noticia_by_id(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@noticia_controller.get("/noticia/{fecha_publicacion}")
async def get_noticia(
    fecha_publicacion: str,
    noticia_service: INoticiaService = Depends(build_noticia_service)):
    try:
        return await noticia_service.get_noticia_by_fecha(fecha_publicacion)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@noticia_controller.get("/noticia/categoria/{nomCategoria}")
async def get_noticia_by_categoria(
    nomCategoria: str,
    noticia_service: INoticiaService = Depends(build_noticia_service)):
    try:
        return await noticia_service.get_noticia_by_categoria(nomCategoria)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@noticia_controller.get("/noticia/titulo/{titulo}")
async def get_noticia_by_title(
    titulo: str,
    noticia_service: INoticiaService = Depends(build_noticia_service)):
    try:
        return await noticia_service.get_noticia_by_title(titulo)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@noticia_controller.put("/noticia/{id}")
async def update_noticia(
    id: int,
    noticiaUpdate: NoticiaDTO,
    noticia_service: INoticiaService = Depends(build_noticia_service)):
    try:        
        noticia: NoticiaDomain = await noticia_service.get_noticia_by_id(id)
        updateNoticia = NoticiaDomain(
            titulo=noticiaUpdate.titulo,
            resumen=noticiaUpdate.resumen,
            contenido=noticiaUpdate.contenido,
            imagen=noticiaUpdate.imagen,
            idCategoria=noticiaUpdate.idCategoria,            
        )
        return await noticia_service.update_noticia(id, updateNoticia)
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@noticia_controller.delete("/noticia/{id}")
async def delete_noticia(
    id: int,
    noticia_service: INoticiaService = Depends(build_noticia_service)):
    try:
        return await noticia_service.delete_noticia(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))