from datetime import datetime
from ftplib import FTP
import re
from typing import Iterable

from interfaces.base_tap import BaseTap
from interfaces.base_state import BaseState

class FTPTap(BaseTap):
    def __init__(self, host: str, state: BaseState, user: str = None, password: str = None, dirpath="/"):
        self.host = host
        self.user = user
        self.password = password
        self.ftp_server = FTP(host)

        self.state = state
        
        self.ftp_server.connect()
        if user or password:
            self.ftp_server.login(user=user, password=password)
        else:
            self.ftp_server.login()
        self.ftp_server.cwd(dirpath)
    
    def download_file(self, filename: str) -> None:
        with open(f'/downloaded/{filename}', 'wb') as f:
           self.ftp_server.retrbinary("RETR " + filename, f.write)
    
    def get_changed_files(self, pattern: str) -> Iterable[str]:
        for file, facts in self.ftp_server.mlsd():
            match = re.findall(pattern, file)
            if len(match) > 0 and self._is_file_modifyed(file, facts):
                self.download_file()
                yield file
    
    def _is_file_modifyed(self, file: str, file_facts: dict) -> bool:
        last_modified_datetime = self.state.get(file, None)
        file_modified_datetime = datetime.strptime(file_facts.get('modify'), '%Y%m%d%H%M%S')
        if last_modified_datetime is None or file_modified_datetime is None:
            return True
        if last_modified_datetime < file_modified_datetime:
            return True
        return False

    def __del__(self):
        self.ftp_server.quit()