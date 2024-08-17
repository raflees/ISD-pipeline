from abc import ABC, abstractmethod
from os.path import splitext
from typing import List, Optional

from ingest.interfaces import FileProcessor, ProcessStrategy

class IngestTap(ABC):
    def __init__(self, config: dict, target_information: List[dict]):
        self._target_information = target_information
        self._config = config
        self._processing_strategies: List[ProcessStrategy] = config["processing_strategies"]
    
    @abstractmethod
    def ingest_data(self, *args, **kwargs):
        pass

    @abstractmethod
    def _process_data(self, *args, **kwargs):
        pass

    @staticmethod
    def _is_compressed_file(file_path):
        extension = IngestTap._get_file_extension(file_path)
        return extension in (".gz", ".zip", ".rar")

    @staticmethod
    def _get_file_extension(file_path: str):
        _, extension = splitext(file_path)
        return extension
    
    @staticmethod
    def _get_file_processor(self, file_path: str) -> Optional[FileProcessor]:
        pass