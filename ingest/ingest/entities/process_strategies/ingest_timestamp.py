from datetime import datetime, timezone
import logging
import pandas as pd

from ingest.interfaces import ProcessStrategy

class IngestTimestamp(ProcessStrategy):
    def process_data(self, input_data: pd.DataFrame):
        logging.info("Applying encapsulate_json logic...")
        ingest_timestamp = self._get_current_timestamp()
        df = input_data
        input_data["ingest_timestamp"] = datetime.isoformat(ingest_timestamp)
        return df

    @staticmethod
    def _get_current_timestamp() -> datetime:
        return datetime.now(timezone.utc)