from packages.educacyl.auth import EducaCyLCredentials
from packages.educacyl.history import SyncHistoryStore
from packages.educacyl.service import EducaCyLIntegrationService


def test_sync_history_store_records_sync(tmp_path):
    service = EducaCyLIntegrationService(cache_dir=tmp_path)
    service.sync(EducaCyLCredentials(username="demo", token="x"))

    records = service.list_history()

    assert len(records) == 1
    assert records[0].teachers == 2
    assert records[0].source == "mock-educacyl"


def test_sync_history_can_be_cleared(tmp_path):
    service = EducaCyLIntegrationService(cache_dir=tmp_path)
    service.sync(EducaCyLCredentials(username="demo", token="x"))

    service.clear_history()

    assert service.list_history() == ()
