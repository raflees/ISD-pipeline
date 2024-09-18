from os.path import splitext
import logging

from google.cloud import storage # type: ignore

from ingest.interfaces import FilesDataLoader

class FileCloudStorageLoader(FilesDataLoader):
    def __init__(self, config):
        super().__init__(config)
        self._client = self._get_client()
    
    @staticmethod
    def _get_client() -> storage.Client:
        return storage.Client()

    def _load_file(self, file_to_load: str):
        bucket_id = self._get_bucket_id()
        bucket_obj = self._client.bucket(bucket_id)
        file_name = self._add_extension_to_file_if_none(file_to_load)
        logging.info(f"Loading file {file_to_load} to bucket {bucket_id}")
        bucket_obj.blob(file_name).upload_from_filename(file_to_load)
    
    def _get_bucket_id(self) -> str:
        return self._config["storage"]["bucket"]
    
    @staticmethod
    def _add_extension_to_file_if_none(file_path) -> str:
        file_name, extension = splitext(file_path)
        if extension == "":
            extension = ".csv"
        return f"{file_name}{extension}"
