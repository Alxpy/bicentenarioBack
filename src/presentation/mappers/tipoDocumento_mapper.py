from src.core.models.tipoDocumento_domain import TipoDocumentoDomain
from src.presentation.dto.tipoDocumento_dto import TipoDocumentoDTO

def map_tipoDocumento_domain_to_dto(tipoDocumentoDTO: TipoDocumentoDTO) -> TipoDocumentoDTO:
    return TipoDocumentoDTO(
        id_tipo=0,
        tipo=tipoDocumentoDTO.tipo
    )