from fastapi import APIRouter, Depends, HTTPException, status, Form
from src.core.abstractions.services.user_service_abstract import IUsuarioService
from src.core.dependency_injection.dependency_injection import build_usuario_service
from src.presentation.dto.user_dto import UsuarioDTO, UpdateDataUserDTO, NewPasswordDTO
from src.presentation.mappers.user_mapper import map_usuario_domain_to_dto
from src.core.models.user_domain import UsuarioDomain
import bcrypt
from time import sleep

user_controller = APIRouter(prefix="/api/v1", tags=["user"])

@user_controller.post("/register")
async def register(
    usuario: UsuarioDTO,
    user_service: IUsuarioService = Depends(build_usuario_service)):
    try:
        return await user_service.create_usuario(usuario)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@user_controller.get("/usuarios")
async def get_usuarios(
    user_service: IUsuarioService = Depends(build_usuario_service)):
    try:
        return await user_service.get_all_usuarios()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@user_controller.get("/usuario/{id}")
async def get_usuario(
    id: int,
    user_service: IUsuarioService = Depends(build_usuario_service)):
    try:
        return await user_service.get_usuario(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@user_controller.put("/usuario/{id}")
async def update_usuario(
    id: int,
    usuarioUpdate: UpdateDataUserDTO,
    user_service: IUsuarioService = Depends(build_usuario_service)):
    try:
        usuario: UsuarioDomain = await user_service.get_usuario(id)
        updateUsuario = UsuarioDomain(
            nombre=usuarioUpdate.nombre,
            apellidoPaterno=usuarioUpdate.apellidoPaterno,
            apellidoMaterno=usuarioUpdate.apellidoMaterno,
            correo=usuarioUpdate.correo,
            genero=usuarioUpdate.genero,
            telefono=usuarioUpdate.telefono,
            pais=usuarioUpdate.pais,
            ciudad=usuarioUpdate.ciudad,
        )
        return await user_service.update_usuario(id, updateUsuario)
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@user_controller.put("/password")
async def change_password(
    new_password: NewPasswordDTO,
    user_service: IUsuarioService = Depends(build_usuario_service)):
    try:
        #haz que duerma 5s  
        
        sleep(5)
        
        return await user_service.change_password(new_password.correo, new_password.nueva_contrasena)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@user_controller.delete("/usuario/{id}")
async def delete_usuario(
    id: int,
    user_service: IUsuarioService = Depends(build_usuario_service)):
    try:
        return await user_service.delete_usuario(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
