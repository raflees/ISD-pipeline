from datetime import datetime
import logging
from flask import Request
import functions_framework

import google.cloud.logging
import yaml

from ingest.entities import (
    PubSubParser,
    FileCloudStorageLoader,
    HTTPFileDownloadTap,
)

logging.basicConfig(
    encoding='utf-8',
    format="%(asctime)s\t%(levelname)s - %(message)s",
    level=logging.INFO)

def setup_logging():
    logging_client = google.cloud.logging.Client()
    logging_client.setup_logging()

def load_config() -> dict:
    with open("config.yaml") as f:
        config = yaml.safe_load(f)
    logging.info(f"Loaded config {config}")
    return config

@functions_framework.http
def ingest(request):
    start_time = datetime.now()
    setup_logging()
    config = load_config()
    parser = PubSubParser(config)
    tap = HTTPFileDownloadTap(config, parser.parse_target_info())
    loader = FileCloudStorageLoader(config)
    
    tap.ingest_data()
    loader.load_data(tap.load_stage_dir)
    parser.acknowledge_pulled_messages()

    execution_total_seconds = (datetime.now() - start_time).total_seconds()
    logging.info(f"Finished ingest process ({round(execution_total_seconds, 2)}s)")
    return 'OK'

if __name__ == "__main__":
    request = Request({})
    ingest(request)