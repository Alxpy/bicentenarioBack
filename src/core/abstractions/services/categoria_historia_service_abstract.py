from abc import ABC, abstractmethod
from src.core.models.categoria_historia_domain import CategoriaHistoriaDomain
from src.presentation.dto.categoria_historia_dto import CategoriaHistoriaDTO
from src.resources.responses.response import Response

class ICategoriaHistoriaService(ABC):

    @abstractmethod
    async def get_categoria_historia(self, id: int) -> Response:
        pass

    @abstractmethod
    async def get_all_categorias_historia(self) -> Response:
        pass

    @abstractmethod
    async def create_categoria_historia(self, categoria_historia: CategoriaHistoriaDTO) -> None:
        pass

    @abstractmethod
    async def update_categoria_historia(self, id: int, categoria_historia: CategoriaHistoriaDomain) -> None:    
        pass

    @abstractmethod
    async def delete_categoria_historia(self, id: int) -> None:
        pass
