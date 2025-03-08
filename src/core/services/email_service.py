from src.core.abstractions.services.email_service_abstract import IEmailServiceAbstract
from src.core.abstractions.infrastructure.repository.email_repository_abstract import IEmailRepositoryAbstract
from src.presentation.dto.email_dto import EmailDTO

class EmailService(IEmailServiceAbstract):

    def __init__(self, email_repository: IEmailRepositoryAbstract):
        self.email_repository = email_repository

    async def sendEmail_to_verify_email(self, email: EmailDTO) -> bool:
        return await self.email_repository.sendEmail_to_verify_email(email)
    
    async def sendEmail_to_change_password(self, email: EmailDTO) -> bool:
        return await self.email_repository.sendEmail_to_change_password(email)
    
    async def sendEmail_to_notify_new_login(self, email: EmailDTO) -> bool:
        return await self.email_repository.sendEmail_to_notify_new_login(email)

    
    async def sendEmail_to_verify_email(self, email: EmailDTO) -> bool:
        return await self.email_repository.sendEmail_to_verify_email(email)

