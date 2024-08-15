from os.path import join
import pandas as pd

from ingest.entities import CSVFileProcessor

def setup_processor(processing_strategies, tmppath):
    processor = CSVFileProcessor(
        local_target_paths=["tests/test_data/sample_csv.csv"],
        processing_strategies=processing_strategies,
        output_dir=join(tmppath, ".output/")
    )
    return processor

def test_processor_without_strategy(tmpdir):
    processor = setup_processor([], tmpdir)
    processor.process_data()

    expected_data = [
        {"id": 1, "col1": "a", "col2": True},
        {"id": 2, "col1": "b", "col2": False},
        {"id": 3, "col1": "c", "col2": True},
    ]
    assert_processed_data_equals(expected_data, tmpdir)

def test_processor_encapsulate_json_strategy(tmpdir):
    processor = setup_processor(["encapsulate_json"], tmpdir)
    processor.process_data()

    expected_data = [
        {"record": "{\"id\": 1, \"col1\": \"a\", \"col2\": true}"},
        {"record": "{\"id\": 2, \"col1\": \"b\", \"col2\": false}"},
        {"record": "{\"id\": 3, \"col1\": \"c\", \"col2\": true}"},
    ]
    assert_processed_data_equals(expected_data, tmpdir)

def assert_processed_data_equals(expected_data, tmpdir):
    assert pd.read_csv(f"{tmpdir}/.output/sample_csv.csv").to_dict('records') == expected_data

def test_get_file_name_with_csv_extension():
    assert CSVFileProcessor._get_file_name_with_csv_ext("test_file.csv") == "test_file.csv"
    assert CSVFileProcessor._get_file_name_with_csv_ext("test_file") == "test_file.csv"
    assert CSVFileProcessor._get_file_name_with_csv_ext("test_file.json") == "test_file_json.csv"