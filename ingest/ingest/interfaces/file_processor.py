from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, Iterable, Optional, Union

import pandas as pd

from ingest.interfaces import ProcessStrategy

class FileProcessor(ABC):
    def __init__(self, 
                 local_target_paths: Union[Iterable[str], str],
                 processing_strategies: Iterable[str],
                 output_dir: Optional[str]):
        if isinstance(local_target_paths, str):
            self._local_target_paths = [local_target_paths,]
        else:
            self._local_target_paths = [path for path in local_target_paths]
        self._output_dir = output_dir or self._get_default_output_dir()
        self._processing_strategies = self._create_processing_strategies(processing_strategies)
    
    @property
    @abstractmethod
    def _processing_strategies_catalog(self) -> Dict[str, Callable[..., ProcessStrategy]]:
        return {}

    def _create_processing_strategies(self, processing_strategies: Iterable[str]) -> Iterable[ProcessStrategy]:
        try:
            return [self._processing_strategies_catalog[ps]() for ps in processing_strategies]
        except KeyError as e:
            msg = (f"Could not find one or more described processing strategies: {processing_strategies}\n" +
                   f"Accepted values: {list(self._processing_strategies_catalog.keys())}")
            raise ValueError(msg) from e

    @staticmethod
    def _get_default_output_dir() -> str:
        return "./output/"
    
    def process_data(self):
        for path in self._local_target_paths:
            self._process_file(path)
    
    @abstractmethod
    def _process_file(self, path: str):
        pass

    @abstractmethod
    def _read_file_content(self, input_path: str) -> pd.DataFrame:
        pass

    @abstractmethod
    def _save_file(self, df: pd.DataFrame, file_name: str):
        pass