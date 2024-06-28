import re
from typing import Iterable, List
from urllib.parse import urljoin

from interfaces import BaseState
from entities.taps.http_base_tap import HTTPBaseTap

class HTTPRepoTap(HTTPBaseTap):
    def __init__(self, base_url: str, pattern: str, state: BaseState):
        super().__init__(base_url, pattern, state)
        
    def get_target_files(self) -> Iterable[str]:
        file_list = []
        self._get_target_files(self.base_url, file_list)
        print(file_list)
        return file_list
    
    def _get_target_files(self, url: str, file_list: list) -> None:
        soup = self._get_soup_from_url(url)
        candidate_links: List[str] = soup.find_all("a")
        print(self.pattern)
        for tag in candidate_links:
            link = tag.attrs.get("href", None)
            if link is None or not self._is_url_valid_for_search(url, link):
                continue
            
            next_url = self._get_join_url(url, link)
            print("Checking", next_url)
            if re.search(self.pattern, next_url) is not None:  # Match
                file_list.append(next_url)
                print("Match")
            if next_url.endswith("/"): # New URL
                self._get_target_files(next_url, file_list)
            

    def get_changed_files() -> Iterable[str]:
        super().get_changed_files()

    def write_state(self):
        super().write_state()