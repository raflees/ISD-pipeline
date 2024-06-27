from datetime import datetime

from event_detector.entities import LocalState

def test_retrieve_state_file_exists():
    local_state = LocalState(state_path='tests/test_data/local_state.json')
    assert local_state.state == {"file1": {"last_modified": "2024-05-01T20:14:00"}}

def test_get_file_last_modified_datetime():
    local_state = LocalState(state_path='tests/test_data/local_state.json')
    assert local_state.get_last_modified_datetime('file1') == datetime(2024, 5, 1, 20, 14, 0)
    assert local_state.get_last_modified_datetime('file_not_exists') == None

def test_retrieve_state_file_not_exists():
    local_state = LocalState(state_path='tests/test_data/i_dont_exist.json')
    assert local_state.state == {}