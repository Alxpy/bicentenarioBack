from src.core.models.comentario_biblioteca_domain import ComentarioBibliotecaDomain
from src.presentation.dto.comentario_biblioteca_dto import ComentarioBibliotecaDTO

def map_comentario_biblioteca_domain_to_dto(comentario: ComentarioBibliotecaDomain) -> ComentarioBibliotecaDTO:
    return ComentarioBibliotecaDTO(
        id_comentario=comentario.id_comentario,
        id_biblioteca=comentario.id_biblioteca,
    )
