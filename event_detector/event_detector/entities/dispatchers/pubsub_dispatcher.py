from copy import deepcopy
import json
from typing import Iterable

from google import pubsub_v1

from interfaces import BaseDispatcher

class PubSubDispatcher(BaseDispatcher):
    def __init__(self, project_id: str, topic: str, chuck_size=1000):
        super().__init__()
        self._client = self._get_client()
        self.topic_path = self._client.topic_path(project_id, topic)
        self.event_chunk_size = chuck_size
    
    @staticmethod
    def _get_client() -> pubsub_v1.PublisherClient:
        return pubsub_v1.PublisherClient()
    
    def add_change_event(self, event: dict) -> None:
        self.events.append(self._stringify_data(event))
    
    def dispatch_change_events(self):
        if len(self.events) == 0:
            return

        request = pubsub_v1.PublishRequest()
        request.topic = self.topic_path
        request.messages = []

        event_chunks = self._chunk_event_list(self.event_chunk_size)
        print(f"Sending {len(self.events)} event messages in {len(event_chunks)} event chunks")
        for event_chunk in event_chunks:
            request.messages.append(
                pubsub_v1.PubsubMessage(data=str(event_chunk).encode("utf-8"))
                )
        self._publish_messages(request)
        print("Finished publishing messages")
    
    def _publish_messages(self, request: pubsub_v1.PublishRequest) -> None:
        self._client.publish(request)

    def _chunk_event_list(self, chunk_size: int) -> Iterable[list]:
        chunks = []
        base_list = self.events
        while base_list != []:
            chunks.append(base_list[:chunk_size])
            base_list = base_list[chunk_size:]
        return chunks

    @staticmethod
    def _stringify_data(data: dict) -> str:
        output = {k: str(v) for k, v in data.items()}
        return json.dumps(output)