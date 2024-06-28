from abc import ABC, abstractmethod
import requests
from typing import Iterable
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from interfaces import BaseTap, BaseState

class HTTPBaseTap(BaseTap, ABC):
    def __init__(self, base_url: str, pattern: str, state: BaseState):
        super().__init__(pattern, state)
        self.base_url = base_url
    
    @abstractmethod
    def get_target_files(self) -> Iterable[str]:
        """
        Returns all files that should be downloaded in a form of a list of urls
        """
        pass
    
    def get_changed_files() -> Iterable[str]:
        super().get_changed_files()

    def write_state(self):
        super().write_state()
    
    @staticmethod
    def _get_soup_from_url(url: str) -> BeautifulSoup:
        response = requests.get(url)
        return BeautifulSoup(response.text, features="lxml")
    
    @staticmethod
    def _get_join_url(url: str, ref: str):
        return urljoin(url, ref)
    
    def _is_url_valid_for_search(self, base_url: str, ref: str):
        url = self._get_join_url(base_url, ref)

        # URL redirects or goes upstream
        if not url.startswith(base_url): return False
        # URL adds parameter to the page
        if url.startswith("?"): return False
        return True