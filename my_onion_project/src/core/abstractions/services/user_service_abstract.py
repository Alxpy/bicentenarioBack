from abc import ABC, abstractmethod
from src.core.models.user_domain import UsuarioDomain

class IUsuarioService(ABC):
    @abstractmethod
    async def get_usuario(self, id: int) -> UsuarioDomain:
        pass

    @abstractmethod
    async def create_usuario(self, Usuario: UsuarioDomain) -> UsuarioDomain:
        pass

    @abstractmethod
    async def update_usuario(self,id:int ,Usuario: UsuarioDomain) -> UsuarioDomain:
        pass

    @abstractmethod
    async def delete_usuario(self, id: int) -> None:
        pass

    @abstractmethod
    async def get_all_usuarios(self) -> list[UsuarioDomain]:
        pass

    @abstractmethod
    async def get_by_correo(self, correo: str) -> UsuarioDomain:
        pass

    @abstractmethod
    async def delete_by_correo(self, correo: str,usuario:UsuarioDomain) -> UsuarioDomain:
        pass

    @abstractmethod
    async def registrar_usuario(self, usuario: UsuarioDomain) -> bool:
        pass
    
    @abstractmethod
    async def login_usuario(self, correo: str, contrasena: str) -> UsuarioDomain:
        pass
