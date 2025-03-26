from src.infrastructure.repository.connection import get_connection
from src.infrastructure.repository.connection_mail import get_gmail_service


def get_db_connection():
    connection = None
    try:
        connection = get_connection()
        yield connection
    finally:
        if connection is not None:
            connection.close()  
            
def get_mail_service():
    mail_service = None
    try:
        mail_service = get_gmail_service()
        yield mail_service
    finally:
        if mail_service is not None:
            mail_service.close()