from abc import abstractmethod, ABC
from src.core.models.multimedia_cultura_domain import MultimediaCulturaDomain
from src.presentation.dto.multimedia_cultura_dto import MultimediaCulturaDTO
from src.resources.responses.response import Response 


class IMultimediaCulturaRepository(ABC):
    
    @abstractmethod
    async def get_all_multimedia_cultura(self) -> Response:
        pass

    @abstractmethod
    async def get_multimedia_cultura_by_id_cultura(self, id_cultura: int) -> Response:
        pass

    @abstractmethod
    async def create_multimedia_cultura(self, multimedia_cultura: MultimediaCulturaDomain) -> None:
        pass

    @abstractmethod
    async def delete_multimedia_cultura(self, id_cultura: int) -> None:
        pass