from google.cloud import storage
from typing import Optional, Union
from google.api_core.exceptions import NotFound

GOOGLE_KEY_ENV_VAR = "GOOGLE_APPLICATION_CREDENTIALS"

class GCSClient:
    def __init__(self, bucket_name: str, credentials: Optional[Union[str, dict]] = None):
        self.bucket_name = bucket_name
        self.client = storage.Client.from_service_account_json(credentials) if isinstance(credentials, str) else storage.Client(credentials=credentials)

    def upload_file(self, file_path: str, destination_blob_name: str):
        bucket = self.client.bucket(self.bucket_name)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(file_path)
        
    def download_file(self, source_blob_name: str, destination_file_path: str):
        bucket = self.client.bucket(self.bucket_name)
        blob = bucket.blob(source_blob_name)
        blob.download_to_filename(destination_file_path)

    def file_exists(self, blob_name: str) -> bool:
        bucket = self.client.bucket(self.bucket_name)
        try:
            blob = bucket.blob(blob_name)
            return blob.exists()
        except NotFound:
            return False