from dataclasses import dataclass
from pathlib import Path

from .auth import AuthSession, EducaCyLCredentials
from .cache import EducaCyLCache
from .client import EducaCyLClient, MockEducaCyLClient
from .importer import EducaCyLImporter, ImportResult
from .models import ImportPackage
from .parser import EducaCyLParser


@dataclass(frozen=True)
class SyncResult:
    session: AuthSession
    package: ImportPackage
    import_result: ImportResult
    cache_metadata: dict


class EducaCyLIntegrationService:
    def __init__(self, client: EducaCyLClient | None = None, cache_dir: str | Path = ".pini_educacyl_cache"):
        self.client = client or MockEducaCyLClient()
        self.parser = EducaCyLParser()
        self.importer = EducaCyLImporter()
        self.cache = EducaCyLCache(cache_dir)

    def sync(self, credentials: EducaCyLCredentials) -> SyncResult:
        session = self.client.authenticate(credentials)
        package = self.parser.parse(self.client.download_school_data())
        result = self.importer.import_package(package)
        self.cache.write_metadata(package.source)
        return SyncResult(session, package, result, self.cache.read_metadata())
