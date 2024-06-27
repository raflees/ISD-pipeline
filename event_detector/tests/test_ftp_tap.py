import pytest
from unittest.mock import patch, Mock

from event_detector.entities import FTPTap, LocalState

state = LocalState("tests/test_data/local_state.json")

def test_file_is_modified(monkeypatch):
    def patch_get_file_list(*args, **kwargs):
        return [
            ("file1", {"modify": "20240501201400"}),  # Was not modified
            ("file2", {"modify": "20240101120000"})   # Was modified
        ]

    monkeypatch.setattr(FTPTap, 'get_file_list', patch_get_file_list)
    monkeypatch.setattr(FTPTap, 'connect', lambda self: None)
    monkeypatch.setattr(FTPTap, 'download_file', lambda *args, **kwargs: None)

    tap = FTPTap("dummy_host", state)
    changed_files = tap.get_changed_files("file")
    assert set(changed_files) == set(["file2"])
    