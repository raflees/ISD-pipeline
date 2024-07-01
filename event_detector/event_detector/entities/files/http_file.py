from datetime import datetime
from typing import Union

from event_detector.interfaces import BaseFile

class HTTPFile(BaseFile):
    def __init__(self, name: str, url: str, last_modified: Union[str, datetime]):
        super().__init__(name, last_modified)
        self.url = url
    
    def to_dict(self):
        return {
            "file_name": self.name,
            "url": self.url,
            "last_modified": self.last_modified
        }