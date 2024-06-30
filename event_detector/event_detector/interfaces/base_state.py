from abc import ABC, abstractmethod
from datetime import datetime

class BaseState(ABC):
    def __init__(self):
        self.state: dict = self._retrieve_state()
    
    @abstractmethod
    def _retrieve_state(self) -> dict:
        pass

    @abstractmethod   
    def get_last_modified_datetime(self, key: str) -> datetime:
        pass
    
    @abstractmethod
    def set_last_modified_datetime(self, key: str, dt: datetime) -> None:
        pass
    
    @abstractmethod
    def write_state(self) -> None:
        pass