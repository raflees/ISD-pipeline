import requests

import pytest

from event_detector.entities import HTTPRepoTap, LocalState

state = LocalState("test_data/local_state.json")

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
    assert tap.get_target_files() == ["http://www.test_url.com/2021/2021.gz"]

    tap = HTTPRepoTap("http://www.test_url.com", "2021/(.*).gz", state)
    assert set(tap.get_target_files()) == set([
            "http://www.test_url.com/2021/2021.gz",
            "http://www.test_url.com/2021/do_not_use.gz",
        ])
    
    tap = HTTPRepoTap("http://www.test_url.com", "(.*).gz", state)
    assert set(tap.get_target_files()) == set([
            "http://www.test_url.com/2020/2020.gz",
            "http://www.test_url.com/2020/do_not_use.gz",
            "http://www.test_url.com/2021/2021.gz",
            "http://www.test_url.com/2021/do_not_use.gz",
        ])