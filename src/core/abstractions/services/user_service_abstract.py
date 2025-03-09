from abc import ABC, abstractmethod
from src.core.models.user_domain import UsuarioDomain
from src.presentation.dto.user_dto import UsuarioDTO

class IUsuarioService(ABC):

    @abstractmethod
    async def get_usuario(self, id: int) -> UsuarioDomain:
        pass
    
    @abstractmethod
    async def get_all_usuarios(self) -> list[UsuarioDomain]:
        pass
    
    @abstractmethod
    async def create_usuario(self, usuario: UsuarioDTO) -> None:
        pass
    
    @abstractmethod
    async def update_usuario(self, id: int, usuario: UsuarioDomain) -> None:
        pass
    
    @abstractmethod
    async def delete_usuario(self, id: int) -> None:
        pass
    
    