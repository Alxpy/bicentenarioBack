from src.core.models.comentario_biblioteca_domain import ComentarioBibliotecaDomain
from src.core.abstractions.services.comentario_biblioteca_service_abstract import IComentarioBibliotecaService
from src.core.abstractions.infrastructure.repository.comentario_biblioteca_repository_abstract import IComentarioBibliotecaRepository
from src.presentation.dto.comentario_biblioteca_dto import ComentarioBibliotecaDTO
from src.resources.responses.response import Response

class ComentarioBibliotecaService(IComentarioBibliotecaService):
    def __init__(self, comentario_biblioteca_repository: IComentarioBibliotecaRepository):
        self.comentario_biblioteca_repository = comentario_biblioteca_repository
    
    async def get_all_comentario_biblioteca(self) -> Response:
        return await self.comentario_biblioteca_repository.get_all_comentario_biblioteca()
    
    async def get_comentario_biblioteca_by_id_biblioteca(self, id: int) -> Response:
        return await self.comentario_biblioteca_repository.get_comentario_biblioteca_by_id_biblioteca(id)
    
    async def create_comentario_biblioteca(self, comentario_biblioteca: ComentarioBibliotecaDTO) -> None:
        return await self.comentario_biblioteca_repository.create_comentario_biblioteca(comentario_biblioteca)
    
    async def delete_comentario_biblioteca(self, id: int) -> None:
        return await self.comentario_biblioteca_repository.delete_comentario_biblioteca(id)