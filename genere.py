from google.cloud import storage
import os
from dotenv import load_dotenv

class GCSClient:
    def __init__(self):
        load_dotenv()
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GCS_CREDENTIALS_JSON")
        self.bucket_name = os.getenv("GCS_BUCKET_NAME")
        self.client = storage.Client()
        self.bucket = self.client.bucket(self.bucket_name)

    def upload_file(self, local_path, destination_blob_name):
        """Sube un archivo al bucket de GCS"""
        blob = self.bucket.blob(destination_blob_name)
        blob.upload_from_filename(local_path)
        blob.make_public()
        return blob.public_url


client = GCSClient()
url = client.upload_file("public/imagenes/alex.jpg", "alex2")
print("✅ Archivo subido. Enlace público:", url)

