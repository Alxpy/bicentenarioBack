from abc import ABC, abstractmethod
from src.presentation.dto.auth_dto import AuthLoginDTO, AuthLogoutDTO, AuthVerifyCodeDTO
from src.resources.responses.response import Response

class IAuthRepositoryAbstract(ABC):

    @abstractmethod
    async def login(self, auth_login_dto: AuthLoginDTO) -> Response:
        pass

    @abstractmethod
    async def logout(self, auth_logout_dto: AuthLogoutDTO) -> Response:
        pass
       
    @abstractmethod
    async def verify_code_login(self, auth_verify: AuthVerifyCodeDTO) -> Response:
        pass
    
    @abstractmethod
    async def verify_code_email(self, auth_verify: AuthVerifyCodeDTO) -> Response:
        pass
    


