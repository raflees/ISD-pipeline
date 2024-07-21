from datetime import datetime
from ftplib import FTP
import re
from typing import Iterable, Optional, Tuple

from event_detector.interfaces.base_tap import BaseTap
from event_detector.interfaces.base_state import BaseState
from event_detector.entities.files.ftp_file import FTPFile

class FTPTap(BaseTap):
    def __init__(
            self,
            host: str,
            pattern: str,
            state: BaseState,
            user: Optional[str] = None,
            password: Optional[str] = None,
            dirpath: str = "/",
            ):
        super().__init__(pattern, state)
        self.dirpath = dirpath
        self.host = host
        self.password = password
        self.user = user

        self.ftp_server = FTP()
        self.ftp_server.host = host
        self.connect()
    
    def connect(self) -> None:
        self.ftp_server.connect()
        if self.user is not None and self.password is not None:
            self.ftp_server.login(user=self.user, passwd=self.password)
        else:
            self.ftp_server.login()
        self.ftp_server.cwd(self.dirpath)
    
    def get_file_list(self) -> Iterable[Tuple[str, dict]]:
        return self.ftp_server.mlsd()
    
    def get_changed_files(self) -> Iterable[FTPFile]:
        for file_name, facts in self.get_file_list():
            match = re.findall(self.pattern, file_name)
            if len(match) > 0:
                file_modified_datetime = datetime.strptime(facts['modify'], '%Y%m%d%H%M%S')
                if self._is_file_modified(file_name, file_modified_datetime):
                    yield FTPFile(file_name, self.dirpath+file_name, file_modified_datetime)
    
    def _is_file_modified(self, file: str, file_modified_datetime: datetime) -> bool:
        last_modified_datetime = self.state.get_last_modified_datetime(file)
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