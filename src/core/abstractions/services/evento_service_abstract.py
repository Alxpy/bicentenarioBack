from abc import ABC, abstractmethod
from src.core.models.evento_domain import EventoDomain
from src.presentation.dto.evento_dto import EventoDTO, EventoPostDTO, EventoUpdateDTO
from src.resources.responses.response import Response

class IEventoService(ABC):

    @abstractmethod
    async def get_all_eventos(self) -> Response:
        """Get all eventos records."""
        pass

    @abstractmethod
    async def get_evento_by_id(self, id: int) -> Response:
        """Get evento by ID."""
        pass

    @abstractmethod
    async def get_evento_by_nombre(self, nombre: str) -> Response:
        """Get evento by name."""
        pass
    
    @abstractmethod
    async def get_evento_by_fecha(self, fecha: str) -> Response:
        """Get evento by date."""
        pass

    @abstractmethod
    async def get_evento_by_tipo(self, tipo: str) -> Response:
        """Get evento by category."""
        pass

    @abstractmethod
    async def get_evento_by_ubicacion(self, ubicacion: str) -> Response:
        """Get evento by location."""
        pass

    @abstractmethod
    async def create_evento(self, evento: EventoPostDTO) -> Response:
        """Create a new evento record."""
        pass

    @abstractmethod
    async def update_evento(self, id: int, evento: EventoUpdateDTO) -> Response:
        """Update an existing evento record."""
        pass

    @abstractmethod
    async def delete_evento(self, id: int) -> Response:
        """Delete a evento record."""
        pass