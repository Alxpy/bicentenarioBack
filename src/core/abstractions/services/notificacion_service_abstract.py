from abc import ABC, abstractmethod
from src.core.models.notificacion_domain import NotificacionDomain
from src.presentation.dto.notificacion_dto import NotificacionDTO
from src.resources.responses.response import Response

class INotificacionService(ABC):
    @abstractmethod
    async def get_notificacion_by_id(self, id: int) -> Response:
        """Get a notification by its ID."""
        pass

