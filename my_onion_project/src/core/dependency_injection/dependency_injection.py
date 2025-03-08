from fastapi import Depends
from src.infrastructure.repository.connection import get_connection
from src.infrastructure.repository.implementations.user_repository import UserRepository
from src.core.services.user_service import UserService

def build_usuario_service(
    connection = Depends(get_connection),
):
    return UserService(UserRepository(connection))

