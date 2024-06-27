import json
import os.path

from interfaces import BaseState

class LocalState(BaseState):
    def __init__(self, state_path="./state/", state_format="json"):
        self.state_path = state_path
        self.state_format = state_format
        super().__init__()
    
    def retrive_state(self):
        if self.state_format == "json":
            return self._retrieve_json_state()
        else:
            raise NotImplemented(f"Retrieval of state in a {self.state_format} is not implemented.")
    
    def _retrieve_json_state(self):
        if not os.path.exists(self.state_path):
            return {}
        else:
            with open(self.state_path) as f:
                return json.load(f)