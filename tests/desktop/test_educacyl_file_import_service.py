from pini_desktop.services.educacyl_service import DesktopEducaCyLService


def test_desktop_educacyl_sync_from_file(tmp_path):
    service = DesktopEducaCyLService(cache_dir=tmp_path / "cache")
    path = tmp_path / "template.xlsx"
    service.create_template(path)

    summary = service.sync_from_file(path)

    assert summary.authenticated
    assert summary.teachers == 1
    assert summary.courses == 1
    assert summary.last_sync
