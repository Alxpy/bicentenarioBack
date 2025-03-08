from fastapi import APIRouter, Depends, HTTPException, status,Form
from src.core.abstractions.services.user_service_abstract import IUsuarioService
from src.core.dependency_injection.dependency_injection import build_usuario_service
from src.presentation.dto.user_dto import UsuarioDTO, UpdateDataUserDTO
from src.presentation.mappers.user_mapper import map_usuario_domain_to_dto
from src.core.models.user_domain import UsuarioDomain
import bcrypt

user_controller = APIRouter(prefix="/api/v1", tags=["user"])

@user_controller.post("/register")
async def register(
    usuario: UsuarioDTO = Depends(UsuarioDTO),
    user_service: IUsuarioService = Depends(build_usuario_service)):
    try:
        id = await user_service.create_usuario(map_usuario_domain_to_dto(usuario))
        return {"id": id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@user_controller.get("/usuarios")
async def get_usuarios(
    user_service: IUsuarioService = Depends(build_usuario_service)):
    try:
        usuarios = await user_service.get_all_usuarios()
        return usuarios
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@user_controller.get("/usuario/{id}")
async def get_usuario(
    id: int,
    user_service: IUsuarioService = Depends(build_usuario_service)):
    try:
        usuario = await user_service.get_usuario(id)
        return usuario
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@user_controller.put("/usuario")
async def update_usuario(
    id: int = Form(...),
    usuarioUpdate: UpdateDataUserDTO  = Depends(UpdateDataUserDTO),
    user_service: IUsuarioService = Depends(build_usuario_service)):
    try:
        usuario: UsuarioDomain = await user_service.get_usuario(id)
        updateUsuario = UsuarioDomain(
            id=usuario.id,
            nombre=usuarioUpdate.nombre,
            apellidoPaterno=usuarioUpdate.apellidoPaterno,
            apellidoMaterno=usuarioUpdate.apellidoMaterno,
            correo=usuarioUpdate.correo,
            contrasena=usuario.contrasena,
            genero=usuarioUpdate.genero,
            telefono=usuarioUpdate.telefono,
            pais=usuarioUpdate.pais,
            ciudad=usuarioUpdate.ciudad,
            estado=usuarioUpdate.estado,
            id_rol=usuario.id_rol
                
        )
        await user_service.update_usuario(id, updateUsuario)
        return {"message": "Usuario actualizado"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@user_controller.put("/usuario/rol")
async def change_rol(
    id: int = Form(...),
    id_rol: int = Form(...),
    user_service: IUsuarioService = Depends(build_usuario_service)):
    try:
        user:UsuarioDomain = await user_service.get_usuario(id)
        if user.id_rol == 1:
            raise HTTPException(status_code=400, detail="No se puede cambiar el rol de un administrador")
        
        update_usuario = UsuarioDomain(
            nombre= user.nombre,
            apellidoPaterno= user.apellidoPaterno,
            apellidoMaterno= user.apellidoMaterno,
            correo= user.correo,
            contrasena= user.contrasena,
            genero= user.genero,
            telefono= user.telefono,
            pais= user.pais,
            ciudad= user.ciudad,
            estado= user.estado,
            id_rol= id_rol
        )
        
        await user_service.update_usuario(id, update_usuario)
        return {"message": "Rol actualizado"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@user_controller.put("/usuario/password")
async def change_password(
    id: int = Form(...),
    contrasena: str = Form(...),
    nueva_contrasena: str = Form(...),
    user_service: IUsuarioService = Depends(build_usuario_service)):
    try:
        user:UsuarioDomain = await user_service.get_usuario(id)
        #if user.contrasena != contrasena:
        #    raise HTTPException(status_code=400, detail="La contraseña actual no coincide")
        
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
        return {"message": "Contraseña actualizada"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@user_controller.delete("/usuario")
async def delete_usuario(
    id: int = Form(...),
    user_service: IUsuarioService = Depends(build_usuario_service)):
    try:
        await user_service.delete_usuario(id)
        return {"message": "Usuario eliminado"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))