from abc import ABC, abstractmethod
from datetime import datetime

class BaseState(ABC):
    def __init__(self):
        self._state: dict = {}
    
    @abstractmethod
    def retrive_state(self) -> dict:
        pass

    @abstractmethod   
    def get_last_modified_datetime(self, key: str) -> datetime:
        pass
    
    @abstractmethod
    def set_last_modified_datetime(self, key: str, dt: datetime) -> None:
        pass

    def update_state(self) -> None:
        self._state = self.retrive_state()
    
    @abstractmethod
    def write_state(self) -> None:
        pass
    
    @property
    def state(self) -> dict:
        if self._state == {}:
            self.update_state()
        return self._state