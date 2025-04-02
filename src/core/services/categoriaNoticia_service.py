from src.core.abstractions.infrastructure.repository.categoriaNoticia_repository_abstract import ICategoriaNoticiaRepository
from src.core.abstractions.services.categoriaNoticia_service_abstract import ICategoriaNoticiaService
from src.core.models.categoriaNoticia_domain import CategoriaNoticiaDomain
from src.presentation.dto.categoriaNoticia_dto import CategoriaNoticiaDTO

class CategoriaNoticiaService(ICategoriaNoticiaService):
    def __init__(self, categoriaNoticia_repository: ICategoriaNoticiaRepository):
        self.categoriaNoticia_repository = categoriaNoticia_repository
    
    async def get_categoria_noticia(self, id: int) -> CategoriaNoticiaDomain:
        return await self.categoriaNoticia_repository.get_categoria_noticia(id)
    
    async def get_all_categorias_noticia(self) -> list[CategoriaNoticiaDomain]:
        return await self.categoriaNoticia_repository.get_all_categorias_noticia()
    
    async def create_categoria_noticia(self, categoriaNoticia: CategoriaNoticiaDTO) -> None:
        return await self.categoriaNoticia_repository.create_categoria_noticia(categoriaNoticia)
    
    async def update_categoria_noticia(self, id: int, categoriaNoticia: CategoriaNoticiaDomain) -> None:
        return await self.categoriaNoticia_repository.update_categoria_noticia(id, categoriaNoticia)
    
    async def delete_categoria_noticia(self, id: int) -> None:
        return await self.categoriaNoticia_repository.delete_categoria_noticia(id)