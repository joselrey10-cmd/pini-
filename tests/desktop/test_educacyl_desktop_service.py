from pini_desktop.services.educacyl_service import DesktopEducaCyLService


def test_desktop_educacyl_mock_sync(tmp_path):
    service = DesktopEducaCyLService(cache_dir=tmp_path)
    summary = service.sync_mock()

    assert summary.authenticated
    assert summary.teachers == 2
    assert summary.courses == 1
    assert summary.last_sync
