from dataclasses import dataclass
from pathlib import Path

from pini_desktop.config.settings import DATA_DIR
from packages.educacyl.auth import EducaCyLCredentials
from packages.educacyl.service import EducaCyLIntegrationService
from packages.educacyl.template import OfficialImportTemplate


@dataclass(frozen=True)
class DesktopEducaCyLSyncSummary:
    authenticated: bool
    source: str
    teachers: int
    courses: int
    subjects: int
    rooms: int
    warnings: tuple[str, ...]
    last_sync: str = ""


class DesktopEducaCyLService:
    def __init__(self, cache_dir=None):
        self.cache_dir = cache_dir or (DATA_DIR / "educacyl_cache")
        self.service = EducaCyLIntegrationService(cache_dir=self.cache_dir)

    def sync_mock(self, username: str = "demo", token: str = "mock") -> DesktopEducaCyLSyncSummary:
        result = self.service.sync(EducaCyLCredentials(username=username, token=token))
        return self._summary(result)

    def sync_from_file(self, path: str | Path) -> DesktopEducaCyLSyncSummary:
        result = self.service.sync_from_file(path)
        return self._summary(result)

    def create_template(self, path: str | Path) -> Path:
        return OfficialImportTemplate().create(path)

    def cache_metadata(self) -> dict:
        return self.service.cache.read_metadata()

    def _summary(self, result) -> DesktopEducaCyLSyncSummary:
        return DesktopEducaCyLSyncSummary(
            authenticated=result.session.authenticated,
            source=result.package.source,
            teachers=result.import_result.teachers,
            courses=result.import_result.courses,
            subjects=result.import_result.subjects,
            rooms=result.import_result.rooms,
            warnings=result.import_result.warnings,
            last_sync=result.cache_metadata.get("last_sync", ""),
        )
