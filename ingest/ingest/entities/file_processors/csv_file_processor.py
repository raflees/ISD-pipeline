import logging
from os import makedirs
from os.path import basename, join, splitext
import pandas as pd
from typing import List, Literal, Optional

from ingest.interfaces import FileProcessor
from ingest.entities import EncapsulateJson, IngestTimestamp

class CSVFileProcessor(FileProcessor):
    def __init__(self,
                 local_target_paths,
                 processing_strategies,
                 output_dir,
                 override_header: Optional[List[str]] = None,
                 skip_lines: int = 0):
        super().__init__(local_target_paths, processing_strategies, output_dir)
        self._override_header = override_header
        self._skip_lines = skip_lines
        self._make_output_dir()

    @property
    def _processing_strategies_catalog(self):
        return {
            "encapsulate_json": EncapsulateJson,
            "ingest_timestamp": IngestTimestamp,
        }
    
    def _make_output_dir(self):
        try:
            makedirs(self._output_dir)
        except FileExistsError:
            pass

    def _process_file(self, path: str):
        file_name = basename(path)
        df = self._read_file_content(path)
        for strategy in self._processing_strategies:
            df = strategy.process_data(df)
        self._save_file(df, file_name)
    
    def _read_file_content(self, input_path: str) -> pd.DataFrame:
        logging.info(f"Reading file {input_path}")
        header: Optional[Literal['infer']] = None if self._override_header is not None else 'infer'
        try:
            df = pd.read_csv(input_path, header=header, names=self._override_header, skiprows=self._skip_lines)
        except:
            df = pd.read_table(input_path, header=header, names=self._override_header, skiprows=self._skip_lines)
        return df
    
    def _save_file(self, df: pd.DataFrame, file_name: str):
        full_output_file_path = join(self._output_dir, file_name)
        logging.info(f"Saving file to {full_output_file_path}")
        df.to_csv(full_output_file_path, index=False)
    
    @staticmethod
    def _get_file_name_with_csv_ext(file_name: str) -> str:
        base_name, extension = splitext(file_name)
        if extension == ".csv":
            return file_name
        elif extension == "":
            return f"{base_name}.csv"
        else:
            return f"{base_name}_{extension.lstrip('.')}.csv"