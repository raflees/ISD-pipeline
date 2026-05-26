from dags.dag_factory import DAGFactory


def test_generate_dags(monkeypatch):
    monkeypatch.setattr(DAGFactory, 'SPECS_PATH', 'dags/specs')
    factory = DAGFactory()
    assert len(factory.generate_dags()) > 0