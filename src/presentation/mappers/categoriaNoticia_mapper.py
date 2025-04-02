from src.core.models.categoriaNoticia_domain import CategoriaNoticiaDomain
from src.presentation.dto.categoriaNoticia_dto import CategoriaNoticiaDTO

def map_categoriaNoticia_domain_to_dto(categoriaNoticiaDTO: CategoriaNoticiaDTO) -> CategoriaNoticiaDTO:
    return CategoriaNoticiaDTO(
        id=0,
        nombre_categoria=categoriaNoticiaDTO.nombre_categoria
    )