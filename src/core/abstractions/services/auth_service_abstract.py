from abc import ABC, abstractmethod
from src.presentation.dto.auth_dto import AuthLoginDTO, AuthLogoutDTO, AuthVerifyCodeDTO

class IAuthServiceAbstract(ABC):

    @abstractmethod
    async def login(self, auth_login_dto: AuthLoginDTO) -> str:
        pass

    @abstractmethod
    async def logout(self, auth_logout_dto: AuthLogoutDTO) -> None:
        pass
       
    @abstractmethod
    async def verify_code_login(self, auth_verify: AuthVerifyCodeDTO) -> bool:
        pass
    
    @abstractmethod
    async def verify_code_email(self, auth_verify: AuthVerifyCodeDTO) -> bool:
        pass
    
