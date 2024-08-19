from dataclasses import dataclass
import pytest

from ingest.entities import PubSubParser

@dataclass
class MockPubSubClient:
    pass

@dataclass
class MockPubSubMessageContent:
    data: bytes

@dataclass
class MockPubSubMessage:
    message: MockPubSubMessageContent
    def __init__(self, data: str):
        self.message = MockPubSubMessageContent(data.encode())

def test_pull_messages(patch_get_client, patch_pull_messages):
    parser = PubSubParser({"pubsub": {"subscription": "test"}})
    assert list(parser.parse_target_info()) == [
        {"file_name": "file1.gz", "file_url": "https://test.com/file1.gz"},
        {"file_name": "file2.gz", "file_url": "https://test.com/file2.gz"},
        {"file_name": "file3.gz", "file_url": "https://test.com/file3.gz"},
    ]

@pytest.fixture
def patch_get_client(monkeypatch):
    monkeypatch.setattr(PubSubParser, "_get_client", MockPubSubClient)

@pytest.fixture
def patch_pull_messages(monkeypatch):
    mocked_message_1 = MockPubSubMessage(
        data='[\'{"file_name": "file1.gz", "url": "https://test.com/file1.gz", "last_modified": "2024-08-03 13:04:00"}\', ' +
        '{"file_name": "file2.gz", "url": "https://test.com/file2.gz", "last_modified": "2024-08-03 13:04:00"}\']'
    )
    mocked_message_2 = MockPubSubMessage(
        data='[\'{"file_name": "file3.gz", "url": "https://test.com/file3.gz", "last_modified": "2024-08-03 13:04:00"}\']'
    )
    empty_mocked_message = MockPubSubMessage(data='[]')
    
    monkeypatch.setattr(
        PubSubParser,
        "_pull_messages",
        lambda self: [mocked_message_1, mocked_message_2, empty_mocked_message]
    )