from abc import ABC, abstractmethod
import pandas as pd
from typing import Dict, List, Optional

from ingest.interfaces.process_strategy import ProcessStrategy

class IngestTap(ABC):
    def __init__(self, target_information: List[dict]):
        self._target_information = target_information
    
    def ingest_data(self):
        self._ingest_data()
        self._process_data()

    @abstractmethod
    def _ingest_data(self) -> None:
        pass

    @abstractmethod
    def _process_data(self):
        pass