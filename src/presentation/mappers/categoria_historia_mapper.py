from src.core.models.categoria_historia_domain import CategoriaHistoriaDomain
from src.presentation.dto.categoria_historia_dto import CategoriaHistoriaDTO

def map_categoria_historia_domain_to_dto(categoria_historia: CategoriaHistoriaDomain) -> CategoriaHistoriaDTO:
    return CategoriaHistoriaDTO(
        id=categoria_historia.id,
        nombre=categoria_historia.nombre,
        descripcion=categoria_historia.descripcion
    )