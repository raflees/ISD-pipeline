from abc import ABC, abstractmethod
from typing import List, Optional

from ingest.interfaces.process_strategy import ProcessStrategy

class IngestTap(ABC):
    def __init__(
            self,
            target_information: List[dict],
            staged_dir: str = None,
            output_dir: str = ".output/final/",
            processing_strategy: Optional[ProcessStrategy] = None
            ):
        self.output_dir = output_dir
        self.processing_strategy = processing_strategy
        self.staged_dir = staged_dir
        self.target_information = target_information
    
    @abstractmethod
    def ingest_data(self) -> None:
        pass

    @abstractmethod
    def _process_data(self):
        pass