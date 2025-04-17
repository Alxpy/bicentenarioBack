from abc import ABC, abstractmethod
from src.core.models.historia_domain import HistoriaDomain
from src.presentation.dto.historia_dto import HistoriaDTO
from src.resources.responses.response import Response

class IHistoriaService(ABC):
    @abstractmethod
    async def get_all_historia(self) -> Response:
        """Get all historia records."""
        pass

    @abstractmethod
    async def get_historia_by_id(self, id: int) -> Response:
        """Get historia by ID."""
        pass

    @abstractmethod
    async def get_historia_by_titulo(self, titulo: str) -> Response:
        """Get historia by title."""
        pass

    @abstractmethod
    async def get_historia_by_ubicacion(self, ubicacion: str) -> Response:
        """Get historia by location."""
        pass

    @abstractmethod
    async def get_historia_by_categoria(self, categoria: str) -> Response:
        """Get historia by category."""
        pass

    @abstractmethod
    async def create_historia(self, historia: HistoriaDTO) -> Response:
        """Create a new historia record."""
        pass

    @abstractmethod
    async def update_historia(self, id: int, historia: HistoriaDomain) -> Response:
        """Update an existing historia record."""
        pass

    @abstractmethod
    async def delete_historia(self, id: int) -> Response:
        """Delete a historia record."""
        pass

    
