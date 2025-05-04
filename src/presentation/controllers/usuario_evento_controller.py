from fastapi import APIRouter, Depends, HTTPException, status
from src.core.abstractions.services.usuario_evento_service_abstract import IUsuarioEventoService
from src.core.dependency_injection.dependency_injection import build_usuario_evento_service
from src.presentation.dto.usuario_evento_dto import UsuarioEventoDTO, UpdateAsistioUsuarioEventoDTO
from src.core.models.usuario_evento_domain import UsuarioEventoDomain
from src.resources.responses.response import Response


usuario_evento_router = APIRouter(prefix="/api/v1/usuario_evento", tags=["usuario_evento"])

@usuario_evento_router.post(
    "",
    summary="Register usuario_evento",
    description="Creates a new usuario_evento in the system.",
    response_model=Response[None]
)
async def register(
    usuario_evento_data: UsuarioEventoDTO,
    usuario_evento_service: IUsuarioEventoService = Depends(build_usuario_evento_service)
):
    try:
        return await usuario_evento_service.create_usuario_evento(usuario_evento_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@usuario_evento_router.get(
    "",
    summary="Get all usuario_eventos",
    description="Returns a list of all registered usuario_eventos.",
    response_model=Response[list[UsuarioEventoDomain]]
)
async def get_usuario_eventos(
    usuario_evento_service: IUsuarioEventoService = Depends(build_usuario_evento_service)
):
    try:
        return await usuario_evento_service.get_all_usuario_eventos()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@usuario_evento_router.get(
    "/usuario/{usuarioId}",
    summary="Get usuario_evento by ID user",
    description="Returns a single usuario_evento based on the given ID.",
    response_model=Response[list[UsuarioEventoDomain]]
)
async def get_usuario_evento_by_id_usuario(
    usuario_eventoId: int,
    usuario_evento_service: IUsuarioEventoService = Depends(build_usuario_evento_service)
):
    try:
        return await usuario_evento_service.get_usuario_evento_by_id_usuario(usuario_eventoId)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@usuario_evento_router.get(
    "/evento/{eventoId}",
    summary="Get usuario_evento by ID evento",
    description="Returns a single usuario_evento based on the given ID.",
    response_model=Response[list[UsuarioEventoDomain]]
)
async def get_usuario_evento_by_id_evento(
    eventoId: int,
    usuario_evento_service: IUsuarioEventoService = Depends(build_usuario_evento_service)
):
    try:
        return await usuario_evento_service.get_usuario_evento_by_id_evento(eventoId)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    

@usuario_evento_router.put(
    "/{usuario_eventoId}",
    summary="Update asistio usuario_evento",
    description="Updates asistio usuario_evento for the specified usuario_evento ID.",
    response_model=Response[None]
)
async def update_usuario_evento(
    usuario_eventoId: int,
    update_data: UpdateAsistioUsuarioEventoDTO,
    usuario_evento_service: IUsuarioEventoService = Depends(build_usuario_evento_service)
):
    try:
        return await usuario_evento_service.update_asistio_usuario_evento(usuario_eventoId, update_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@usuario_evento_router.delete(
    "/{usuario_eventoId}",
    summary="Delete usuario_evento",
    description="Deletes a usuario_evento based on the given ID.",
    response_model=Response[None]
)
async def delete_usuario_evento(
    usuario_eventoId: int,
    usuario_evento_service: IUsuarioEventoService = Depends(build_usuario_evento_service)
):
    try:
        return await usuario_evento_service.delete_usuario_evento(usuario_eventoId)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    