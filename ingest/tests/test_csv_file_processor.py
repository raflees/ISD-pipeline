from datetime import datetime, timezone
from os.path import join
import pandas as pd

from ingest.entities import CSVFileProcessor, IngestTimestamp

def setup_processor(processing_strategies, files, tmpdir, header=None):
    processor = CSVFileProcessor(
        local_target_paths=files,
        processing_strategies=processing_strategies,
        output_dir=join(tmpdir, ".output/"),
        override_header=header
    )
    return processor

def test_processor_without_strategy(tmpdir):
    processor = setup_processor([], ["tests/test_data/sample_csv.csv"], tmpdir)
    processor.process_data()

    expected_data = [
        {"id": 1, "col1": "a", "col2": True},
        {"id": 2, "col1": "b", "col2": False},
        {"id": 3, "col1": "c", "col2": True},
    ]
    assert_processed_data_equals("sample_csv.csv", expected_data, tmpdir)

def test_processor_encapsulate_json_strategy_with_header(tmpdir):
    processor = setup_processor(["encapsulate_json"], ["tests/test_data/sample_csv.csv"], tmpdir)
    processor.process_data()

    expected_data = [
        {"record": "{\"id\": 1, \"col1\": \"a\", \"col2\": true}"},
        {"record": "{\"id\": 2, \"col1\": \"b\", \"col2\": false}"},
        {"record": "{\"id\": 3, \"col1\": \"c\", \"col2\": true}"},
    ]
    assert_processed_data_equals("sample_csv.csv", expected_data, tmpdir)

def test_processor_encapsulate_json_strategy_without_header(tmpdir):
    processor = setup_processor(["encapsulate_json"], ["tests/test_data/csv_no_header.csv"], tmpdir, header=["data"])
    processor.process_data()

    expected_data = [
        {"record": "{\"data\": \"0136A51256004512024010106156+36699-093402FM-15+0411KFWB V0209999C00005007325MN0160935N5+00005-00405999999ADDGA1085+007325999GD14991+0073259MA1102545097655REMMET07801/01/24 00:15:02 METAR KFWB 010615Z 00000KT 10SM OVC024 M00/M04 A3028 RMK AO2\"}"},
        {"record": "{\"data\": \"0136A51256004512024010106356+36699-093402FM-15+0411KFWB V0209999C00005007325MN0160935N5+00005-00405999999ADDGA1085+007325999GD14991+0073259MA1102545097655REMMET07801/01/24 00:35:02 METAR KFWB 010635Z 00000KT 10SM OVC024 M00/M04 A3028 RMK AO2\"}"},
        {"record": "{\"data\": \"0171A51256004512024010106556+36699-093402FM-15+0411KFWB V0200205N00315007015MN0160935N5+0000C-0040C999999ADDGA1085+007015999GD14991+0070159MA1102545097655REMMET07801/01/24 00:55:02 METAR KFWB 010655Z 02006KT 10SM OVC023 M00/M04 A3028 RMK AO2EQDR01   M007TMP046R02   M047DPT046\"}"},
    ]
    assert_processed_data_equals("csv_no_header.csv", expected_data, tmpdir)

def test_processor_encapsulate_json_and_ingest_timestamp(monkeypatch, tmpdir):
    mock_now = datetime(2024, 8, 27, 12, 53, 11, 666666, tzinfo=timezone.utc)
    monkeypatch.setattr(IngestTimestamp, '_get_current_timestamp', lambda self: mock_now)
    expected_timestamp = "2024-08-27T12:53:11.666666+00:00"

    processor = setup_processor(["encapsulate_json", "ingest_timestamp"], ["tests/test_data/csv_no_header.csv"], tmpdir, header=["data"])
    processor.process_data()

    expected_data = [
        {"record": "{\"data\": \"0136A51256004512024010106156+36699-093402FM-15+0411KFWB V0209999C00005007325MN0160935N5+00005-00405999999ADDGA1085+007325999GD14991+0073259MA1102545097655REMMET07801/01/24 00:15:02 METAR KFWB 010615Z 00000KT 10SM OVC024 M00/M04 A3028 RMK AO2\"}", "ingest_timestamp": expected_timestamp},
        {"record": "{\"data\": \"0136A51256004512024010106356+36699-093402FM-15+0411KFWB V0209999C00005007325MN0160935N5+00005-00405999999ADDGA1085+007325999GD14991+0073259MA1102545097655REMMET07801/01/24 00:35:02 METAR KFWB 010635Z 00000KT 10SM OVC024 M00/M04 A3028 RMK AO2\"}", "ingest_timestamp": expected_timestamp},
        {"record": "{\"data\": \"0171A51256004512024010106556+36699-093402FM-15+0411KFWB V0200205N00315007015MN0160935N5+0000C-0040C999999ADDGA1085+007015999GD14991+0070159MA1102545097655REMMET07801/01/24 00:55:02 METAR KFWB 010655Z 02006KT 10SM OVC023 M00/M04 A3028 RMK AO2EQDR01   M007TMP046R02   M047DPT046\"}", "ingest_timestamp": expected_timestamp},
    ]
    assert_processed_data_equals("csv_no_header.csv", expected_data, tmpdir)

def assert_processed_data_equals(file_name, expected_data, tmpdir):
    assert pd.read_csv(f"{tmpdir}/.output/{file_name}").to_dict('records') == expected_data

def test_get_file_name_with_csv_extension():
    assert CSVFileProcessor._get_file_name_with_csv_ext("test_file.csv") == "test_file.csv"
    assert CSVFileProcessor._get_file_name_with_csv_ext("test_file") == "test_file.csv"
    assert CSVFileProcessor._get_file_name_with_csv_ext("test_file.json") == "test_file_json.csv"