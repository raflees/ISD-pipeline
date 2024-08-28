from abc import ABC, abstractmethod

import pandas as pd

class ProcessStrategy(ABC):
    @abstractmethod
    def process_data(self, df: pd.DataFrame) -> pd.DataFrame:
        pass
