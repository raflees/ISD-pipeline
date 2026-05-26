from datetime import datetime, timedelta
from os import walk
from os.path import join
from typing import Dict, Iterable

from airflow.sdk import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.sdk.bases.operator import BaseOperator
from irflow.providers.standard.operators.empty import EmptyOperator
import yaml


class DAGFactory:
    SPECS_PATH = "dags/specs"
    DEFAULT_DAG_ARGS = {
        "default_args": {
            "depends_on_past": False,
            "retries": 1,
            "retry_delay": timedelta(minutes=5),
        },
        "start_date": datetime(2021, 1, 1),
        "catchup": False,
    }

    def generate_dags(self) -> Dict[str,  DAG]:
        dags = {}
        for spec in self.get_specs():
            dag = self.parse_spec_into_dag(spec)
            dags[dag.dag_id] = dag
        return dags

    def get_specs(self) -> Iterable[dict]:
        for base_dir, _, files in walk(self.SPECS_PATH):
            for file in filter(lambda f: f.endswith(".yaml"), files):
                yield self.read_spec(join(base_dir, file))
    
    @staticmethod
    def read_spec(filepath: str) -> dict:
        with open(filepath) as f:
            return yaml.safe_load(f)

    def parse_spec_into_dag(self, spec: dict) -> DAG:
        with self._get_dag(spec) as dag:
            triggers_checkpoint = EmptyOperator(task_id="trigger_checkpoint")
            for trigger_task in self._get_tasks(spec, key="triggers"):
                trigger_task >> triggers_checkpoint
            for ingest_task in self._get_tasks(spec, key="ingests"):
                triggers_checkpoint >> ingest_task
        return dag

    def _get_tasks(self, spec: dict, key: str) -> Iterable[BaseOperator]:
        for idx, task_spec in enumerate(spec.get(key) or []):
            image = task_spec["image"]
            tag = task_spec.get("tag") or "latest"
            envs = task_spec.get("envs") or {}
            yield DockerOperator(
                task_id=f"{key}-{idx}",
                image=f"{image}:{tag}",
                environment=envs
            )
    
    def _get_dag(self, spec: dict) -> DAG:
        return DAG(
            spec["name"],
            schedule=spec["schedule"],
            description=spec.get("description") or None,
            **self.DEFAULT_DAG_ARGS,
        )

if __name__ == "__main__":
    DAGFactory().generate_dags()