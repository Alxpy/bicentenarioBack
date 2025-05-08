from abc import abstractmethod, ABC
from src.core.models.comentario_evento_domain import ComentarioEventoDomain
from src.presentation.dto.comentario_evento_dto import *
from src.resources.responses.response import Response

class IComentarioEventoService(ABC):
    
    @abstractmethod
    async def get_all_comentario_evento(self) -> Response:
        pass

    @abstractmethod
    async def get_comentario_evento_by_id_evento(self, id_evento: int) -> Response:
        pass

    @abstractmethod
    async def create_comentario_evento(self, comentario_evento: ComentarioEventoDomain) -> None:
        pass

    @abstractmethod
    async def delete_comentario_evento(self, id_evento: int) -> None:
        pass