from abc import ABC,abstractmethod
from src.core.models.categoriaNoticia_domain import CategoriaNoticiaDomain
from src.presentation.dto.categoriaNoticia_dto import CategoriaNoticiaDTO

class ICategoriaNoticiaService(ABC):

    @abstractmethod
    async def get_categoria_noticia(self, id: int) -> CategoriaNoticiaDomain:
        pass
    
    @abstractmethod
    async def get_all_categorias_noticia(self) -> list[CategoriaNoticiaDomain]:
        pass
    
    @abstractmethod
    async def create_categoria_noticia(self, categoriaNoticia: CategoriaNoticiaDTO) -> None:
        pass
    
    @abstractmethod
    async def update_categoria_noticia(self, id: int, categoriaNoticia: CategoriaNoticiaDomain) -> None:
        pass

    @abstractmethod
    async def delete_categoria_noticia(self, id: int) -> None:
        pass
