from src.core.models.multimedia_cultura_domain import MultimediaCulturaDomain
from src.presentation.dto.multimedia_cultura_dto import MultimediaCulturaDTO

def map_multimedia_cultura_domain_to_dto(multimedia: MultimediaCulturaDomain) -> MultimediaCulturaDTO:
    return MultimediaCulturaDTO(
        id_cultura=multimedia.id_cultura,
        id_multimedia=multimedia.id_multimedia  
    )

