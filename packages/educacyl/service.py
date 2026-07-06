from dataclasses import dataclass
from pathlib import Path

from .auth import AuthSession, EducaCyLCredentials
from .cache import EducaCyLCache
from .client import EducaCyLClient, MockEducaCyLClient
from .diff import ImportDiff, ImportPackageDiffer
from .file_parser import OfficialFileParser
from .importer import EducaCyLImporter, ImportResult
from .models import ImportPackage
from .package_store import ImportPackageStore
from .parser import EducaCyLParser


@dataclass(frozen=True)
class SyncResult:
    session: AuthSession
    package: ImportPackage
    import_result: ImportResult
    cache_metadata: dict
    diff: ImportDiff | None = None


class EducaCyLIntegrationService:
    def __init__(self, client: EducaCyLClient | None = None, cache_dir: str | Path = ".pini_educacyl_cache"):
        self.client = client or MockEducaCyLClient()
        self.parser = EducaCyLParser()
        self.file_parser = OfficialFileParser()
        self.importer = EducaCyLImporter()
        self.cache = EducaCyLCache(cache_dir)
        self.package_store = ImportPackageStore(cache_dir)
        self.differ = ImportPackageDiffer()

    def sync(self, credentials: EducaCyLCredentials) -> SyncResult:
        session = self.client.authenticate(credentials)
        package = self.parser.parse(self.client.download_school_data())
        return self._finish_sync(session, package)

    def sync_from_file(self, path: str | Path) -> SyncResult:
        session = AuthSession(authenticated=True, token="", provider="file")
        package = self.file_parser.parse_file(path)
        return self._finish_sync(session, package)

    def preview_diff_from_file(self, path: str | Path) -> ImportDiff:
        old_package = self.package_store.load() or ImportPackage()
        new_package = self.file_parser.parse_file(path)
        return self.differ.diff(old_package, new_package)

    def _finish_sync(self, session: AuthSession, package: ImportPackage) -> SyncResult:
        old_package = self.package_store.load()
        diff = self.differ.diff(old_package, package) if old_package else None
        result = self.importer.import_package(package)
        self.cache.write_metadata(package.source)
        self.package_store.save(package)
        return SyncResult(session, package, result, self.cache.read_metadata(), diff)
