from unittest.mock import Mock

from google.cloud import bigquery
import pytest

from ingest.entities import FileCloudStorageLoader

config = {
    "project_id": "test-project",
    "storage": {
        "bucket": "gs://test-bucket/"
    }
}

def test_load_data():
    loader = FileCloudStorageLoader(config)
    loader._load_file = Mock()
    loader.load_data("tests/test_data/")
    loader._load_file.assert_any_call("tests/test_data/sample_csv.csv")
    loader._load_file.assert_any_call("tests/test_data/csv_no_header.csv")

@pytest.fixture(autouse=True)
def mock_get_client(monkeypatch):
    class MockClient:
        pass
    monkeypatch.setattr(FileCloudStorageLoader, "_get_client", lambda self: MockClient())
