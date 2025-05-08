from fastapi import APIRouter, Depends, HTTPException, status
from src.core.abstractions.services.usuario_rol_service_abstract import IUsuarioRolService
from src.core.dependency_injection.dependency_injection import build_usuario_rol_service
from src.presentation.dto.usuario_rol_dto import UsuarioRolDTO,UsuarioRolDataDTO
from src.core.models.usuario_rol_domain import UsuarioRolDomain
from src.resources.responses.response import Response


usuario_rol_router = APIRouter(prefix="/api/v1/usuario_rol", tags=["usuario_rol"])

@usuario_rol_router.post(
    "",
    summary="Register usuario_rol",
    description="Creates a new usuario_rol in the system.",
    response_model=Response[None]
)
async def register(
    usuario_rol_data: UsuarioRolDTO,
    usuario_rol_service: IUsuarioRolService = Depends(build_usuario_rol_service)
):
    try:
        return await usuario_rol_service.create_usuario_rol(usuario_rol_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@usuario_rol_router.get(
    "",
    summary="Get all usuario_roles",
    description="Returns a list of all registered usuario_roles.",
    response_model=Response[list[UsuarioRolDataDTO]]
)
async def get_usuario_roles(
    usuario_rol_service: IUsuarioRolService = Depends(build_usuario_rol_service)
):
    try:
        return await usuario_rol_service.get_all_usuario_roles()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@usuario_rol_router.get(
    "/{usuario_rol_Id}",
    summary="Get usuario_rol by ID",
    description="Returns a single usuario_rol based on the given ID.",
    response_model=Response[list[UsuarioRolDataDTO]]
)
async def get_usuario_rol_by_id_rol(
    usuario_rol_Id: int,
    usuario_rol_service: IUsuarioRolService = Depends(build_usuario_rol_service)
):
    try:
        return await usuario_rol_service.get_usuario_rol_by_id_rol(usuario_rol_Id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@usuario_rol_router.delete(
    "/{usuario_rol_Id}",
    summary="Delete usuario_rol",
    description="Deletes a usuario_rol based on the given ID.",
    response_model=Response[None]
)
async def delete_usuario_rol(
    usuario_rol_Id: int,
    usuario_rol_service: IUsuarioRolService = Depends(build_usuario_rol_service)
):
    try:
        return await usuario_rol_service.delete_usuario_rol(usuario_rol_Id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


