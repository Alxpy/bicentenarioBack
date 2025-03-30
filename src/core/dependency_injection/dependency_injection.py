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
