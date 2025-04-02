from abc import ABC, abstractmethod
from src.core.models.biblioteca_domain import BibliotecaDomain
from src.presentation.dto.biblioteca_dto import BibliotecaDTO

class IBibliotecaService(ABC):
    @abstractmethod
    async def get_all_bibliotecas(self) -> list[BibliotecaDomain]:
        pass

    @abstractmethod
    async def get_biblioteca_by_id(self, id: int) -> BibliotecaDomain:
        pass

    @abstractmethod
    async def get_biblioteca_by_title(self, titulo: str) -> BibliotecaDomain:
        pass

    @abstractmethod
    async def get_biblioteca_by_categoria(self, nomCategoria: str) -> list[BibliotecaDomain]:
        pass

    @abstractmethod
    async def get_biblioteca_by_autor(self, autor: str) -> list[BibliotecaDomain]:
        pass

    @abstractmethod
    async def get_biblioteca_by_fecha(self, fecha: str) -> list[BibliotecaDomain]:
        pass

    @abstractmethod
    async def create_biblioteca(self, biblioteca: BibliotecaDTO) -> None:
        pass
    
    @abstractmethod
    async def update_biblioteca(self, id: int, biblioteca: BibliotecaDomain) -> None:
        pass
    
    @abstractmethod
    async def delete_biblioteca(self, id: int) -> None:
        pass