from src.core.abstractions.infrastructure.repository.categoria_historia_repository_abstract import ICategoriaHistoriaRepository
from src.core.abstractions.services.categoria_historia_service_abstract import ICategoriaHistoriaService
from src.core.models.categoria_historia_domain import CategoriaHistoriaDomain
from src.presentation.dto.categoria_historia_dto import CategoriaHistoriaDTO
from src.resources.responses.response import Response

class CategoriaHistoriaService(ICategoriaHistoriaService):
    def __init__(self, categoria_historia_repository: ICategoriaHistoriaRepository):
        self.categoria_historia_repository = categoria_historia_repository
    
    async def get_categoria_historia(self, id: int) -> Response:
        return await self.categoria_historia_repository.get_categoria_historia(id)
    
    async def get_all_categorias_historia(self) -> Response:
        return await self.categoria_historia_repository.get_all_categorias_historia()
    
    async def create_categoria_historia(self, categoria_historia: CategoriaHistoriaDTO) -> None:
        return await self.categoria_historia_repository.create_categoria_historia(categoria_historia)
    
    async def update_categoria_historia(self, id: int, categoria_historia: CategoriaHistoriaDomain) -> None:
        return await self.categoria_historia_repository.update_categoria_historia(id, categoria_historia)
    
    async def delete_categoria_historia(self, id: int) -> None:
        return await self.categoria_historia_repository.delete_categoria_historia(id)
    
