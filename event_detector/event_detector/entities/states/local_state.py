from datetime import datetime
import json
import os.path

from interfaces import BaseState

class LocalState(BaseState):
    def __init__(self, state_path="./state/", state_format="json"):
        self.state_path = state_path
        self.state_format = state_format
        self.datetime_format = "%Y-%m-%dT%H:%M:%S"
        super().__init__()
    
    def get_last_modified_datetime(self, key: str) -> datetime:
        raw_last_modified = self.state.get(key, {}).get("last_modified", None)
        if raw_last_modified is not None:
            return datetime.strptime(raw_last_modified, self.datetime_format)
        return None

    def set_last_modified_datetime(self, key: str, dt: datetime):
        if self.state.get(key, None) is None:
            self.state[key] = {}
        self.state[key]["last_modified"] = dt.strftime(self.datetime_format)
    
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