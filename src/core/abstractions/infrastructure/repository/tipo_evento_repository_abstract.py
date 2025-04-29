from abc import abstractmethod, ABC
from src.core.models.tipo_evento_domain import TipoEventoDomain
from src.presentation.dto.tipo_evento_dto import TipoEventoDTO
from src.resources.responses.response import Response 

class ITipoEventoRepository(ABC):

    @abstractmethod
    async def get_tipo_evento_by_id(self, id: int) -> Response:
        pass

    @abstractmethod
    async def get_all_tipo_eventos(self) -> Response:
        pass

    @abstractmethod
    async def create_tipo_evento(self, tipo_evento: TipoEventoDTO) -> None:
        pass

    @abstractmethod
    async def update_tipo_evento(self, id: int, tipo_evento: TipoEventoDomain) -> None:
        pass

    @abstractmethod
    async def delete_tipo_evento(self, id: int) -> None:
        pass
