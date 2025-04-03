from src.core.abstractions.infrastructure.repository.noticia_repository_abstract import INoticiaRepository
from src.core.abstractions.services.noticia_service_abstract import INoticiaService
from src.core.models.noticia_domain import NoticiaDomain
from src.presentation.dto.noticia_dto import NoticiaDTO

class NoticiaService(INoticiaService):
    
    def __init__(self, noticia_repository: INoticiaRepository):
        self.noticia_repository = noticia_repository
    
    async def get_all_noticias(self) -> list[NoticiaDomain]:
        return await self.noticia_repository.get_all_noticias()
    
    async def get_noticia_by_id(self, id: int) -> NoticiaDomain:
        return await self.noticia_repository.get_noticia_by_id(id)
    
    async def get_noticia_by_fecha(self, fecha: str) -> NoticiaDomain:
        return await self.noticia_repository.get_noticia_by_fecha(fecha)
    
    async def get_noticia_by_categoria(self, nomCategoria: str) -> NoticiaDomain:
        return await self.noticia_repository.get_noticia_by_categoria(nomCategoria)
    
    async def get_noticia_by_title(self, titulo: str) -> NoticiaDomain:
        return await self.noticia_repository.get_noticia_by_title(titulo)
    
    async def create_noticia(self, noticia: NoticiaDTO) -> None:
        return await self.noticia_repository.create_noticia(noticia)
    
    async def update_noticia(self, id: int, noticia: NoticiaDomain) -> None:
        return await self.noticia_repository.update_noticia(id, noticia)
    
    async def delete_noticia(self, id: int) -> None:
        return await self.noticia_repository.delete_noticia(id)