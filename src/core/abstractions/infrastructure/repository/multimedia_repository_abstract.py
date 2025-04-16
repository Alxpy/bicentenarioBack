from abc import ABC, abstractmethod
from src.core.models.multimedia_domain import MultimediaDomain
from src.presentation.dto.multimedia_dto import MultimediaDTO

class IMultimediaRepository(ABC):

    @abstractmethod
    async def get_all_multimedia(self) -> list[MultimediaDomain]:
        pass

    @abstractmethod
    async def get_multimedia_by_id(self, id: int) -> MultimediaDomain:
        pass

    @abstractmethod
    async def create_multimedia(self, multimedia: MultimediaDTO) -> None:
        pass

    @abstractmethod
    async def update_multimedia(self, id: int, multimedia: MultimediaDomain) -> None:
        pass

    @abstractmethod
    async def delete_multimedia(self, id: int) -> None:
        pass