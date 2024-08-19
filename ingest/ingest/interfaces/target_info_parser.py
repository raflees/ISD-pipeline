from abc import ABC, abstractmethod
from typing import Iterable

class TargetInfoParser(ABC):
    def __init__(self, config: dict):
        self.config = config
    
    @abstractmethod
    def parse_target_info(self) -> Iterable[dict]:
        pass