from src.core.abstractions.infrastructure.repository.biblioteca_repository_abstract import IBibliotecaRepository
from src.core.abstractions.services.biblioteca_service_abstract import IBibliotecaService
from src.core.models.biblioteca_domain import BibliotecaDomain
from src.presentation.dto.biblioteca_dto import BibliotecaDTO

class BibliotecaService(IBibliotecaService):
    def __init__(self, biblioteca_repository: IBibliotecaService):
        self.biblioteca_repository = biblioteca_repository
    
    async def get_all_bibliotecas(self) -> list[BibliotecaDomain]:
        return await self.biblioteca_repository.get_all_bibliotecas()
    
    async def get_biblioteca_by_id(self, id: int) -> BibliotecaDomain:
        return await self.biblioteca_repository.get_biblioteca_by_id(id)
    
    async def get_biblioteca_by_title(self, titulo: str) -> BibliotecaDomain:
        return await self.biblioteca_repository.get_biblioteca_by_title(titulo)
    
    async def get_biblioteca_by_categoria(self, nomCategoria: str) -> list[BibliotecaDomain]:
        return await self.biblioteca_repository.get_biblioteca_by_categoria(nomCategoria)
    
    async def get_biblioteca_by_autor(self, autor: str) -> list[BibliotecaDomain]:
        return await self.biblioteca_repository.get_biblioteca_by_autor(autor)
    
    async def get_biblioteca_by_fecha(self, fecha: str) -> list[BibliotecaDomain]:
        return await self.biblioteca_repository.get_biblioteca_by_fecha(fecha)
    
    async def create_biblioteca(self, biblioteca: BibliotecaDTO) -> None:
        return await self.biblioteca_repository.create_biblioteca(biblioteca)
    
    async def update_biblioteca(self, id: int, biblioteca: BibliotecaDomain) -> None:
        return await self.biblioteca_repository.update_biblioteca(id, biblioteca)
    
    async def delete_biblioteca(self, id: int) -> None:
        return await self.biblioteca_repository.delete_biblioteca(id)