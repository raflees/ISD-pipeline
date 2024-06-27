from abc import ABC, abstractmethod
from typing import Iterable

from .base_state import BaseState

class BaseTap(ABC):
    def __init__(self, state: BaseState):
        self.state = state

    @abstractmethod
    def download_file():
        pass
    
    @abstractmethod
    def get_changed_files(pattern: str) -> Iterable[str]:
        pass
    