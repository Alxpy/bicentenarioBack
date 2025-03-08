from fastapi import Depends
from src.infrastructure.repository.connection import get_connection
from src.infrastructure.repository.connection_mail import get_gmail_service

from src.infrastructure.repository.implementations.user_repository import UserRepository
from src.core.services.user_service import UsuarioService

from src.infrastructure.repository.implementations.auth_repository import AuthRepository
from src.core.services.auth_service import AuthService

from src.infrastructure.repository.implementations.email_repository import EmailRepository
from src.core.services.email_service import EmailService

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