from packages.educacyl.models import ImportPackage, TeacherImport
from packages.educacyl.offline import OfflineImportProvider
from packages.educacyl.package_store import ImportPackageStore
from packages.educacyl.service import EducaCyLIntegrationService


def test_offline_status_without_cache(tmp_path):
    status = OfflineImportProvider(tmp_path).status()
    assert not status.available


def test_offline_provider_loads_cached_package(tmp_path):
    store = ImportPackageStore(tmp_path)
    store.save(ImportPackage(teachers=(TeacherImport("P01", "Ana", "García"),), source="test"))

    provider = OfflineImportProvider(tmp_path)
    status = provider.status()
    package = provider.load_cached_package()

    assert status.available
    assert status.teachers == 1
    assert package.source == "test"


def test_service_uses_offline_cache(tmp_path):
    service = EducaCyLIntegrationService(cache_dir=tmp_path)
    service.package_store.save(ImportPackage(teachers=(TeacherImport("P01", "Ana", "García"),), source="cache"))

    result = service.use_offline_cache()

    assert result.session.provider == "offline-cache"
    assert result.import_result.teachers == 1
