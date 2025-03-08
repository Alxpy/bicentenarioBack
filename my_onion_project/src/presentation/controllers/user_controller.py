from fastapi import APIRouter, Depends, HTTPException, status,Form
from src.core.abstractions.services.user_service_abstract import IUsuarioService
from src.core.dependency_injection.dependency_injection import build_usuario_service
from src.presentation.dto.user_dto import UsuarioDTO
from src.presentation.mappers.user_mapper import map_usuario_domain_to_dto
from src.core.models.user_domain import UsuarioDomain

user_controller = APIRouter(prefix="/api/v1", tags=["user"])

@user_controller.get("/user",response_model=list[UsuarioDomain])
async def list_usuarios(usuario_service: IUsuarioService = Depends(build_usuario_service)):
    return await usuario_service.get_all_usuarios()

@user_controller.get("/user/{id}", response_model=UsuarioDomain)
async def retrieve_usuario(id: int, usuario_service: IUsuarioService = Depends(build_usuario_service)):
    usuario = await usuario_service.get_usuario(id)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Usuario con {id} no encontrado")
    return usuario

@user_controller.post("/user", response_model=UsuarioDomain, status_code=status.HTTP_201_CREATED)
async def create_usuario(usuario: UsuarioDTO, usuario_service: IUsuarioService = Depends(build_usuario_service)):
    usuario_domain = map_usuario_domain_to_dto(usuario)
    return await usuario_service.create_usuario(usuario_domain)

@user_controller.post("/login(correo)",response_model=UsuarioDomain)
async def login_usuario(
    correo: str = Form(...),
    contrasena: str = Form(...),
    usuario_service: IUsuarioService = Depends(build_usuario_service)
):
    usuario=await usuario_service.get_by_correo(correo)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con correo{correo}no encontrado"
        )
    if usuario.contrasena != contrasena:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Contraseña incorrecta"
        )
    return usuario

