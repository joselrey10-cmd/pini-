from packages.educacyl.auth import EducaCyLCredentials
from packages.educacyl.cache import EducaCyLCache
from packages.educacyl.models import ImportPackage, TeacherImport
from packages.educacyl.service import EducaCyLIntegrationService


def test_models():
    package = ImportPackage(teachers=(TeacherImport("P01", "Ana", "García"),), source="test")
    assert package.teachers[0].code == "P01"
    assert package.source == "test"


def test_cache(tmp_path):
    cache = EducaCyLCache(tmp_path)
    assert not cache.has_sync()
    cache.write_metadata("mock")
    assert cache.has_sync()
    assert cache.read_metadata()["source"] == "mock"


def test_mock_sync_flow(tmp_path):
    service = EducaCyLIntegrationService(cache_dir=tmp_path)
    result = service.sync(EducaCyLCredentials(username="demo", token="x"))
    assert result.session.authenticated
    assert result.import_result.teachers == 2
    assert result.import_result.courses == 1
    assert result.cache_metadata["source"] == "mock-educacyl"
