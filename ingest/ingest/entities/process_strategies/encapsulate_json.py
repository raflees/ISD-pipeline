import json
import pandas as pd

class EncapsulateJson:
    @staticmethod
    def process_data(input_data: pd.DataFrame):
        reduced_series = input_data.apply(
            lambda row_values: json.dumps({k: v for k, v in zip(input_data.columns, list(row_values))}),
            axis=1,
            result_type="reduce")
        df = pd.DataFrame(reduced_series.values, columns=["record"])
        return df
        