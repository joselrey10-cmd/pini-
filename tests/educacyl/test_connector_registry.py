from packages.educacyl.connectors.registry import ConnectorRegistry
from packages.educacyl.connectors.mock_connector import MockConnector

def test_registry():
    r = ConnectorRegistry()
    r.register(MockConnector())
    assert "mock" in r.names()
    assert r.get("mock").available()
