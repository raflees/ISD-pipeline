import logging
from os import listdir
from os.path import join, isfile, splitext
from typing import Tuple

from google.cloud import bigquery

from ingest.interfaces import DataLoader

class FileBigQueryLoader(DataLoader):
    def __init__(self, config):
        super().__init__(config)
        self._client = self._get_client()
    
    @staticmethod
    def _get_client() -> bigquery.Client:
        return bigquery.Client()

    def load_data(self, source_files_dir):
        for file in self._get_files_to_load(source_files_dir):
            self._load_file(file)
    
    def _get_files_to_load(self, source_files_dir) -> Tuple[str]:
        files_to_load = []
        for file in self._list_files_in_dir(source_files_dir):
            _, extension = splitext(file)
            if (extension == ".csv" or extension == ""):
                files_to_load.append(join(source_files_dir, file))
        return tuple(files_to_load)
    
    @staticmethod
    def _list_files_in_dir(files_dir: str):
        return [file_path for file_path in listdir(files_dir) if isfile(join(files_dir, file_path))]

    def _load_file(self, file_to_load: str):
        table_id = self._get_table_id()
        job_config = self._get_load_job_config()
        logging.info(f"Loading file {file_to_load} to table {table_id}")
        with open(file_to_load, "rb") as source_file:
            load_job = self._client.load_table_from_file(source_file, table_id, job_config=job_config)
        load_job.result()

    @staticmethod
    def _get_load_job_config() -> bigquery.LoadJobConfig:
        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.CSV, skip_leading_rows=1, autodetect=True,
        )
        return job_config
    
    def _get_table_id(self) -> str:
        project_id = self._config['project_id']
        bq_dataset = self._config['bigquery']['dataset']
        bq_table = self._config['bigquery']['table']
        return f"{project_id}.{bq_dataset}.{bq_table}"