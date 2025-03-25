from src.core.abstractions.infrastructure.repository.user_repository_abstract import IUsuarioRepository
from src.core.abstractions.services.user_service_abstract import IUsuarioService
from src.core.models.user_domain import UsuarioDomain
from src.presentation.dto.user_dto import UsuarioDTO

class UsuarioService(IUsuarioService):
    
    def __init__(self, usuario_repository: IUsuarioRepository):
        self.usuario_repository = usuario_repository

    
    
    async def get_usuario(self, id: int) -> UsuarioDomain:
        return await self.usuario_repository.get_usuario(id)
    
    
    async def get_all_usuarios(self) -> list[UsuarioDomain]:
        return await self.usuario_repository.get_all_usuarios()
    
    
    async def create_usuario(self, usuario: UsuarioDTO) -> None:
        return await self.usuario_repository.create_usuario(usuario)
    
    
    async def update_usuario(self, id: int, usuario: UsuarioDomain) -> None:
        return await self.usuario_repository.update_usuario(id, usuario)
    
    async def change_password(self, id, password):
        return await self.usuario_repository.change_password(id, password)
    
    async def delete_usuario(self, id: int) -> None:
        return await self.usuario_repository.delete_usuario(id)
    
    
            

