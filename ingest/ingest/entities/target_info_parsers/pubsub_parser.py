import json
from typing import Iterable

from google import pubsub_v1

from ingest.interfaces import TargetInfoParser

class PuSubParser(TargetInfoParser):
    def __init__(self, config: dict):
        super().__init__(config)
        self.subscription: str = config["pubsub"]["subscription"]
        self.client = self._get_client()

    @staticmethod
    def _get_client() -> pubsub_v1.SubscriberClient:
        return pubsub_v1.SubscriberClient()

    def _pull_messages(self) -> Iterable[pubsub_v1.ReceivedMessage]:
        request = pubsub_v1.PullRequest(
            subscription=self.subscription,
            max_messages=100
        )
        response: pubsub_v1.PullResponse = self.client.pull(request)

        return response.received_messages

    ## TEST ME
    def parse_target_info(self) -> Iterable[dict]:
        for message in self._pull_messages():
            data: list = eval(message.data)
            for file_info in data:
                yield {"file_name": file_info["file_name"], "file_url": file_info["url"]}