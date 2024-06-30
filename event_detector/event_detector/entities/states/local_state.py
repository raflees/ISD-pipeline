from datetime import datetime
import json
import os
import os.path

from interfaces import BaseState

class LocalState(BaseState):
    def __init__(self, state_path="event_detector/.state/state.json"):
        super().__init__()
        self.state_path = state_path
        self.state = self._retrieve_state()
        
    def _retrieve_state(self):
        if self.state_format == "json":
            return self._retrieve_json_state()
        else:
            raise NotImplemented(f"Retrieval of state in a {self.state_format} is not implemented.")
    
    def _retrieve_json_state(self) -> dict:
        if not os.path.exists(self.state_path):
            return {}
        else:
            with open(self.state_path) as f:
                return json.load(f)
    
    def _create_state_folder(self):
        print("Making directory", self.state_path)
        folder = os.path.dirname(self.state_path)
        os.makedirs(folder, exist_ok=True)

    def write_state(self):
        self._create_state_folder()
        with open(self.state_path, 'w') as f:
            json.dump(self.state, f)