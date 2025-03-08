from src.core.abstractions.infrastructure.repository.email_repository_abstract import IEmailRepositoryAbstract
from src.presentation.dto.email_dto import EmailDTO
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import base64

class EmailRepository(IEmailRepositoryAbstract):

    def __init__(self, conecction, connection_email):
        self.connection = conecction
        self.connection_email = connection_email


    async def sendEmail_to_verify_email(self, email: EmailDTO) -> bool:
        print(f"Enviando correo...{ email }")
        try:
            sender = os.getenv('GMAIL_SENDER')
            to = email.email  
            if not to or '@' not in to:
                print("Dirección de correo no válida")
                return False
            
            subject = 'Verificación de correo electrónico'
            body = 'Para verificar su correo electrónico haga click en el siguiente enlace'
            
            message = MIMEMultipart()
            message['to'] = to
            message['from'] = sender
            message['subject'] = subject
            
            msg = MIMEText(body)
            message.attach(msg)
            
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

            message = self.connection_email.users().messages().send(userId="me", body={'raw': raw_message}).execute()
            
            print(f'Message Id: {message["id"]}')
            return True

        except Exception as e:
            print(f"Error al enviar correo: {e}")
            return False

        
    async def sendEmail_to_change_password(self, email: EmailDTO) -> bool:
        pass


    async def sendEmail_to_notify_new_login(self, email: EmailDTO) -> bool:
        pass
    


