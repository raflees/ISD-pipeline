from abc import ABC, abstractmethod
from datetime import datetime

from typing import Optional

class BaseState(ABC):
    def __init__(self, state_format="json", datetime_format="%Y-%m-%d %H:%M:%S") -> None:
        self.state: dict = {}
        self.datetime_format: str = datetime_format
        self.state_format: str = state_format
    
    @abstractmethod
    def _retrieve_state(self) -> dict:
        pass
    
    @abstractmethod
    def write_state(self) -> None:
        pass

    def get_last_modified_datetime(self, key: str) -> Optional[datetime]:
        raw_last_modified = self.state.get(key, {}).get("last_modified", None)
        if raw_last_modified is not None:
            return datetime.strptime(raw_last_modified, self.datetime_format)
        return None

    def set_last_modified_datetime(self, key: str, dt: datetime):
        if self.state.get(key, None) is None:
            self.state[key] = {}
        self.state[key]["last_modified"] = dt.strftime(self.datetime_format)