import requests
import os
from dotenv import load_dotenv

class GofileClient:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("GOFILE_API_KEY", "")
        self.fixed_server = os.getenv("GOFILE_FIXED_SERVER", "")

        self.server = self.fixed_server or self.get_best_server()

    def get_best_server(self):
        try:
            response = requests.get("https://api.gofile.io/getServer")
            response.raise_for_status()
            return response.json()["data"]["server"]
        except Exception as e:
            print("Error al obtener el servidor:", e)
            return None

    def get_upload_url(self):
        if not self.server:
            raise Exception("Servidor no disponible.")
        return f"https://{self.server}.gofile.io/uploadFile"

    def get_headers(self):
        if self.api_key:
            return {"Authorization": f"Bearer {self.api_key}"}
        return {}
