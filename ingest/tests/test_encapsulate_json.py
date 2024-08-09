import pandas as pd

from ingest.entities.process_strategies import EncapsulateJson

def test_process_file():
    strategy = EncapsulateJson()
    result = strategy.process_data(pd.read_csv("tests/test_data/sample_csv.csv")).to_dict('records')
    assert result == [
        {"record": {"id": 1, "col1": "a", "col2": True}},
        {"record": {"id": 2, "col1": "b", "col2": False}},
        {"record": {"id": 3, "col1": "c", "col2": True}},
    ]