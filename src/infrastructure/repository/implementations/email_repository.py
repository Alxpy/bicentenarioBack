from src.core.abstractions.infrastructure.repository.email_repository_abstract import IEmailRepositoryAbstract
from src.resources.responses.response import Response
from src.resources.email.email_send_code_html import get_email_send_code_html, get_email_send_verify_html
from src.presentation.dto.email_dto import EmailDTO
from src.infrastructure.queries.user_queries import CREATE_USER_CODE
from src.infrastructure.constants.http_codes import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR
from src.infrastructure.constants.email_constants import *
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import base64
import random

class EmailRepository(IEmailRepositoryAbstract):

    def __init__(self, connection, connection_email):
        self.connection = connection
        self.connection_email = connection_email

    def generate_code(self) -> str:
        """Genera un código de verificación de 6 dígitos"""
        return ''.join(str(random.randint(0, 9)) for _ in range(6))
    
    def _validate_email(self, email: str) -> bool:
        """Valida que el email tenga un formato válido"""
        return email and '@' in email
    
    def _create_email_message(self, to: str, subject: str, body: str) -> MIMEMultipart:
        """Crea el objeto MIMEMultipart para el correo electrónico"""
        sender = os.getenv('GMAIL_SENDER')
        message = MIMEMultipart()
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        message.attach(MIMEText(body, 'html'))
        return message
    
    def _send_email(self, message: MIMEMultipart) -> dict:
        """Envía el correo electrónico a través de la API de Gmail"""
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        return self.connection_email.users().messages().send(
            userId="me", 
            body={'raw': raw_message}
        ).execute()
    
    def _store_verification_code(self, email: str, code: str) -> None:
        """Almacena el código de verificación en la base de datos"""
        with self.connection.cursor() as cursor:
            cursor.execute(CREATE_USER_CODE, (code, email))
            self.connection.commit()
    
    async def _send_verification_email(
        self, 
        email: EmailDTO, 
        subject: str, 
        body_generator: callable
    ) -> Response:
        """Método base para enviar emails de verificación"""
        print(f"Enviando correo a: {email.email}")
        
        try:
            if not self._validate_email(email.email):
                print("Dirección de correo no válida")
                return Response(
                    status=HTTP_400_BAD_REQUEST,
                    success=False,
                    message=INVALID_EMAIL_MSG,
                    data=None
                )

            verification_code = self.generate_code()
            message = self._create_email_message(
                to=email.email,
                subject=subject,
                body=body_generator(verification_code)
            )

            result = self._send_email(message)
            print(f'Message Id: {result["id"]}')
            
            self._store_verification_code(email.email, verification_code)
            
            return Response(
                status=HTTP_200_OK,
                success=True,
                message=EMAIL_SENT_SUCCESS_MSG,
                data={"message_id": result["id"]}
            )

        except Exception as e:
            print(f"Error al enviar correo: {e}")
            return Response(
                status=HTTP_500_INTERNAL_SERVER_ERROR,
                success=False,
                message=EMAIL_SEND_ERROR_MSG,
                data={"error": str(e)}
            )
    
    async def sendEmail_to_notify_new_login(self, email: EmailDTO) -> Response:
        """Envía email para notificar nuevo inicio de sesión"""
        return await self._send_verification_email(
            email=email,
            subject='Código de Inicio de Sesión',
            body_generator=get_email_send_verify_html
        )
        
    async def sendEmail_to_change_password(self, email: EmailDTO) -> Response:
        """Envía email para cambio de contraseña"""
        return await self._send_verification_email(
            email=email,
            subject='Cambio de contraseña',
            body_generator=get_email_send_code_html
        )
    
    async def sendEmail_to_verify_email(self, email: EmailDTO) -> Response:
        """Envía email para verificación de correo electrónico"""
        return await self._send_verification_email(
            email=email,
            subject='Verificación de correo electrónico',
            body_generator=get_email_send_code_html
        )