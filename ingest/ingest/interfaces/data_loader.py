from abc import ABC, abstractmethod

class DataLoader(ABC):
    def __init__(self, config: dict, local_target_paths: list):
        self.config = config
        self.local_target_paths: list
    
    @abstractmethod
    def load_data() -> None:
        pass