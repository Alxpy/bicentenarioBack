from fastapi import APIRouter, Depends, HTTPException
from src.core.abstractions.services.comentario_evento_service_abstract import IComentarioEventoService
from src.core.dependency_injection.dependency_injection import build_comentario_evento_service
from src.presentation.dto.comentario_evento_dto import ComentarioEventoDTO, ComentarioDatosEventoDTO
from src.presentation.responses.base_response import Response

comentario_evento_router = APIRouter(
    prefix="/api/v1/comentario_evento",
    tags=["comentario_evento"]
)

@comentario_evento_router.post("", response_model=Response[ComentarioDatosEventoDTO], summary="Create comment for event")
async def create_comentario_evento(
    comentario_evento: ComentarioEventoDTO,
    comentario_evento_service: IComentarioEventoService = Depends(build_comentario_evento_service)):
    """
    Creates a new comment associated with an event.
    """
    try:
        return await comentario_evento_service.create_comentario_evento(comentario_evento)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@comentario_evento_router.get("", response_model=Response[list[ComentarioDatosEventoDTO]], summary="Get all comments for event")
async def get_all_comentario_evento(
    comentario_evento_service: IComentarioEventoService = Depends(build_comentario_evento_service)):
    """
    Retrieves all comments related to events.
    """
    try:
        return await comentario_evento_service.get_all_comentario_evento()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@comentario_evento_router.get("/byEventoId/{id}", response_model=Response[list[ComentarioDatosEventoDTO]], summary="Get comments by event ID")
async def get_comentario_evento_by_id(
    id: int,
    comentario_evento_service: IComentarioEventoService = Depends(build_comentario_evento_service)):
    """
    Retrieves all comments associated with a specific event by its ID.
    """
    try:
        return await comentario_evento_service.get_comentario_evento_by_id_evento(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@comentario_evento_router.delete("/{id}", response_model=Response[ComentarioDatosEventoDTO], summary="Delete comment entry by ID")
async def delete_comentario_evento(
    id: int,
    comentario_evento_service: IComentarioEventoService = Depends(build_comentario_evento_service)):
    """
    Deletes a comment entry by its ID.
    """
    try:
        return await comentario_evento_service.delete_comentario_evento(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    








