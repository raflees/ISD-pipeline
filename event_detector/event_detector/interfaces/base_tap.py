from abc import ABC, abstractmethod
from typing import Iterable

from .base_state import BaseState
from .base_file import BaseFile

class BaseTap(ABC):
    def __init__(self, pattern: str, state: BaseState):
        self.pattern = pattern
        self.state = state
    
    @abstractmethod
    def get_changed_files(self) -> Iterable[BaseFile]:
        pass
    
    def write_state(self):
        self.state.write_state()