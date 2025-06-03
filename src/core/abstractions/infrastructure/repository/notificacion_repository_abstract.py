from abc import ABC, abstractmethod
from src.presentation.responses.base_response import Response
from src.core.models.notificacion_domain import NotificacionDomain

class INotificacionRepositoryAbstract(ABC):

    @abstractmethod
    async def get_notificacion_by_usuario(self, id_usuario: int) -> Response:
        """
        Obtiene todas las notificaciones asociadas a un usuario.
        """
        pass

   
