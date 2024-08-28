from dataclasses import dataclass
import pytest
from unittest.mock import Mock

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
    def __init__(self, ack_id: str, data: str):
        self.ack_id = ack_id
        self.message = MockPubSubMessageContent(data.encode())

def test_pull_messages(patch_get_client, patch_pull_messages):
    parser = PubSubParser({"pubsub": {"subscription": "test"}})
    assert list(parser.parse_target_info()) == [
        {"file_name": "file1.gz", "file_url": "https://test.com/file1.gz"},
        {"file_name": "file2.gz", "file_url": "https://test.com/file2.gz"},
        {"file_name": "file3.gz", "file_url": "https://test.com/file3.gz"},
    ]
    assert parser._pulled_messages_ack_ids == ["1", "2" , "3"]

def test_parse_target_info_duplicated_messages(patch_get_client, patch_pull_duplicated_messages):
    parser = PubSubParser({"pubsub": {"subscription": "test"}})
    assert list(parser.parse_target_info()) == [
        {"file_name": "file1.gz", "file_url": "https://test.com/file1.gz"},
        {"file_name": "file2.gz", "file_url": "https://test.com/file2.gz"},
    ]

def test_no_messages_to_acknowledge():
    parser = PubSubParser({"pubsub": {"subscription": "test"}})
    parser._pulled_messages_ack_ids = []
    parser.acknowledge_pulled_messages()

@pytest.fixture
def patch_get_client(monkeypatch):
    monkeypatch.setattr(PubSubParser, "_get_client", MockPubSubClient)

@pytest.fixture
def patch_pull_messages(monkeypatch):
    mocked_message_1 = MockPubSubMessage(
        ack_id="1",
        data='[\'{"file_name": "file1.gz", "url": "https://test.com/file1.gz", "last_modified": "2024-08-03 13:04:00"}\', ' +
        '{"file_name": "file2.gz", "url": "https://test.com/file2.gz", "last_modified": "2024-08-03 13:04:00"}\']'
    )
    mocked_message_2 = MockPubSubMessage(
        ack_id="2",
        data='[\'{"file_name": "file3.gz", "url": "https://test.com/file3.gz", "last_modified": "2024-08-03 13:04:00"}\']'
    )
    empty_mocked_message = MockPubSubMessage(ack_id="3", data='[]')
    
    monkeypatch.setattr(
        PubSubParser,
        "_pull_messages",
        lambda self: [mocked_message_1, mocked_message_2, empty_mocked_message]
    )

@pytest.fixture
def patch_pull_duplicated_messages(monkeypatch):
    mocked_message = MockPubSubMessage(
        ack_id="4",
        data='[\'{"file_name": "file1.gz", "url": "https://test.com/file1.gz", "last_modified": "2024-08-03 13:04:00"}, ' +
        '{"file_name": "file1.gz", "url": "https://test.com/file1.gz", "last_modified": "2024-08-03 13:06:00"}, ' +
        '{"file_name": "file2.gz", "url": "https://test.com/file2.gz", "last_modified": "2024-08-03 13:04:00"}\']'
    )
    
    monkeypatch.setattr(
        PubSubParser,
        "_pull_messages",
        lambda self: [mocked_message]
    )