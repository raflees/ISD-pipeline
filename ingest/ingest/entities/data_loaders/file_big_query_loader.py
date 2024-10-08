import logging
from os import listdir
from os.path import join, isfile, splitext
from typing import Tuple

from google.cloud import bigquery

from ingest.interfaces import FilesDataLoader

class FileBigQueryLoader(FilesDataLoader):
    def __init__(self, config):
        super().__init__(config)
        self._client = self._get_client()
    
    @staticmethod
    def _get_client() -> bigquery.Client:
        return bigquery.Client()

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