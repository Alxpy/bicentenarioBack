from src.core.abstractions.infrastructure.repository.comentario_repository_abstract import IComentarioRepository
from src.core.abstractions.services.comentario_service_abstract import IComentarioService
from src.core.models.comentario_domain import ComentarioDomain
from src.presentation.dto.comentario_dto import ComentarioDTO, ComentarioUpdateDTO
from src.resources.responses.response import Response

class ComentarioService(IComentarioService):
    
    def __init__(self, comentario_repository: IComentarioRepository):
        self.comentario_repository = comentario_repository

    async def get_all_comentarios(self) -> Response:
        return await self.comentario_repository.get_all_comentarios()
    
    async def get_comentario_by_id(self, id: int) -> Response:
        return await self.comentario_repository.get_comentario_by_id(id)
    
    async def create_comentario(self, comentario: ComentarioDTO) -> None:
        return await self.comentario_repository.create_comentario(comentario)
    
    async def update_comentario(self, id: int, comentario: ComentarioUpdateDTO) -> None:
        return await self.comentario_repository.update_comentario(id, comentario)
    
    async def delete_comentario(self, id: int) -> None:
        return await self.comentario_repository.delete_comentario(id)
        