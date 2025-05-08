from fastapi import APIRouter, Depends, HTTPException
from src.core.abstractions.services.comentario_service_abstract import IComentarioService
from src.core.dependency_injection.dependency_injection import build_comentario_service
from src.presentation.dto.comentario_dto import ComentarioDTO, ComentarioUpdateDTO,ComentarioResponseCreate
from src.presentation.responses.base_response import Response
from src.core.models.comentario_domain import ComentarioDomain
from src.presentation.dto.comentario_evento_dto import ComentarioDatosEventoDTO

comentario_router = APIRouter(
    prefix="/api/v1/comentario",
    tags=["comentario"]
)

@comentario_router.post("", response_model=Response[ComentarioResponseCreate], summary="Create a new comentario entry")
async def create_comentario(
    comentario: ComentarioDTO,
    comentario_service: IComentarioService = Depends(build_comentario_service)):
    """
    Creates a new comentario resource.
    """
    try:
        return await comentario_service.create_comentario(comentario)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@comentario_router.get("", response_model=Response[list], summary="Get all comentario entries")
async def get_all_comentarios(
    comentario_service: IComentarioService = Depends(build_comentario_service)):
    """
    Retrieves all comentario resources.
    """
    try:
        return await comentario_service.get_all_comentarios()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@comentario_router.get("/{id}", response_model=Response[ComentarioDomain], summary="Get comentario entry by ID")
async def get_comentario_by_id(
    id: int,
    comentario_service: IComentarioService = Depends(build_comentario_service)):
    """
    Retrieves a specific comentario resource by its ID.
    """
    try:
        return await comentario_service.get_comentario_by_id(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@comentario_router.put("/{id}", response_model=Response[None], summary="Update comentario entry")
async def update_comentario(
    id: int,
    comentario: ComentarioUpdateDTO,
    comentario_service: IComentarioService = Depends(build_comentario_service)):
    """
    Updates a comentario resource by its ID.
    """
    try:
        return await comentario_service.update_comentario(id, comentario)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@comentario_router.delete("/{id}", response_model=Response[None], summary="Delete comentario entry")
async def delete_comentario(
    id: int,
    comentario_service: IComentarioService = Depends(build_comentario_service)):
    """
    Deletes a comentario resource by its ID.
    """
    try:
        return await comentario_service.delete_comentario(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 
    