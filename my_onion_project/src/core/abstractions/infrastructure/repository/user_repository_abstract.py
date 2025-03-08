from abc import ABC, abstractmethod
from src.core.models.user_domain import UsuarioDomain
class IUsuarioRepository(ABC):

    @abstractmethod
    async def get_usuario(self, id: int) -> UsuarioDomain:
        pass
    @abstractmethod
    async def create_usuario(self, Usuario: UsuarioDomain) -> int:
        pass

    @abstractmethod
    async def update_usuario(self,id:int, suario: UsuarioDomain) -> bool:
        pass

    @abstractmethod
    async def delete_usuario(self, id: int) -> bool:
        pass

    @abstractmethod
    async def get_all_usuarios(self) -> list[UsuarioDomain]:
        pass

    @abstractmethod
    async def get_by_correo(self, correo: str) -> UsuarioDomain:
        pass

    @abstractmethod
    async def delete_by_correo(self, correo: str) -> UsuarioDomain:
        pass

    @abstractmethod
    async def registrar_usuario(self, usuario: UsuarioDomain) -> bool:
        pass

    @abstractmethod
    async def login_usuario(self, correo: str, contrasena: str) -> UsuarioDomain:
        pass
    