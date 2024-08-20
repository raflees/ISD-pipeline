import logging
import json
from typing import Any, Dict, Iterable

from google import pubsub_v1

from ingest.interfaces import TargetInfoParser

class PubSubParser(TargetInfoParser):
    def __init__(self, config: dict):
        super().__init__(config)
        self._subscription: str = config["pubsub"]["subscription"]
        self._client = self._get_client()

    @staticmethod
    def _get_client() -> pubsub_v1.SubscriberClient:
        return pubsub_v1.SubscriberClient()

    def _pull_messages(self) -> Iterable[Dict[str, Any]]:
        request = pubsub_v1.PullRequest(
            subscription=self._subscription,
            max_messages=100
        )
        response: pubsub_v1.PullResponse = self._client.pull(request)
        return response.received_messages

    def _parse_received_message_into_file_data(self, pubsub_message):
        unnested_raw_data = pubsub_message.message.data
        try:
            files_data = unnested_raw_data.decode().replace("\'", "")
            for file_data in json.loads(files_data):
                yield file_data
        except json.JSONDecodeError:
            raise ValueError(f"Unable to parse message to json: {unnested_raw_data}")

    def parse_target_info(self) -> Iterable[dict]:
        target_information = {}
        logging.info(f"Pulling messages from {self._subscription}")
        for raw_message in self._pull_messages():
            files_data = self._parse_received_message_into_file_data(raw_message)
            for file_data in files_data:
                key = (file_data["file_name"], file_data["url"])
                target_information[key] = {"file_name": file_data["file_name"], "file_url": file_data["url"]}
        return target_information.values()