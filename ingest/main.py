import logging
from flask import Request
import functions_framework
import yaml

from ingest.entities import (
    PubSubParser,
    FileBigQueryLoader,
    HTTPFileDownloadTap,
)

logging.basicConfig(encoding='utf-8', level=logging.INFO)

def load_config() -> dict:
    with open("config.yaml") as f:
        config = yaml.safe_load(f)
    logging.info(f"Loaded config {config}")
    return config

@functions_framework.http
def ingest(request):
    config = load_config()
    parser = PubSubParser(config)
    tap = HTTPFileDownloadTap(config, parser.parse_target_info())
    loader = FileBigQueryLoader(config)
    
    # tap.ingest_data()
    loader.load_data(tap.load_stage_dir)

    return 'OK'

if __name__ == "__main__":
    request = Request({})
    ingest(request)