from abc import ABC, abstractmethod

class ProcessStrategy(ABC):
    @abstractmethod
    def process_file(input_path: str, output_path: str) -> None:
        pass