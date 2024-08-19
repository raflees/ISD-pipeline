from unittest.mock import Mock

from google.cloud import bigquery
import pytest

from ingest.entities import FileBigQueryLoader

config = {
    "project_id": "test-project",
    "bigquery": {
        "dataset": "test_dataset",
        "table": "test_table"
    }
}

def test_get_table_id():
    loader = FileBigQueryLoader(config)
    assert loader._get_table_id() == "`test-project.test_dataset.test_table`"

def test_load_job_config():
    loader = FileBigQueryLoader(config)
    expected_job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV, skip_leading_rows=1, autodetect=True,
    )
    job_config = loader._get_load_job_config()
    assert job_config.source_format == expected_job_config.source_format
    assert job_config.skip_leading_rows == expected_job_config.skip_leading_rows
    assert job_config.autodetect == expected_job_config.autodetect
    
def test_list_files_to_load():
    loader = FileBigQueryLoader(config)
    files_to_load = loader._get_files_to_load("tests/test_data/")
    assert files_to_load == (
        "tests/test_data/csv_no_header.csv",
        "tests/test_data/sample_csv.csv"
        )

def test_load_data():
    loader = FileBigQueryLoader(config)
    loader._load_file = Mock()
    loader.load_data("tests/test_data/")
    loader._load_file.assert_any_call("tests/test_data/sample_csv.csv")
    loader._load_file.assert_any_call("tests/test_data/csv_no_header.csv")

@pytest.fixture(autouse=True)
def mock_get_client(monkeypatch):
    class MockClient:
        pass
    monkeypatch.setattr(FileBigQueryLoader, "_get_client", lambda self: MockClient())