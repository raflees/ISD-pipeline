from datetime import datetime
from typing import Union

from event_detector.interfaces import BaseFile

class FTPFile(BaseFile):
    def __init__(self, name: str, remote_path: str, last_modified: Union[str, datetime]):
        super().__init__(name, last_modified)
        self.remote_path = remote_path
    
    def to_dict(self):
        return {
            "file_name": self.name,
            "remote_path": self.remote_path,
            "last_modified": self.last_modified
        }