from fastapi import Depends
from src.infrastructure.repository.connection_mail import get_gmail_service
from src.infrastructure.repository.dependency_injection.dependency_injection import get_connection

from src.infrastructure.repository.implementations.user_repository import UserRepository
from src.core.services.user_service import UsuarioService

from src.infrastructure.repository.implementations.auth_repository import AuthRepository
from src.core.services.auth_service import AuthService

from src.infrastructure.repository.implementations.email_repository import EmailRepository
from src.core.services.email_service import EmailService

from src.infrastructure.repository.implementations.categoriaNoticia_repository import CategoriaNoticiaRepository
from src.core.services.categoriaNoticia_service import CategoriaNoticiaService

from src.infrastructure.repository.implementations.noticia_repository import NoticiaRepository
from src.core.services.noticia_service import NoticiaService

from src.infrastructure.repository.implementations.tipoDocumento_repository import TipoDocumentoRepository
from src.core.services.tipoDocumento_service import TipoDocumentoService

from src.infrastructure.repository.implementations.biblioteca_repository import BibliotecaRepository
from src.core.services.biblioteca_service import BibliotecaService

from src.infrastructure.repository.implementations.ubicacion_repository import UbicacionRepository
from src.core.services.ubicacion_service import UbicacionService

from src.infrastructure.repository.implementations.cultura_repository import CulturaRepository
from src.core.services.cultura_service import CulturaService

from src.infrastructure.repository.implementations.presidente_repository import PresidenteRepository
from src.core.services.presidente_service import PresidenteService


def build_usuario_service(
    connection = Depends(get_connection),
):
    return UsuarioService(UserRepository(connection))

def build_auth_service(
    connection = Depends(get_connection),
):
    return AuthService(AuthRepository(connection))

def build_email_service(
    connection = Depends(get_connection),
    connection_email = Depends(get_gmail_service),
):
    return EmailService(EmailRepository(connection, connection_email))

def build_categoriaNoticia_service(
    connection = Depends(get_connection),
):
    return CategoriaNoticiaService(CategoriaNoticiaRepository(connection))

def build_noticia_service(
    connection = Depends(get_connection),
):
    return NoticiaService(NoticiaRepository(connection))

def build_tipoDocumento_service(
    connection = Depends(get_connection),
):
    return TipoDocumentoService(TipoDocumentoRepository(connection))

def build_biblioteca_service(
    connection = Depends(get_connection),
):
    return BibliotecaService(BibliotecaRepository(connection))

def build_ubicacion_service(
    connection = Depends(get_connection),
):
    return UbicacionService(UbicacionRepository(connection))

def build_cultura_service(
    connection = Depends(get_connection),
):
    return CulturaService(CulturaRepository(connection))

def build_presidente_service(
    connection = Depends(get_connection),
):
    return PresidenteService(PresidenteRepository(connection))