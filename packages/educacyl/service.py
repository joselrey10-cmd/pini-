from dataclasses import dataclass
from pathlib import Path

from .auth import AuthSession, EducaCyLCredentials
from .cache import EducaCyLCache
from .client import EducaCyLClient, MockEducaCyLClient
from .conflict_resolver import ConflictResolutionPlan, ConflictResolutionPolicy, ImportConflictResolver
from .diff import ImportDiff, ImportPackageDiffer
from .file_parser import OfficialFileParser
from .history import SyncHistoryStore
from .importer import EducaCyLImporter, ImportResult
from .models import ImportPackage
from .offline import OfflineImportProvider, OfflineStatus
from .package_store import ImportPackageStore
from .parser import EducaCyLParser
from .validator import ImportPackageValidator, ImportValidationReport


@dataclass(frozen=True)
class SyncResult:
    session: AuthSession
    package: ImportPackage
    import_result: ImportResult
    cache_metadata: dict
    diff: ImportDiff | None = None
    validation_report: ImportValidationReport | None = None
    resolution_plan: ConflictResolutionPlan | None = None


class EducaCyLIntegrationService:
    def __init__(self, client: EducaCyLClient | None = None, cache_dir: str | Path = ".pini_educacyl_cache"):
        self.client = client or MockEducaCyLClient()
        self.parser = EducaCyLParser()
        self.file_parser = OfficialFileParser()
        self.importer = EducaCyLImporter()
        self.cache = EducaCyLCache(cache_dir)
        self.package_store = ImportPackageStore(cache_dir)
        self.offline = OfflineImportProvider(cache_dir)
        self.history = SyncHistoryStore(cache_dir)
        self.differ = ImportPackageDiffer()
        self.validator = ImportPackageValidator()
        self.resolver = ImportConflictResolver()

    def sync(self, credentials: EducaCyLCredentials) -> SyncResult:
        session = self.client.authenticate(credentials)
        package = self.parser.parse(self.client.download_school_data())
        return self._finish_sync(session, package, register_history=True)

    def sync_from_file(self, path: str | Path) -> SyncResult:
        session = AuthSession(authenticated=True, token="", provider="file")
        package = self.file_parser.parse_file(path)
        return self._finish_sync(session, package, register_history=True)

    def use_offline_cache(self) -> SyncResult:
        package = self.offline.load_cached_package()
        session = AuthSession(authenticated=True, provider="offline-cache")
        result = self.importer.import_package(package)
        sync_result = SyncResult(
            session=session,
            package=package,
            import_result=result,
            cache_metadata=self.cache.read_metadata(),
            diff=None,
            validation_report=self.validator.validate(package),
            resolution_plan=None,
        )
        self.history.add(self.history.build_record(sync_result))
        return sync_result

    def list_history(self):
        return self.history.list_records()

    def clear_history(self) -> None:
        self.history.clear()

    def offline_status(self) -> OfflineStatus:
        return self.offline.status()

    def clear_cache(self) -> None:
        self.cache.clear()

    def preview_diff_from_file(self, path: str | Path) -> ImportDiff:
        old_package = self.package_store.load() or ImportPackage()
        new_package = self.file_parser.parse_file(path)
        return self.differ.diff(old_package, new_package)

    def validate_file(self, path: str | Path) -> ImportValidationReport:
        package = self.file_parser.parse_file(path)
        return self.validator.validate(package)

    def preview_resolution_from_file(self, path: str | Path, policy: ConflictResolutionPolicy | None = None) -> ConflictResolutionPlan:
        diff = self.preview_diff_from_file(path)
        return self.resolver.build_plan(diff, policy)

    def _finish_sync(self, session: AuthSession, package: ImportPackage, register_history: bool = True) -> SyncResult:
        old_package = self.package_store.load()
        diff = self.differ.diff(old_package, package) if old_package else None
        validation_report = self.validator.validate(package)
        resolution_plan = self.resolver.build_plan(diff) if diff else None
        result = self.importer.import_package(package)
        self.cache.write_metadata(package.source)
        self.package_store.save(package)

        sync_result = SyncResult(session, package, result, self.cache.read_metadata(), diff, validation_report, resolution_plan)

        if register_history:
            self.history.add(self.history.build_record(sync_result))

        return sync_result
