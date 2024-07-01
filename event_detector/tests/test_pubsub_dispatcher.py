from datetime import datetime

from google import pubsub_v1

from event_detector.entities import PubSubDispatcher

class MockTopic():
    messages = []

def mock_publish(self, request):
    for message in request.messages:
        MockTopic.messages.append(message.data.decode("utf-8"))

def test_chunk_event_list():
    dispatcher = PubSubDispatcher("test_project", "test_topic")
    dispatcher.events = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    assert dispatcher._chunk_event_list(5) == [
        [1, 2, 3, 4, 5],
        [6, 7, 8, 9, 10]
    ]
    
    assert dispatcher._chunk_event_list(3) == [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
        [10]
    ]

def test_dispatch_method(monkeypatch):
    monkeypatch.setattr(PubSubDispatcher, '_publish_messages', mock_publish)

    dispatcher = PubSubDispatcher("test_project", "test_topic")

    event1 = {"file": "test_file_1", "url": "test_url/test_file_1", "modified": datetime(2024, 5, 31, 20, 54, 0)}
    event2 = {"file": "test_file_2", "url": "test_url/test_file_2", "modified": datetime(2024, 5, 31, 21, 54, 0)}
    dispatcher.add_change_event(event1)
    dispatcher.add_change_event(event2)
    assert MockTopic.messages == []

    MockTopic.messages = []
    dispatcher.dispatch_change_events()
    assert MockTopic.messages == [
        '[\'{"file": "test_file_1", "url": "test_url/test_file_1", "modified": "2024-05-31 20:54:00"}\', ' +
        '\'{"file": "test_file_2", "url": "test_url/test_file_2", "modified": "2024-05-31 21:54:00"}\']'
    ]

    MockTopic.messages = []
    dispatcher.event_chunk_size = 1
    dispatcher.dispatch_change_events()
    print(MockTopic.messages)
    assert MockTopic.messages == [
        '[\'{"file": "test_file_1", "url": "test_url/test_file_1", "modified": "2024-05-31 20:54:00"}\']',
        '[\'{"file": "test_file_2", "url": "test_url/test_file_2", "modified": "2024-05-31 21:54:00"}\']'
    ]
