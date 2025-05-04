from abc import ABC, abstractmethod
from src.core.models.usuario_evento_domain import UsuarioEventoDomain
from src.presentation.dto.usuario_evento_dto import UsuarioEventoDTO, UpdateAsistioUsuarioEventoDTO
from src.resources.responses.response import Response

class IUsuarioEventoService(ABC):
    
    @abstractmethod
    async def get_usuario_evento_by_id_usuario(self, id: int) -> Response:
        """Get a user event by its ID."""
        pass

    @abstractmethod
    async def get_usuario_evento_by_id_evento(self,id:int) -> Response:
        """Get all user events."""
        pass

    @abstractmethod
    async def get_all_usuario_eventos(self) -> Response:
        """Get all user events."""
        pass

    @abstractmethod
    async def create_usuario_evento(self, usuario_evento: UsuarioEventoDTO) -> None:
        """Create a new user event."""
        pass

    @abstractmethod
    async def update_asistio_usuario_evento(self, id: int, asistio: UpdateAsistioUsuarioEventoDTO) -> None:
        """Update the attendance status of a user event."""
        pass

    @abstractmethod
    async def delete_usuario_evento(self, id: int) -> None:
        """Delete a user event."""
        pass

    