from bs4 import BeautifulSoup
import re
from typing import Iterable, List
from urllib.parse import urljoin

from interfaces import BaseState
from entities.files.http_file import HTTPFile
from entities.taps.http_base_tap import HTTPBaseTap

class HTTPRepoTap(HTTPBaseTap):
    DEFAULT_FILE_NAME_COL_NUM = 0
    DEFAULT_MODIFIED_COL_NUM = 1

    def __init__(self, base_url: str, pattern: str, state: BaseState):
        super().__init__(base_url, pattern, state)
        self.file_name_col_num = HTTPRepoTap.DEFAULT_FILE_NAME_COL_NUM
        self.modified_col_num = HTTPRepoTap.DEFAULT_MODIFIED_COL_NUM
        
    def get_target_files(self) -> Iterable[str]:
        file_list = []
        self._get_target_files(self.base_url, file_list)
        return file_list
    
    def _get_target_files(self, url: str, file_list: list) -> None:
        soup = self._get_soup_from_url(url)
        table_rows = soup.find_all("tr")

        for tr in table_rows:
            table_row_contents = [
                content
                for content in 
                tr.contents
                if content != "\n"
            ]

            table_name_data = table_row_contents[self.file_name_col_num].find("a")
            if table_name_data == -1: # Not an anchor
                continue
            
            link = table_name_data.attrs.get("href", None)
            if link is None or not self._is_url_valid_for_search(url, link):
                continue
            
            next_url = self._get_join_url(url, link)
            if next_url.endswith("/"): # New URL
                self._get_target_files(next_url, file_list)
            elif re.search(self.pattern, next_url) is not None:  # Match
                print(table_row_contents[self.modified_col_num].string.strip())
                file = HTTPFile(
                    name=table_name_data.string.strip(),
                    url=next_url,
                    last_modified=table_row_contents[self.modified_col_num].string.strip(),
                )
                file_list.append(file)
            

    def get_changed_files() -> Iterable[str]:
        super().get_changed_files()

    def write_state(self):
        super().write_state()