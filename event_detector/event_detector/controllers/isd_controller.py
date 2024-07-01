from interfaces import BaseDispatcher, BaseState
from entities import HTTPRepoTap, HTTPFile

class ISDController():
    def __init__(self, state: BaseState, dispatcher: BaseDispatcher):
        self.tap = HTTPRepoTap("https://www.ncei.noaa.gov/pub/data/noaa/2024/", "A51256(.*).gz", state=state)
        self.dispatcher = dispatcher
    
    def get_and_dispatch_changed_events(self) -> None:
        changed_files = self.tap.get_changed_files()
        for changed_file in changed_files:
            self.dispatcher.add_change_event(event=changed_file.to_dict())
        self.dispatcher.dispatch_change_events()
    
    def write_state(self):
        self.tap.write_state()