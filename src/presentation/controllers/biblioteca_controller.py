from fastapi import APIRouter, Depends, HTTPException, status, Form
from src.core.abstractions.services.biblioteca_service_abstract import IBibliotecaService
from src.core.dependency_injection.dependency_injection import build_biblioteca_service
from src.presentation.dto.biblioteca_dto import *
from src.presentation.mappers.biblioteca_mapper import map_biblioteca_domain_to_dto
from src.core.models.biblioteca_domain import BibliotecaDomain

biblioteca_controller = APIRouter(prefix="/api/v1", tags=["biblioteca"])

@biblioteca_controller.post("/biblioteca")
async def create_biblioteca(
    biblioteca: BibliotecaDTO,
    biblioteca_service: IBibliotecaService = Depends(build_biblioteca_service)):
    try:
        return await biblioteca_service.create_biblioteca(biblioteca)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@biblioteca_controller.get("/bibliotecas")
async def get_bibliotecas(
    biblioteca_service: IBibliotecaService = Depends(build_biblioteca_service)):
    try:
        return await biblioteca_service.get_all_bibliotecas()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@biblioteca_controller.get("/biblioteca/ID/{id}")
async def get_biblioteca(
    id: int,
    biblioteca_service: IBibliotecaService = Depends(build_biblioteca_service)):
    try:
        return await biblioteca_service.get_biblioteca_by_id(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@biblioteca_controller.get("/biblioteca/categoria/{nomCategoria}")
async def get_biblioteca_by_categoria(
    nomCategoria: str,
    biblioteca_service: IBibliotecaService = Depends(build_biblioteca_service)):
    try:
        return await biblioteca_service.get_biblioteca_by_categoria(nomCategoria)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@biblioteca_controller.get("/biblioteca/titulo/{titulo}")
async def get_biblioteca_by_title(
    titulo: str,
    biblioteca_service: IBibliotecaService = Depends(build_biblioteca_service)):
    try:
        return await biblioteca_service.get_biblioteca_by_title(titulo)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@biblioteca_controller.get("/biblioteca/autor/{autor}")
async def get_biblioteca_by_autor(
    autor: str,
    biblioteca_service: IBibliotecaService = Depends(build_biblioteca_service)):
    try:
        return await biblioteca_service.get_biblioteca_by_autor(autor)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@biblioteca_controller.get("/biblioteca/fecha/{fecha_publicacion}")
async def get_biblioteca_by_fecha(
    fecha_publicacion: str,
    biblioteca_service: IBibliotecaService = Depends(build_biblioteca_service)):
    try:
        return await biblioteca_service.get_biblioteca_by_fecha(fecha_publicacion)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@biblioteca_controller.put("/biblioteca/{id}")
async def update_biblioteca(
    id: int,
    bibliotecaUpdate: BibliotecaUpdateDTO,
    biblioteca_service: IBibliotecaService = Depends(build_biblioteca_service)):
    try: 
        bliblioteca:BibliotecaDomain = await biblioteca_service.get_biblioteca_by_id(id)       
        updateBibliotca=BibliotecaDomain(
            id=id,
            titulo=bibliotecaUpdate.titulo,
            autor=bibliotecaUpdate.autor,
            imagen=bibliotecaUpdate.imagen,
            fecha_publicacion=bibliotecaUpdate.fecha_publicacion,
            edicion=bibliotecaUpdate.edicion,
            id_tipo=bibliotecaUpdate.id_tipo,
            id_usuario=bliblioteca.id_usuario,
            fuente=bibliotecaUpdate.fuente,
            enlace=bibliotecaUpdate.enlace,
        )
        return await biblioteca_service.update_biblioteca(id, updateBibliotca)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@biblioteca_controller.delete("/biblioteca/{id}")
async def delete_biblioteca(
    id: int,
    biblioteca_service: IBibliotecaService = Depends(build_biblioteca_service)):
    try:
        return await biblioteca_service.delete_biblioteca(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    