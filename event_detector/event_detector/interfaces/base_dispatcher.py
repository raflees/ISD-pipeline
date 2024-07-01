from abc import ABC, abstractmethod

class BaseDispatcher(ABC):
    def __init__(self):
        self.events = []
    
    def add_change_event(self, event: dict) -> None:
        self.events.append(event)

    def dispatch_change_events(self) -> None:
        pass