from datetime import datetime
from ftplib import FTP
import re
from typing import Iterable, Tuple

from interfaces.base_tap import BaseTap
from interfaces.base_state import BaseState

class FTPTap(BaseTap):
    def __init__(self, host: str, state: BaseState, user: str = None, password: str = None, dirpath="/"):
        self.dirpath = dirpath
        self.host = host
        self.password = password
        self.state = state
        self.user = user

        self.ftp_server = FTP()
        self.ftp_server.host = host
        self.connect()
    
    def connect(self) -> None:
        self.ftp_server.connect()
        if self.user or self.password:
            self.ftp_server.login(user=self.user, password=self.password)
        else:
            self.ftp_server.login()
        self.ftp_server.cwd(self.dirpath)

    def download_file(self, filename: str) -> None:
        with open(f'/downloaded/{filename}', 'wb') as f:
           self.ftp_server.retrbinary("RETR " + filename, f.write)
    
    def get_file_list(self) -> Iterable[Tuple[str, dict]]:
        return self.ftp_server.mlsd()
    
    def get_changed_files(self, pattern: str) -> Iterable[str]:
        for file, facts in self.get_file_list():
            match = re.findall(pattern, file)
            if len(match) > 0 and self._is_file_modified(file, facts):
                self.download_file()
                yield file
    
    def _is_file_modified(self, file: str, file_facts: dict) -> bool:
        last_modified_datetime = self.state.get_last_modified_datetime(file)
        file_modified_datetime = datetime.strptime(file_facts['modify'], '%Y%m%d%H%M%S')
        if last_modified_datetime is None or file_modified_datetime is None:
            return True
        if last_modified_datetime < file_modified_datetime:
            return True
        return False

    def __del__(self):
        try:
            self.ftp_server.quit()
        except:
            pass