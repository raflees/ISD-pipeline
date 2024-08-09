import pandas as pd

from ingest.interfaces.ingest_tap import IngestTap

class TestIngestTap(IngestTap):
    __test__ = False
    def _process_data(self):
        pass
    
    def ingest_data(self):
        pass

def test_read_file_content():
    strategy = TestIngestTap({})
    result = strategy._read_file_content("tests/test_data/sample_csv.csv").to_dict('records')
    assert result == [
        {"id": 1, "col1": "a", "col2": True},
        {"id": 2, "col1": "b", "col2": False},
        {"id": 3, "col1": "c", "col2": True},
    ]