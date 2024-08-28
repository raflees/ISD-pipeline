from datetime import datetime, timezone
import pandas as pd

from ingest.entities import EncapsulateJson, IngestTimestamp


def test_encapsulate_json():
    strategy = EncapsulateJson()
    result = strategy.process_data(pd.read_csv("tests/test_data/sample_csv.csv")).to_dict("records")
    assert result == [
        {"record": "{\"id\": 1, \"col1\": \"a\", \"col2\": true}"},
        {"record": "{\"id\": 2, \"col1\": \"b\", \"col2\": false}"},
        {"record": "{\"id\": 3, \"col1\": \"c\", \"col2\": true}"},
    ]

def test_add_ingest_timestamp(monkeypatch):
    mock_now = datetime(2024, 8, 27, 12, 53, 11, 666666, tzinfo=timezone.utc)
    monkeypatch.setattr(IngestTimestamp, '_get_current_timestamp', lambda self: mock_now)

    strategy = IngestTimestamp()
    result = strategy.process_data(pd.read_csv("tests/test_data/sample_csv.csv")).to_dict("records")
    assert result == [
        {"id": 1, "col1": "a", "col2": True, "ingest_timestamp": "2024-08-27T12:53:11.666666+00:00"},
        {"id": 2, "col1": "b", "col2": False, "ingest_timestamp": "2024-08-27T12:53:11.666666+00:00"},
        {"id": 3, "col1": "c", "col2": True, "ingest_timestamp": "2024-08-27T12:53:11.666666+00:00"},
    ]