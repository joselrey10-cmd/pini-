from packages.educacyl.client import MockEducaCyLClient
from .base import OfficialConnector

class MockConnector(OfficialConnector):
    name = "mock"

    def __init__(self):
        self.client = MockEducaCyLClient()

    def available(self):
        return True

    def import_package(self):
        return self.client.download_school_data()
