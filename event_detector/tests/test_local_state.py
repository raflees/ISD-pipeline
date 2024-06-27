from event_detector.entities import LocalState

def test_retrieve_state_file_exists():
    local_state = LocalState(state_path='tests/test_data/local_state.json')
    local_state.retrive_state()

    assert local_state.state == {"test_file": {"last_modified": "2024-05-01T20:14:00"}}

def test_retrieve_state_file_not_exists():
    local_state = LocalState(state_path='tests/test_data/i_dont_exist.json')
    local_state.retrive_state()

    assert local_state.state == {}