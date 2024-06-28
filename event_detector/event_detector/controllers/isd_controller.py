from interfaces import BaseState
from entities import HTTPRepoTap, HTTPFile

class ISDController():
    bigquery_tables = {}

    def __init__(self, state: BaseState):
        self.tap = HTTPRepoTap("https://www.ncei.noaa.gov/pub/data/noaa/2024/", "(.*).gz", state=state)
    
    def get_and_dispatch_changed_events(self) -> None:
        changed_files = self.tap.get_changed_files()
        for changed_file in changed_files:
            target_table = ISDController.bigquery_tables.get(changed_file)
            self.trigger_etl_pipeline(target_file=changed_files, target_table=target_table)
    
    def trigger_etl_pipeline(self, target_file: HTTPFile, target_table: str):
        pass
        # print("Trigger ETL")
    
    def write_state(self):
        self.tap.write_state()