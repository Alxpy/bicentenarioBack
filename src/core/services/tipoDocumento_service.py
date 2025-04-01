from src.core.abstractions.infrastructure.repository.tipoDocumento_repository_abstract import ITipoDocumentoRepository 
from src.core.abstractions.services.tipoDocumento_service_abstract import ITipoDocumentoService
from src.core.models.tipoDocumento_domain import TipoDocumentoDomain
from src.presentation.dto.tipoDocumento_dto import TipoDocumentoDTO

class TipoDocumentoService(ITipoDocumentoService):
    def __init__(self, tipo_documento_repository: ITipoDocumentoRepository) -> None:
        self.tipo_documento_repository = tipo_documento_repository
    
    async def get_tipo_documento(self, id: int) -> TipoDocumentoDomain:
        return await self.tipo_documento_repository.get_tipo_documento(id)
    
    async def get_all_tipos_documento(self) -> list[TipoDocumentoDomain]:
        return await self.tipo_documento_repository.get_all_tipos_documento()
    
    async def create_tipo_documento(self, tipo_documento: TipoDocumentoDTO) -> None:
        return await self.tipo_documento_repository.create_tipo_documento(tipo_documento)
    
    async def update_tipo_documento(self, id: int, tipo_documento: TipoDocumentoDomain) -> None:
        return await self.tipo_documento_repository.update_tipo_documento(id, tipo_documento)
    
    async def delete_tipo_documento(self, id: int) -> None:
        return await self.tipo_documento_repository.delete_tipo_documento(id)