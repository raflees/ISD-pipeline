from datetime import datetime
import json

from event_detector.entities import LocalState

def test_retrieve_state_file_exists():
    local_state = LocalState(state_path='tests/test_data/local_state.json')
    assert local_state.state == {
        "file1": {"last_modified": "2024-05-01 20:14:00"},
        "http://www.test_url.com/2020/2020.gz": {"last_modified": "2018-08-26 02:55:00"}
        }

def test_get_file_last_modified_datetime():
    local_state = LocalState(state_path='tests/test_data/local_state.json')
    assert local_state.get_last_modified_datetime('file1') == datetime(2024, 5, 1, 20, 14, 0)
    assert local_state.get_last_modified_datetime('file_not_exists') == None

def test_retrieve_state_file_not_exists():
    local_state = LocalState(state_path='tests/test_data/i_dont_exist.json')
    assert local_state.state == {}

def test_set_and_write_state(tmp_path):
    local_state = LocalState(state_path='tests/test_data/local_state.json')
    
    file1_new_modified_datetime = datetime(2024, 12, 31, 12, 0, 0)
    file2_new_modified_datetime = datetime(2025, 6, 30, 12, 0, 0)
    tmp_state_path = f"{tmp_path}/state/state.json"

    local_state.update_state()
    local_state.state_path = tmp_state_path
    local_state.set_last_modified_datetime("file1", file1_new_modified_datetime)
    local_state.set_last_modified_datetime("file2", file2_new_modified_datetime)

    local_state.write_state()

    with open(tmp_state_path) as f:
        written_state = json.load(f)
        format_str = local_state.datetime_format
        assert written_state == {
            "file1": {"last_modified": file1_new_modified_datetime.strftime(format_str)},
            "file2": {"last_modified": file2_new_modified_datetime.strftime(format_str)},
            "http://www.test_url.com/2020/2020.gz": {"last_modified": "2018-08-26 02:55:00"}
        }