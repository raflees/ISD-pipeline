import logging
import json
import pandas as pd

from ingest.interfaces import ProcessStrategy

class EncapsulateJson(ProcessStrategy):
    def process_data(self, input_data: pd.DataFrame):
        logging.info("Applying encapsulate_json logic...")
        reduced_series = input_data.apply(
            lambda row_values: json.dumps({k: v for k, v in zip(input_data.columns, list(row_values))}),
            axis=1,
            result_type="reduce")
        df = pd.DataFrame(reduced_series.values, columns=["record"])
        return df
        