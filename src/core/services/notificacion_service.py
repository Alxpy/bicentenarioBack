from src.core.abstractions.services.notificacion_service_abstract import INotificacionService
from src.core.abstractions.infrastructure.repository.notificacion_repository_abstract import INotificacionRepositoryAbstract
from src.core.models.notificacion_domain import NotificacionDomain
from src.presentation.dto.notificacion_dto import NotificacionDTO
from src.resources.responses.response import Response

class NotificacionService(INotificacionService):
    def __init__(self, notificacion_repository: INotificacionRepositoryAbstract):
        self.notificacion_repository = notificacion_repository

    async def get_notificacion_by_id(self, id: int) -> NotificacionDomain:
        """Get a notification by its ID."""
        return await self.notificacion_repository.get_notificacion_by_id(id)