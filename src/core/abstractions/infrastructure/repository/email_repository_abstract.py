from abc import ABC, abstractmethod
from src.presentation.dto.email_dto import EmailDTO

class IEmailRepositoryAbstract(ABC):

    @abstractmethod
    async def sendEmail_to_verify_email(self, email: EmailDTO) -> bool:
        pass
    @abstractmethod
    async def sendEmail_to_change_password(self, email: EmailDTO) -> bool:
        pass
    @abstractmethod
    async def sendEmail_to_notify_new_login(self, email: EmailDTO) -> bool:
        pass
    


