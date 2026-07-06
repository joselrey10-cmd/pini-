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
    created: int = 0
    updated: int = 0
    deleted: int = 0


@dataclass(frozen=True)
class DesktopOfflineStatus:
    available: bool
    source: str = ""
    teachers: int = 0
    courses: int = 0
    subjects: int = 0
    rooms: int = 0


@dataclass(frozen=True)
class DesktopSyncHistoryRecord:
    id: str
    source: str
    provider: str
    created_at: str
    teachers: int
    courses: int
    subjects: int
    rooms: int
    created: int
    updated: int
    deleted: int
    warnings: tuple[str, ...]


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

    def use_offline_cache(self) -> DesktopEducaCyLSyncSummary:
        result = self.service.use_offline_cache()
        return self._summary(result)

    def list_history(self) -> list[DesktopSyncHistoryRecord]:
        return [
            DesktopSyncHistoryRecord(
                id=item.id,
                source=item.source,
                provider=item.provider,
                created_at=item.created_at,
                teachers=item.teachers,
                courses=item.courses,
                subjects=item.subjects,
                rooms=item.rooms,
                created=item.created,
                updated=item.updated,
                deleted=item.deleted,
                warnings=item.warnings,
            )
            for item in self.service.list_history()
        ]

    def clear_history(self) -> None:
        self.service.clear_history()

    def offline_status(self) -> DesktopOfflineStatus:
        status = self.service.offline_status()
        return DesktopOfflineStatus(status.available, status.source, status.teachers, status.courses, status.subjects, status.rooms)

    def clear_cache(self) -> None:
        self.service.clear_cache()

    def preview_diff_from_file(self, path: str | Path):
        return self.service.preview_diff_from_file(path)

    def create_template(self, path: str | Path) -> Path:
        return OfficialImportTemplate().create(path)

    def cache_metadata(self) -> dict:
        return self.service.cache.read_metadata()

    def _summary(self, result) -> DesktopEducaCyLSyncSummary:
        diff = result.diff
        return DesktopEducaCyLSyncSummary(
            authenticated=result.session.authenticated,
            source=result.package.source,
            teachers=result.import_result.teachers,
            courses=result.import_result.courses,
            subjects=result.import_result.subjects,
            rooms=result.import_result.rooms,
            warnings=result.import_result.warnings,
            last_sync=result.cache_metadata.get("last_sync", ""),
            created=len(diff.created) if diff else 0,
            updated=len(diff.updated) if diff else 0,
            deleted=len(diff.deleted) if diff else 0,
        )
