from datetime import datetime
import json
import pytest

from event_detector.entities import CloudStorageState

with open("tests/test_data/local_state.json") as f:
    json_state = json.load(f)

class MockClient():
    pass

class MockBlob():
    def download_as_bytes(self):
        return json.dumps(json_state).encode("utf-8")
    
    def upload_from_string(self):
        pass

@pytest.fixture(autouse=True)
def patch_cloud_storage_state(monkeypatch):
    monkeypatch.setattr(CloudStorageState, '_get_client', lambda self, project_id: MockClient())
    monkeypatch.setattr(CloudStorageState, '_get_blob', lambda self, bucket, blob: MockBlob())

def test_retrieve_state_file():
    cloud_state = CloudStorageState("test_project", "test_bucket", "state.json")
    assert cloud_state.state == {
        "file1": {"last_modified": "2024-05-01 20:14:00"},
        "http://www.test_url.com/2020/2020.gz": {"last_modified": "2018-08-26 02:55:00"}
        }

def test_get_file_last_modified_datetime():
    cloud_state = CloudStorageState("test_project", "test_bucket", "state.json")
    assert cloud_state.get_last_modified_datetime('file1') == datetime(2024, 5, 1, 20, 14, 0)
    assert cloud_state.get_last_modified_datetime('file_not_exists') == None

def test_set_state():
    cloud_state = CloudStorageState("test_project", "test_bucket", "state.json")
    
    file1_new_modified_datetime = datetime(2024, 12, 31, 12, 0, 0)
    file2_new_modified_datetime = datetime(2025, 6, 30, 12, 0, 0)

    cloud_state.set_last_modified_datetime("file1", file1_new_modified_datetime)
    cloud_state.set_last_modified_datetime("file2", file2_new_modified_datetime)
    
    assert cloud_state.state == {
            "file1": {"last_modified": file1_new_modified_datetime.strftime(cloud_state.datetime_format)},
            "file2": {"last_modified": file2_new_modified_datetime.strftime(cloud_state.datetime_format)},
            "http://www.test_url.com/2020/2020.gz": {"last_modified": "2018-08-26 02:55:00"}
        }
        