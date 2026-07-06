class ConnectorRegistry:
    def __init__(self):
        self._connectors = {}

    def register(self, connector):
        self._connectors[connector.name] = connector

    def names(self):
        return sorted(self._connectors)

    def get(self, name):
        return self._connectors[name]
