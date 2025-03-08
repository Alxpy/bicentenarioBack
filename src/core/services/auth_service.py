
from src.presentation.dto.auth_dto import AuthLoginDTO, AuthLogoutDTO
from src.core.abstractions.infrastructure.repository.auth_repository_abstract import IAuthRepositoryAbstract
from src.core.abstractions.services.auth_service_abstract import IAuthServiceAbstract

class AuthService(IAuthServiceAbstract):

    def __init__(self, auth_repository: IAuthRepositoryAbstract):
        self.auth_repository = auth_repository
    
    async def login(self, auth_login_dto: AuthLoginDTO) -> str:
        return await self.auth_repository.login(auth_login_dto)

    
    async def logout(self, auth_logout_dto: AuthLogoutDTO) -> None:
        return await self.auth_repository.logout(auth_logout_dto)
    
       


