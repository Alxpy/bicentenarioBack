from src.core.abstractions.infrastructure.repository.email_repository_abstract import IEmailRepositoryAbstract
from src.resources.email.email_send_code_html import get_email_send_code_html, get_email_send_verify_html
from src.presentation.dto.email_dto import EmailDTO
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import base64
import random

class EmailRepository(IEmailRepositoryAbstract):

    def __init__(self, conecction, connection_email):
        self.connection = conecction
        self.connection_email = connection_email

    def generate_code(self):
        code = ""
        for i in range(6):
            code += str(random.randint(0, 9))
        return code
    

    
    async def sendEmail_to_notify_new_login(self, email: EmailDTO) -> bool:
        print(f"Enviando correo a: {email.email}")

        try:
            sender = os.getenv('GMAIL_SENDER')
            to = email.email  
            if not to or '@' not in to:
                print("Dirección de correo no válida")
                return False

            subject = 'Verificación de correo electrónico'
            verification_code = self.generate_code()
            body = get_email_send_verify_html(verification_code)

            message = MIMEMultipart()
            message['to'] = to
            message['from'] = sender
            message['subject'] = subject

            msg = MIMEText(body, 'html') 
            message.attach(msg)

            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

            message = self.connection_email.users().messages().send(
                userId="me", 
                body={'raw': raw_message}
            ).execute()

            print(f'Message Id: {message["id"]}')

            with self.connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE usuario SET codeValidacion = %s 
                    WHERE correo = %s
                    """,
                    (verification_code, email.email)
                )
                self.connection.commit()
            
            return True

        except Exception as e:
            print(f"Error al enviar correo: {e}")
            return False

        
    async def sendEmail_to_change_password(self, email: EmailDTO) -> bool:
        pass
    
    async def sendEmail_to_verify_email(self, email: EmailDTO) -> bool:
        try:
            sender = os.getenv('GMAIL_SENDER')
            to = email.email  
            if not to or '@' not in to:
                print("Dirección de correo no válida")
                return False

            subject = 'Verificación de correo electrónico'
            verification_code = self.generate_code()
            body = get_email_send_code_html(verification_code)

            message = MIMEMultipart()
            message['to'] = to
            message['from'] = sender
            message['subject'] = subject

            msg = MIMEText(body, 'html') 
            message.attach(msg)

            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

            message = self.connection_email.users().messages().send(
                userId="me", 
                body={'raw': raw_message}
            ).execute()

            print(f'Message Id: {message["id"]}')

            with self.connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE usuario SET codeValidacion = %s 
                    WHERE correo = %s
                    """,
                    (verification_code, email.email)
                )
                self.connection.commit()
            
            return True
        except Exception as e:
            print(f"Error al enviar correo: {e}")
            return False
        
    


