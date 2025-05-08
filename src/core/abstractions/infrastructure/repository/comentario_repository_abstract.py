from abc import ABC, abstractmethod
from src.core.models.comentario_domain import ComentarioDomain
from src.presentation.dto.comentario_dto import *
from src.resources.responses.response import Response

class IComentarioRepository(ABC):

    @abstractmethod
    async def get_all_comentarios(self) -> Response:
        pass

    @abstractmethod
    async def get_comentario_by_id(self, id: int) -> Response:
        pass

    @abstractmethod
    async def create_comentario(self, comentario: ComentarioDTO) -> None:
        pass

    @abstractmethod
    async def update_comentario(self, id: int, comentario: ComentarioUpdateDTO) -> None:
        pass

    @abstractmethod
    async def delete_comentario(self, id: int) -> None:
        pass