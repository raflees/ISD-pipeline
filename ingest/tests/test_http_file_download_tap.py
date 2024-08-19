from os import makedirs, walk
from os.path import basename, join
import shutil

from ingest.entities import HTTPFileDownloadTap, CSVFileProcessor

def test_is_compressed_file():
    assert HTTPFileDownloadTap._is_compressed_file("i_am_compressed.gz")
    assert HTTPFileDownloadTap._is_compressed_file("i_am_compressed.zip")
    assert HTTPFileDownloadTap._is_compressed_file("i_am_compressed.rar")
    assert not HTTPFileDownloadTap._is_compressed_file("i_am_not_compressed.json")
    assert not HTTPFileDownloadTap._is_compressed_file("i_am_not_compressed.csv")

def test_files_are_downloaded_no_processing(monkeypatch, tmpdir):
    download_dir = join(tmpdir, '.download')
    patch_download_dir(monkeypatch, download_dir)
    patch_download_call(monkeypatch)
    patch_save_file(monkeypatch)

    config = {"processing_strategies": []}
    tap = HTTPFileDownloadTap(config, [{"file_url": "https://test_url.com/csv_no_header.gz", "file_name": "csv_no_header.gz"}])
    tap.ingest_data()

    dir_path, _, files = walk(download_dir).__next__()
    downloaded_files = [join(dir_path, file_path) for file_path in files]
    assert tap.downloaded_paths == [join(download_dir, "csv_no_header.gz")]

def mock_download_file(self: HTTPFileDownloadTap, remote_file_url, local_file_path):
    file_name = basename(local_file_path)
    src_path = join("tests", "test_data", file_name)
    dest_path = join(self._download_dir, file_name)
    with open(src_path, "rb") as src:
        with open(dest_path, "wb") as dest:
            shutil.copyfileobj(src, dest)

def patch_download_call(monkeypatch):    
    monkeypatch.setattr(HTTPFileDownloadTap, "_download_file", mock_download_file)

def patch_download_dir(monkeypatch, download_dir):
    monkeypatch.setattr(HTTPFileDownloadTap, "_download_dir", download_dir)

def patch_save_file(monkeypatch):
    monkeypatch.setattr(CSVFileProcessor, "_save_file", lambda self, df, file_name: None)

def print_dir(path):
    for base_dir, dir_list, file_list in walk(path):
        print(base_dir, dir_list, file_list)