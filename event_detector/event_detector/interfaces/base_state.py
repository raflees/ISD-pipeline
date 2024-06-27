from abc import ABC, abstractmethod
from datetime import datetime

class BaseState(ABC):
    def __init__(self):
        self._state: dict = {}
    
    @abstractmethod
    def retrive_state(self) -> dict:
        pass

    def get_last_modified_datetime(self, key: str) -> datetime:
        pass
    
    def set_last_modified_datetime(self, key: str, dt: datetime):
        pass
    
    @property
    def state(self) -> dict:
        if self._state == {}:
            self._state = self.retrive_state()
        return self._state