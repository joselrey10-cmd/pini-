from packages.educacyl.models import ImportPackage, TeacherImport
from packages.educacyl.package_store import ImportPackageStore
from pini_desktop.services.educacyl_service import DesktopEducaCyLService


def test_desktop_offline_status(tmp_path):
    service = DesktopEducaCyLService(cache_dir=tmp_path)
    assert not service.offline_status().available

    ImportPackageStore(tmp_path).save(
        ImportPackage(teachers=(TeacherImport("P01", "Ana", "García"),), source="cache")
    )

    status = service.offline_status()
    assert status.available
    assert status.teachers == 1
