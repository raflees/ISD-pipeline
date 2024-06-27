from interfaces import BaseState
from entities import FTPTap

class ISDController():
    bigquery_tables = {}

    def __init__(self, state: BaseState):
        self.tap = FTPTap("ftp.ncdc.noaa.gov", state=state)
    
    def get_and_dispatch_changed_events(self) -> None:
        changed_files = self.tap.get_changed_files()
        for changed_file in changed_files:
            target_table = ISDController.bigquery_tables[changed_file]
            self.trigger_etl_pipeline(target_file=changed_files, target_table=target_table)