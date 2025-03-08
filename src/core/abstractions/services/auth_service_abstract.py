from abc import ABC, abstractmethod
from src.presentation.dto.auth_dto import AuthLoginDTO, AuthLogoutDTO

class IAuthServiceAbstract(ABC):

    @abstractmethod
    async def login(self, auth_login_dto: AuthLoginDTO) -> str:
        pass

    @abstractmethod
    async def logout(self, auth_logout_dto: AuthLogoutDTO) -> None:
        pass
       


