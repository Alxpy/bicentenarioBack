from abc import abstractmethod, ABC
from src.core.models.tipoDocumento_domain import TipoDocumentoDomain
from src.presentation.dto.tipoDocumento_dto import TipoDocumentoDTO

class ITipoDocumentoRepository(ABC):

    @abstractmethod
    async def get_tipo_documento(self, id: int) -> TipoDocumentoDomain:
        pass
    
    @abstractmethod
    async def get_all_tipos_documento(self) -> list[TipoDocumentoDomain]:
        pass
    
    @abstractmethod
    async def create_tipo_documento(self, tipo_documento: TipoDocumentoDTO) -> None:
        pass
    
    @abstractmethod
    async def update_tipo_documento(self, id: int, tipo_documento: TipoDocumentoDomain) -> None:
        pass
    
    @abstractmethod
    async def delete_tipo_documento(self, id: int) -> None:
        pass