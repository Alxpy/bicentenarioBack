from abc import ABC, abstractmethod
from src.core.models.noticia_domain import NoticiaDomain
from src.presentation.dto.noticia_dto import NoticiaDTO

class INoticiaService(ABC):
    
    @abstractmethod
    async def get_all_noticias(self) -> list[NoticiaDomain]:
        pass

    @abstractmethod
    async def get_noticia_by_id(self, id: int) -> NoticiaDomain:
        pass
    
    @abstractmethod
    async def get_noticia_by_fecha(self, fecha: str) -> list[NoticiaDomain]:
        pass
    
    @abstractmethod
    async def get_noticia_by_categoria(self, nomCategoria: str) -> list[NoticiaDomain]:
        pass
    
    @abstractmethod
    async def get_noticia_by_title(self, titulo: str) -> NoticiaDomain:
        pass

    @abstractmethod
    async def create_noticia(self, noticia: NoticiaDTO) -> None:
        pass
    
    @abstractmethod
    async def update_noticia(self, id: int, noticia: NoticiaDomain) -> None:
        pass
    
    @abstractmethod
    async def delete_noticia(self, id: int) -> None:
        pass