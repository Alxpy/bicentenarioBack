from abc import ABC, abstractmethod
from src.core.models.usuario_rol_domain import UsuarioRolDomain
from src.presentation.dto.usuario_rol_dto import UsuarioRolDTO
from src.resources.responses.response import Response

class IUsuarioRolRepository(ABC):

    @abstractmethod
    async def get_all_usuario_roles(self) -> Response:
        """Get all user roles."""
        pass

    @abstractmethod
    async def get_usuario_rol_by_id_rol(self, id: int) -> Response:
        """Get a user role by its ID."""
        pass

    @abstractmethod
    async def create_usuario_rol(self, usuario_rol: UsuarioRolDTO) -> None:
        """Create a new user role."""
        pass

    @abstractmethod
    async def delete_usuario_rol(self, id: int) -> None:
        """Delete a user role."""
        pass
