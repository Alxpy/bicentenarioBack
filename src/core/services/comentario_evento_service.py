from src.core.abstractions.services.comentario_evento_service_abstract import IComentarioEventoService
from src.core.abstractions.infrastructure.repository.comentario_evento_repository_abstract import IComentarioEventoRepository
from src.core.models.comentario_evento_domain import ComentarioEventoDomain
from src.presentation.dto.comentario_evento_dto import ComentarioEventoDTO
from src.resources.responses.response import Response

class ComentarioEventoService(IComentarioEventoService):
    def __init__(self, comentario_evento_repository: IComentarioEventoRepository):
        self.comentario_evento_repository = comentario_evento_repository
    
    async def get_all_comentario_evento(self) -> Response:
        return await self.comentario_evento_repository.get_all_comentario_evento()
    
    async def get_comentario_evento_by_id_evento(self, id: int) -> Response:
        return await self.comentario_evento_repository.get_comentario_evento_by_id_evento(id)
    
    async def create_comentario_evento(self, comentario_evento: ComentarioEventoDTO) -> None:
        return await self.comentario_evento_repository.create_comentario_evento(comentario_evento)
    
    async def delete_comentario_evento(self, id: int) -> None:
        return await self.comentario_evento_repository.delete_comentario_evento(id)