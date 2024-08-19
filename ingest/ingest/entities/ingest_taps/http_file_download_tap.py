import gzip
import logging
from os import makedirs
from os.path import basename, join, splitext
from typing import List
from urllib.request import urlretrieve

from ingest.interfaces import IngestTap
from ingest.entities import CSVFileProcessor

class HTTPFileDownloadTap(IngestTap):
    def __init__(self, config: dict, target_information: List[dict]):
        super().__init__(config, target_information)
        self._download_dir = self.download_dir()
        self.downloaded_paths: List[str] = []
        makedirs(self._download_dir)
    
    @property
    def download_dir(self):
        return ".downloaded/"
    
    def ingest_data(self):
        for target in self._target_information:
            downloaded_file_path = self._ingest_data(target)
            self.downloaded_paths.append(downloaded_file_path)
            if self._is_compressed_file(downloaded_file_path):
                self._process_compressed_file(downloaded_file_path)
            else:
                self._process_data(downloaded_file_path)

    def _ingest_data(self, target):
        file_url = target["file_url"]
        local_file_path = join(self._download_dir, target["file_name"])
        self._download_file(file_url, local_file_path)
        return local_file_path
    
    def _download_file(self, remote_file_url: str, local_file_path: str):
        urlretrieve(remote_file_url, local_file_path)

    def _process_data(self, local_file_path):
        processor = self._get_file_processor(local_file_path)
        if processor:
            processor.process_data()
    
    def _get_file_processor(self, local_file_path):
        extension = self._get_file_extension(local_file_path)
        if extension == ".csv" or extension == "":
            return CSVFileProcessor(local_file_path, self._processing_strategies, ".final/")
        else:
            logging.warning(f"Could not find a compatible file processor for {local_file_path}")

    def _process_compressed_file(self, path_to_zip: str):
        extracted_files = self._extract_and_list_files(path_to_zip)
        for file in extracted_files:
            self._process_data(file)

    def _extract_and_list_files(self, path_to_zip: str) -> List[str]:
        extension = self._get_file_extension(path_to_zip)
        if extension == ".gz":
            extracted_files = self._extract_and_list_gz_file(path_to_zip)
        else:
            raise NotImplementedError(f"Extraction for non-gz files is not implemented (got {path_to_zip})")
        return extracted_files
    
    def _extract_and_list_gz_file(self, path_to_gzip: str) -> List[str]:
        zip_file_name = basename(path_to_gzip)
        stripped_file_name, _ = splitext(zip_file_name)
        local_decompressed_file = join(self._download_dir, stripped_file_name)
        with gzip.open(path_to_gzip) as gz:
            with open(local_decompressed_file, "w") as f:
                f.write(gz.read().decode())
        return [local_decompressed_file,]