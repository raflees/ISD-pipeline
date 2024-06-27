from abc import ABC, abstractmethod

class BaseState(ABC):
    def __init__(self):
        self._state: dict = {}
    
    @abstractmethod
    def retrive_state(self) -> dict:
        pass
    
    @property
    def state(self) -> dict:
        if self._state == {}:
            self._state = self.retrive_state()
        return self._state