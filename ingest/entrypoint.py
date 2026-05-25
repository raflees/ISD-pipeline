from datetime import datetime
import json
import logging

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
    project_id = os.environ["PROJECT_ID"]
    table_name = os.environ["BQ_TABLE_NAME"]
    config = {
        "project_id": project_id
        "bigquery":
            "dataset": table_name.split(".")[0]
            "table": table_name.split(".")[1]
        "storage":
            "bucket": os.environ["GCS_BUCKET_NAME"]
        "pubsub":
            "subscription": f"projects/{project_id}/subscriptions/{os.environ['PUBSUB_SUBSCRIPTION_NAME']}"
        "processing_strategies": json.loads(os.environ.get("PROCESSING_STRATEGIES") or [])
        "table":
            "headers": json.loads(os.environ["TABLE_HEADERS"])
    }
    return config

def ingest():
    start_time = datetime.now()
    setup_logging()
    config = load_config()
    parser = PubSubParser(config)
    
    target_info = parser.parse_target_info()
    if len(target_info) == 0:
        logging.info("Found no files to download, finishing execution")
        exit(0)

    tap = HTTPFileDownloadTap(config, target_info)
    loader = FileCloudStorageLoader(config)
    
    tap.ingest_data()
    loader.load_data(tap.load_stage_dir)
    parser.acknowledge_pulled_messages()

    execution_total_seconds = (datetime.now() - start_time).total_seconds()
    logging.info(f"Finished ingest process ({round(execution_total_seconds, 2)}s)")
    return 'OK'

if __name__ == "__main__":
    ingest()