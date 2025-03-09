from fastapi import APIRouter, Depends, HTTPException, status, Form
from src.core.abstractions.services.user_service_abstract import IUsuarioService
from src.core.dependency_injection.dependency_injection import build_usuario_service
from src.presentation.dto.user_dto import UsuarioDTO, UpdateDataUserDTO
from src.presentation.mappers.user_mapper import map_usuario_domain_to_dto
from src.core.models.user_domain import UsuarioDomain
import bcrypt

user_controller = APIRouter(prefix="/api/v1", tags=["user"])

@user_controller.post("/register")
async def register(
    usuario: UsuarioDTO,
    user_service: IUsuarioService = Depends(build_usuario_service)):
    try:
        response = await user_service.create_usuario(usuario)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@user_controller.get("/usuarios")
async def get_usuarios(
    user_service: IUsuarioService = Depends(build_usuario_service)):
    try:
        usuarios = await user_service.get_all_usuarios()
        return {"response": usuarios}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@user_controller.get("/usuario/{id}")
async def get_usuario(
    id: int,
    user_service: IUsuarioService = Depends(build_usuario_service)):
    try:
        usuario = await user_service.get_usuario(id)
        return {"response": usuario}
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
        response = await user_service.update_usuario(id, updateUsuario)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@user_controller.put("/password/{id}")
async def change_password(
    id: int,
    nueva_contrasena: str = Form(...),
    user_service: IUsuarioService = Depends(build_usuario_service)):
    try:
        user:UsuarioDomain = await user_service.get_usuario(id)
        
        update_usuario = UsuarioDomain(
            id= user.id,
            nombre= user.nombre,
            apellidoPaterno= user.apellidoPaterno,
            apellidoMaterno= user.apellidoMaterno,
            correo= user.correo,
            contrasena= bcrypt.hashpw(nueva_contrasena.encode('utf-8'), bcrypt.gensalt()),
            genero= user.genero,
            telefono= user.telefono,
            pais= user.pais,
            ciudad= user.ciudad,
            estado= user.estado,
            id_rol= user.id_rol
        )
        
        await user_service.update_usuario(id, update_usuario)
        return {"response": "Contraseña actualizada"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@user_controller.delete("/usuario/{id}")
async def delete_usuario(
    id: int,
    user_service: IUsuarioService = Depends(build_usuario_service)):
    try:
        await user_service.delete_usuario(id)
        return {"response": "Usuario eliminado"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
