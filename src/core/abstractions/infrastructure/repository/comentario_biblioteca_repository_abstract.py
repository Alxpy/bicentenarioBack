from abc import abstractmethod, ABC
from src.core.models.comentario_biblioteca_domain import ComentarioBibliotecaDomain
from src.presentation.dto.comentario_biblioteca_dto import *
from src.resources.responses.response import Response

class IComentarioBibliotecaRepository(ABC):
        
        @abstractmethod
        async def get_all_comentario_biblioteca(self) -> Response:
            pass
    
        @abstractmethod
        async def get_comentario_biblioteca_by_id_biblioteca(self, id_biblioteca: int) -> Response:
            pass
    
        @abstractmethod
        async def create_comentario_biblioteca(self, comentario_biblioteca: ComentarioBibliotecaDomain) -> None:
            pass
    
        @abstractmethod
        async def delete_comentario_biblioteca(self, id_biblioteca: int) -> None:
            pass
