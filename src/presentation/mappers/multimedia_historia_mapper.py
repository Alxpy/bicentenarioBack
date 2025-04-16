from src.core.models.multimedia_historia_domain import MultimediaHistoriaDomain
from src.presentation.dto.multimedia_historia_dto import MultimediaHistoriaDTO

def map_multimedia_historia_domain_to_dto(multimedia: MultimediaHistoriaDomain) -> MultimediaHistoriaDTO:
    return MultimediaHistoriaDTO(
        id_historia=multimedia.id_historia,
        id_multimedia=multimedia.id_multimedia  
    )