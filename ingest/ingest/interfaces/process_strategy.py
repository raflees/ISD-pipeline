from abc import ABC, abstractmethod

import pandas as pd

class ProcessStrategy(ABC):
    @staticmethod
    @abstractmethod
    def process_data(self, df: pd.DataFrame) -> None:
        pass
