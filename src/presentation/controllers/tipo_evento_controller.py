from fastapi import APIRouter, Depends, HTTPException
from src.core.abstractions.services.tipo_evento_abstract import ITipoEventoService
from src.core.dependency_injection.dependency_injection import build_tipo_evento_service    
from src.presentation.dto.tipo_evento_dto import TipoEventoDTO
from src.presentation.responses.base_response import Response


tipo_evento_router = APIRouter(
    prefix="/api/v1/tipo_evento",
    tags=["tipo_evento"]
)

@tipo_evento_router.post("", response_model=Response[None], summary="Create tipo_evento")
async def create_tipo_evento(
    tipo_evento: TipoEventoDTO,
    tipo_evento_service: ITipoEventoService = Depends(build_tipo_evento_service)):
    """
    Creates a new tipo_evento.
    """
    try:
        return await tipo_evento_service.create_tipo_evento(tipo_evento)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@tipo_evento_router.get("", response_model=Response[list[TipoEventoDTO]], summary="Get all tipo_eventos")
async def get_all_tipo_eventos(
    tipo_evento_service: ITipoEventoService = Depends(build_tipo_evento_service)):
    """
    Retrieves all tipo_eventos.
    """
    try:
        return await tipo_evento_service.get_all_tipo_eventos()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@tipo_evento_router.get("/byId/{id}", response_model=Response[TipoEventoDTO], summary="Get tipo_evento by ID")
async def get_tipo_evento_by_id(
    id: int,
    tipo_evento_service: ITipoEventoService = Depends(build_tipo_evento_service)):
    """
    Retrieves a tipo_evento by its ID.
    """
    try:
        return await tipo_evento_service.get_tipo_evento_by_id(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@tipo_evento_router.put("/{id}", response_model=Response[None], summary="Update tipo_evento by ID") 
async def update_tipo_evento(
    id: int,
    tipo_evento: TipoEventoDTO,
    tipo_evento_service: ITipoEventoService = Depends(build_tipo_evento_service)):
    """
    Updates a tipo_evento by its ID.
    """
    try:
        return await tipo_evento_service.update_tipo_evento(id, tipo_evento)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@tipo_evento_router.delete("/{id}", response_model=Response[None], summary="Delete tipo_evento by ID")
async def delete_tipo_evento(
    id: int,
    tipo_evento_service: ITipoEventoService = Depends(build_tipo_evento_service)):
    """
    Deletes a tipo_evento by its ID.
    """
    try:
        return await tipo_evento_service.delete_tipo_evento(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    