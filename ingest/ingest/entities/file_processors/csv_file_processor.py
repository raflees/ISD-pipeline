import logging
from os import makedirs
from os.path import basename, join, splitext
import pandas as pd

from ingest.interfaces import FileProcessor
from ingest.entities import EncapsulateJson

class CSVFileProcessor(FileProcessor):
    @property
    def _processing_strategies_catalog(self):
        return {
            "encapsulate_json": EncapsulateJson
        }

    def _process_file(self, path: str):
        file_name = basename(path)
        df = self._read_file_content(path)
        for strategy in self._processing_strategies:
            df = strategy.process_data(df)
        self._save_file(df, file_name)
    
    def _read_file_content(self, input_path: str) -> pd.DataFrame:
        logging.info(f"Reading file {input_path}")
        return pd.read_csv(input_path)
    
    def _save_file(self, df: pd.DataFrame, file_name: str):
        makedirs(self._output_dir)
        full_output_file_path = join(self._output_dir, file_name)
        print("Saving file to", full_output_file_path)
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