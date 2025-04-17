import os
from google.cloud import storage

bucket_name = os.getenv("GCS_BUCKET_NAME")

class GCSClient:
    def __init__(self):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GCS_CREDENTIALS_JSON")
        self.client = storage.Client()
        self.bucket = self.client.bucket(bucket_name)

    def upload_file(self, local_path, destination_name):
        blob = self.bucket.blob(destination_name)
        blob.upload_from_filename(local_path)
        blob.make_public()
        return f"https://storage.googleapis.com/{bucket_name}/{destination_name}"
