from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, Union

from event_detector.helper_methods import parse_datetime

class BaseFile(ABC):
    def __init__(self, name: str, last_modified: Union[datetime, str]):
        self.name = name
        self.last_modified: Optional[datetime] = None
        if type(last_modified) == str:
            self.last_modified = parse_datetime(last_modified)
        if type(last_modified) == datetime:
            self.last_modified = last_modified
        

    @abstractmethod
    def to_dict(self) -> dict:
        pass

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __str__(self):
        return str(self.to_dict())

    def __hash__(self):
        return hash(str(self))

    def __repr__(self):
        return str(self.to_dict())