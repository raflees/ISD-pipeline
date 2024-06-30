from datetime import datetime
import json

from google.cloud import storage

from interfaces import BaseState

class CloudStorageState(BaseState):
    def __init__(self, project_id: str, bucket: str, blob_path: str):
        super().__init__()
        self._client = self._get_client(project_id)
        self.state_blob = self._get_blob(bucket, blob_path)
        self.state = self._retrieve_state()

    @staticmethod
    def _get_client(project_id: str) -> storage.Client:
        return storage.Client(project_id)
    
    def _get_blob(self, bucket: str, blob_path: str) -> storage.Blob:
        bucket = self._client.bucket(bucket)
        return bucket.blob(blob_path)
    
    def _retrieve_state(self):
        raw_state = self.state_blob.download_as_bytes().decode("utf-8")
        if self.state_format == "json":
            return self._decode_json_state(raw_state)
        else:
            raise NotImplemented(f"Retrieval of state in a {self.state_format} is not implemented.")
    
    @staticmethod
    def _decode_json_state(raw_state: str) -> dict:
        return json.loads(raw_state)

    def write_state(self):
        self.state_blob.upload_from_string(json.dumps(self.state))