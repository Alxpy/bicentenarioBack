from src.core.abstractions.infrastructure.repository.historia_repository_abstract import IHistoriaRepository
from src.core.abstractions.services.historia_service_abstract import IHistoriaService
from src.core.models.historia_domain import HistoriaDomain
from src.presentation.dto.historia_dto import HistoriaDTO
from src.resources.responses.response import Response


class HistoriaService(IHistoriaService):
    def __init__(self, historia_repository: IHistoriaRepository):
        self.historia_repository = historia_repository
    
    async def get_all_historia(self) -> Response:
        return await self.historia_repository.get_all_historia()
    
    async def get_historia_by_id(self, id: int) -> Response:
        return await self.historia_repository.get_historia_by_id(id)
    
    async def get_historia_by_titulo(self, titulo: str) -> Response:
        return await self.historia_repository.get_historia_by_titulo(titulo)
    
    async def get_historia_by_ubicacion(self, ubicacion: str) -> Response:
        return await self.historia_repository.get_historia_by_ubicacion(ubicacion)
    
    async def get_historia_by_categoria(self, categoria: str) -> Response:
        return await self.historia_repository.get_historia_by_categoria(categoria)
    
    async def create_historia(self, historia: HistoriaDTO) -> Response:
        return await self.historia_repository.create_historia(historia)
    
    async def update_historia(self, id: int, historia: HistoriaDomain) -> Response:
        return await self.historia_repository.update_historia(id, historia)
    
    async def delete_historia(self, id: int) -> Response:
        return await self.historia_repository.delete_historia(id)
    