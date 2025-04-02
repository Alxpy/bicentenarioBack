from src.core.models.biblioteca_domain import BibliotecaDomain
from src.presentation.dto.biblioteca_dto import BibliotecaDTO

def map_biblioteca_domain_to_dto(biblioteca: BibliotecaDomain) -> BibliotecaDTO:
    return BibliotecaDTO(
        id=0,
        titulo=biblioteca.titulo,
        autor=biblioteca.autor,
        imagen=biblioteca.imagen,
        fecha_publicacion=biblioteca.fecha_publicacion,
        edicion=biblioteca.edicion,
        id_tipo=biblioteca.id_tipo,
        fuente=biblioteca.fuente,
        enlace=biblioteca.enlace,
    )