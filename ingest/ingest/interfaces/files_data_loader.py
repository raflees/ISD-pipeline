from abc import abstractmethod
from os import listdir
from os.path import join, isfile, splitext
from typing import Tuple

from ingest.interfaces.data_loader import DataLoader

class FilesDataLoader(DataLoader):
    def load_data(self, source_files_dir):
        for file in self._get_files_to_load(source_files_dir):
            self._load_file(file)
    
    def _get_files_to_load(self, source_files_dir) -> Tuple[str]:
        files_to_load = []
        for file in self._list_files_in_dir(source_files_dir):
            _, extension = splitext(file)
            if (extension == ".csv" or extension == ""):
                files_to_load.append(join(source_files_dir, file))
        return tuple(files_to_load)
    
    @staticmethod
    def _list_files_in_dir(files_dir: str):
        return [file_path for file_path in listdir(files_dir) if isfile(join(files_dir, file_path))]
    
    @abstractmethod
    def _load_file(self, source_files_dir: str):
        pass