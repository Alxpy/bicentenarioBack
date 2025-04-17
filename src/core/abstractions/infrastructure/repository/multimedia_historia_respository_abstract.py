from abc import abstractmethod, ABC
from src.core.models.multimedia_historia_domain import MultimediaHistoriaDomain
from src.presentation.dto.multimedia_historia_dto import MultimediaHistoriaDTO
from src.resources.responses.response import Response 


class IMultimediaHistoriaRepository(ABC):

    @abstractmethod
    async def get_all_multimedia_historia(self) -> Response:
        pass

    @abstractmethod
    async def get_multimedia_historia_by_id_historia(self, id_historia: int) -> Response:
        pass

    @abstractmethod
    async def create_multimedia_historia(self, multimedia_historia: MultimediaHistoriaDTO) -> None:
        pass

    @abstractmethod
    async def delete_multimedia_historia(self, id_historia: int) -> None:
        pass
