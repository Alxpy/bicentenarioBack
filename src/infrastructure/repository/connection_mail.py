import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request


credentials_file =  os.getenv('CREDENTIALS_FILE')
token_file =  os.getenv('GMAIL_TOKEN')
scopes = [os.getenv('GMAIL_SCOPE')]

def authenticate():
    creds = None
    if os.path.exists(token_file):
        with open(token_file, 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_file, scopes)
            creds = flow.run_local_server(port=0)

        with open(token_file, 'wb') as token:
            pickle.dump(creds, token)

    return creds

def get_gmail_service():
    """Devuelve el servicio Gmail autenticado sin caché de archivo."""
    try:
        creds = authenticate()  # Llama a tu función de autenticación
        service = build('gmail', 'v1', credentials=creds, cache_discovery=False)  # Desactiva el caché
        return service
    except HttpError as error:
        print(f"❌ Error en la conexión con Gmail: {error}")
        return None
