from abc import ABC, abstractmethod

class BaseState(ABC):
    def __init__(self):
        self.state: dict = {}
    
    @abstractmethod
    def retrive_state(self):
        pass
    
    @property
    def state(self) -> dict:
        if self.state == {}:
            self.retrive_state()