from abc import abstractmethod, ABC
from src.core.models.comentario_evento_domain import ComentarioEventoDomain
from src.presentation.dto.comentario_evento_dto import ComentarioEventoDTO
from src.resources.responses.response import Response

class IComentarioBibliotecaService(ABC):
    
    @abstractmethod
    async def get_all_comentario_biblioteca(self) -> Response:
        pass

    @abstractmethod
    async def get_comentario_biblioteca_by_id_biblioteca(self, id_biblioteca: int) -> Response:
        pass

    @abstractmethod
    async def create_comentario_biblioteca(self, comentario_biblioteca: ComentarioEventoDomain) -> None:
        pass

    @abstractmethod
    async def delete_comentario_biblioteca(self, id_biblioteca: int) -> None:
        pass