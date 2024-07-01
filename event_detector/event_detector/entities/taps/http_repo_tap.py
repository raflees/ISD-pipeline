import re
from typing import Iterable

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
        
    def get_target_files(self) -> Iterable[HTTPFile]:
        file_list = []
        self.searched_urls = set()
        self._get_target_files(self.base_url, file_list)
        return file_list
    
    def _get_target_files(self, url: str, file_list: list) -> None:
        self.searched_urls.add(url)
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
            if table_name_data == -1 or table_name_data is None: # Not an anchor
                continue
            
            link = table_name_data.attrs.get("href", None)
            if link is None or not self._is_url_valid_for_search(url, link):
                continue
            
            next_url = self._get_join_url(url, link)
            if next_url.endswith("/"): # New URL
                self._get_target_files(next_url, file_list)
            elif re.search(self.pattern, next_url) is not None:  # Match
                file = HTTPFile(
                    name=table_name_data.string.strip(),
                    url=next_url,
                    last_modified=table_row_contents[self.modified_col_num].string.strip(),
                )
                file_list.append(file)
            
    def get_changed_files(self) -> Iterable[HTTPFile]:
        all_downstream_files = self.get_target_files()
        for file in all_downstream_files:
            last_file_modified_datetime = self.state.get_last_modified_datetime(file.url)
            if last_file_modified_datetime is None or file.last_modified > last_file_modified_datetime:
                print(f"Identified modified file {file.url}")
                self.state.set_last_modified_datetime(file.url, file.last_modified)
                yield file