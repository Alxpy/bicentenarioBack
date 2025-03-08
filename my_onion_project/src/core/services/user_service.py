from src.core.abstractions.infrastructure.repository.user_repository_abstract import IUsuarioRepository
from src.core.abstractions.services.user_service_abstract import IUsuarioService
from src.core.models.user_domain import UsuarioDomain

class UsuarioService(IUsuarioService):
    def __init__(self, usuario_repository: IUsuarioRepository):
        self.usuario_repository = usuario_repository

    async def get_usuario(self, id: int):
        usuario= await self.usuario_repository.get_usuario(id)
        if usuario is None:
            raise ValueError(f"Usuario con id{id}no encontrado")
        return usuario

    async def create_usuario(self, usuario:UsuarioDomain) -> UsuarioDomain:
        try:
            last_id = await self.usuario_repository.create_usuario(usuario)
            usuario.id = last_id
            return usuario
        except Exception as e:
            raise ValueError(f"Error al crear usuario: {str(e)}")

    async def update_usuario(self, idCliente: int, usuario: UsuarioDomain) -> UsuarioDomain:
        existing_usuario = await self.usuario_repository.get_usuario(idCliente)
        if not existing_usuario:
            raise ValueError(f"Usuario con id{idCliente}no encontrado")
        await self.usuario_repository.update_usuario(idCliente, usuario)
        return await self.usuario_repository.get_usuario(idCliente)
    
    async def delete_usuario(self, idCliente: int) -> None:
        existing_usuario = await self.usuario_repository.get_usuario(idCliente)
        if not existing_usuario:
            raise ValueError(f"Usuario con id{idCliente}no encontrado")
        await self.usuario_repository.delete_usuario(idCliente)

    async def get_all_usuarios(self) -> list[UsuarioDomain]:
        return await self.usuario_repository.get_all_usuarios()
    
    async def get_by_correo(self, correo: str) -> UsuarioDomain:
        usuario = await self.usuario_repository.get_by_correo(correo)
        if usuario is None:
            raise ValueError(f"Usuario con correo{correo}no encontrado")
        return usuario
    
    async def delete_by_correo(self, correo: str) -> UsuarioDomain:
        usuario = await self.usuario_repository.get_by_correo(correo)
        if usuario is None:
            raise ValueError(f"Usuario con correo{correo}no encontrado")
        await self.usuario_repository.delete_by_correo(correo)
        return usuario

    async def registrar_usuario(self, usuario: UsuarioDomain) -> bool:
        return await self.usuario_repository.registrar_usuario(usuario)
    
    async def login_usuario(self, correo: str, contrasena: str) -> UsuarioDomain:
        return await self.usuario_repository.login_usuario(correo, contrasena)
    
            

