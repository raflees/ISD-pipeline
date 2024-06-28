from datetime import datetime
import requests

import pytest

from event_detector.entities import HTTPRepoTap, LocalState, HTTPFile

state = LocalState('tests/test_data/local_state.json')

class MockedResponse:
    def __init__(self, text):
        self.text = text

@pytest.fixture(autouse=True, scope="function")
def patch_requests_get(monkeypatch):
    def translate_url(url):
        filename = url.replace("http://www.", "").replace(".com", "").replace("/", "_")
        filename = filename.strip("_") + ".html"
        with open(f"tests/test_data/{filename}") as f:
            return MockedResponse(f.read())
    monkeypatch.setattr(requests, "get", translate_url)

def test_get_target_files():
    tap = HTTPRepoTap("http://www.test_url.com", "(.*)/2021.gz", state)
    assert set(tap.get_target_files()) == set([
            HTTPFile("2021.gz", "http://www.test_url.com/2021/2021.gz", datetime(2018, 8, 26, 2, 57, 0)),
        ])

    tap = HTTPRepoTap("http://www.test_url.com", "2021/(.*).gz", state)
    assert set(tap.get_target_files()) == set([
            HTTPFile("2021.gz", "http://www.test_url.com/2021/2021.gz", datetime(2018, 8, 26, 2, 57, 0)),
            HTTPFile("2021_2.gz", "http://www.test_url.com/2021/2021_2.gz", datetime(2018, 8, 26, 2, 58, 0)),
        ])
    
    tap = HTTPRepoTap("http://www.test_url.com", "(.*).gz", state)
    assert set(tap.get_target_files()) == set([
            HTTPFile("2020.gz", "http://www.test_url.com/2020/2020.gz", datetime(2018, 8, 26, 2, 55, 0)),
            HTTPFile("2020_2.gz", "http://www.test_url.com/2020/2020_2.gz", datetime(2018, 8, 26, 2, 56, 0)),
            HTTPFile("2021.gz", "http://www.test_url.com/2021/2021.gz", datetime(2018, 8, 26, 2, 57, 0)),
            HTTPFile("2021_2.gz", "http://www.test_url.com/2021/2021_2.gz", datetime(2018, 8, 26, 2, 58, 0)),
        ])

def test_get_changed_files():
    tap = HTTPRepoTap("http://www.test_url.com", "(.*).gz", state)
    assert set(tap.get_changed_files()) == set([
        HTTPFile("2020_2.gz", "http://www.test_url.com/2020/2020_2.gz", datetime(2018, 8, 26, 2, 56, 0)),
        HTTPFile("2021.gz", "http://www.test_url.com/2021/2021.gz", datetime(2018, 8, 26, 2, 57, 0)),
        HTTPFile("2021_2.gz", "http://www.test_url.com/2021/2021_2.gz", datetime(2018, 8, 26, 2, 58, 0)),
    ])