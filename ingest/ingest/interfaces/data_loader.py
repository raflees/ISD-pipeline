from abc import ABC, abstractmethod

class DataLoader(ABC):
    def __init__(self, config: dict):
        self._config = config
    
    @abstractmethod
    def load_data(source_files_dir: str) -> None:
        pass