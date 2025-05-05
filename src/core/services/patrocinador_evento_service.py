from src.core.models.patrocinador_evento_domain import PatrocinadorEvento
from src.presentation.responses.base_response import Response
from src.infrastructure.repository.implementations.patrocinador_evento_repository import PatrocinadorEventoRepository
class PatrocinadorEventoService:
    
    def __init__(self, patrocinador_evento_repository: PatrocinadorEventoRepository):        
        self.patrocinador_evento_repository = patrocinador_evento_repository
        
    async def create_patrocinador_evento(self, patrocinador_evento: PatrocinadorEvento) -> Response:
        return await self.patrocinador_evento_repository.create_patrocinador_evento(patrocinador_evento)
    
    async def get_patrocinador_by_evento(self, id_evento: int) -> Response:
        return await self.patrocinador_evento_repository.get_patrocinador_by_evento(id_evento)
    
    async def get_evento_by_patrocinador(self, id_patrocinador: int) -> Response:
        return await self.patrocinador_evento_repository.get_evento_by_patrocinador(id_patrocinador)
    
    