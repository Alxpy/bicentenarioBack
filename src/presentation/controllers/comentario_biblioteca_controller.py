from fastapi import APIRouter, Depends, HTTPException
from src.core.abstractions.services.comentario_biblioteca_service_abstract import IComentarioBibliotecaService
from src.core.dependency_injection.dependency_injection import build_comentario_biblioteca_service
from src.presentation.dto.comentario_biblioteca_dto import ComentarioBibliotecaDTO, ComentarioDatosBibliotecaDTO
from src.presentation.responses.base_response import Response

comentario_biblioteca_router = APIRouter(
    prefix="/api/v1/comentario_biblioteca",
    tags=["comentario_biblioteca"]
)

@comentario_biblioteca_router.post("", response_model=Response[ComentarioDatosBibliotecaDTO], summary="Create comment for library")
async def create_comentario_biblioteca(
    comentario_biblioteca: ComentarioBibliotecaDTO,
    comentario_biblioteca_service: IComentarioBibliotecaService = Depends(build_comentario_biblioteca_service)):
    """
    Creates a new comment associated with a library.
    """
    try:
        return await comentario_biblioteca_service.create_comentario_biblioteca(comentario_biblioteca)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@comentario_biblioteca_router.get("", response_model=Response[list[ComentarioDatosBibliotecaDTO]], summary="Get all comments for library")
async def get_all_comentario_biblioteca(
    comentario_biblioteca_service: IComentarioBibliotecaService = Depends(build_comentario_biblioteca_service)):
    """
    Retrieves all comments related to libraries.
    """
    try:
        return await comentario_biblioteca_service.get_all_comentario_biblioteca()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@comentario_biblioteca_router.get("/byBibliotecaId/{id}", response_model=Response[list[ComentarioDatosBibliotecaDTO]], summary="Get comments by library ID")
async def get_comentario_biblioteca_by_id(
    id: int,
    comentario_biblioteca_service: IComentarioBibliotecaService = Depends(build_comentario_biblioteca_service)):
    """
    Retrieves all comments associated with a specific library by its ID.
    """
    try:
        return await comentario_biblioteca_service.get_comentario_biblioteca_by_id_biblioteca(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@comentario_biblioteca_router.delete("/{id}", response_model=Response[ComentarioDatosBibliotecaDTO], summary="Delete comment entry by ID")
async def delete_comentario_biblioteca(
    id: int,
    comentario_biblioteca_service: IComentarioBibliotecaService = Depends(build_comentario_biblioteca_service)):
    """
    Deletes a comment entry by its ID.
    """
    try:
        return await comentario_biblioteca_service.delete_comentario_biblioteca(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    


