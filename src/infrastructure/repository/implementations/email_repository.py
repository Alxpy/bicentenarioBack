from src.core.abstractions.infrastructure.repository.email_repository_abstract import IEmailRepositoryAbstract
from src.presentation.responses.response_factory import Response, success_response, error_response
from src.resources.email.email_send_code_html import get_email_send_code_html, get_email_send_verify_html
from src.presentation.dto.email_dto import EmailDTO
from src.infrastructure.queries.user_queries import CREATE_USER_CODE
from src.infrastructure.constants.http_codes import *
from src.infrastructure.constants.email_constants import *
from src.infrastructure.constants.messages import *
import os
import base64
import random
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

logger = logging.getLogger(__name__)

class EmailRepository(IEmailRepositoryAbstract):
    def __init__(self, connection, connection_email):
        self.connection = connection
        self.connection_email = connection_email

    def generate_code(self) -> str:
        """Genera un código de verificación de 6 dígitos"""
        return ''.join(str(random.randint(0, 9)) for _ in range(6))
    
    def _validate_email(self, email: str) -> bool:
        """Valida el formato del email"""
        return email and '@' in email
    
    def _create_email_message(self, to: str, subject: str, body: str) -> MIMEMultipart:
        """Construye el objeto email con formato MIME"""
        sender = os.getenv('GMAIL_SENDER')
        message = MIMEMultipart()
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        message.attach(MIMEText(body, 'html'))
        return message
    
    def _send_email(self, message: MIMEMultipart) -> dict:
        """Envía el email usando la API de Gmail"""
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        return self.connection_email.users().messages().send(
            userId="me", 
            body={'raw': raw_message}
        ).execute()
    
    def _store_verification_code(self, email: str, code: str) -> None:
        """Almacena el código en la base de datos"""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(CREATE_USER_CODE, (code, email))
                self.connection.commit()
        except Exception as e:
            logger.error("Error almacenando código de verificación: %s", e)
            raise

    async def _send_verification_email(
        self, 
        email: EmailDTO, 
        subject: str, 
        body_generator: callable
    ) -> Response:
        """Método base para envío de emails con verificación"""
        logger.info("Iniciando envío de email a: %s", email.email)
        try:
            if not self._validate_email(email.email):
                logger.warning("Email inválido: %s", email.email)
                return error_response(
                    message=INVALID_EMAIL_MSG,
                    status=HTTP_400_BAD_REQUEST
                )

            verification_code = self.generate_code()
            message = self._create_email_message(
                to=email.email,
                subject=subject,
                body=body_generator(verification_code)
            )
            
            send_result = self._send_email(message)
            logger.info("Email enviado correctamente. Message ID: %s", send_result["id"])
            
            self._store_verification_code(email.email, verification_code)
            
            return success_response(
                message=EMAIL_SENT_SUCCESS_MSG
            )
        except Exception as e:
            logger.error("Error enviando email: %s", str(e))
            return error_response(
                message=EMAIL_SEND_ERROR_MSG,
                status=HTTP_500_INTERNAL_SERVER_ERROR,
            )

    async def sendEmail_to_notify_new_login(self, email: EmailDTO) -> Response:
        """Notifica nuevo inicio de sesión"""
        return await self._send_verification_email(
            email=email,
            subject='Código de Inicio de Sesión',
            body_generator=get_email_send_verify_html
        )
        
    async def sendEmail_to_change_password(self, email: EmailDTO) -> Response:
        """Solicitud de cambio de contraseña"""
        return await self._send_verification_email(
            email=email,
            subject='Cambio de contraseña',
            body_generator=get_email_send_code_html
        )
    
    async def sendEmail_to_verify_email(self, email: EmailDTO) -> Response:
        """Verificación de dirección de correo"""
        return await self._send_verification_email(
            email=email,
            subject='Verificación de correo electrónico',
            body_generator=get_email_send_code_html
        )