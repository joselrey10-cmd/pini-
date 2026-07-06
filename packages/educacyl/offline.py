from dataclasses import dataclass

from .models import ImportPackage
from .package_store import ImportPackageStore


@dataclass(frozen=True)
class OfflineStatus:
    available: bool
    source: str = ""
    teachers: int = 0
    courses: int = 0
    subjects: int = 0
    rooms: int = 0


class OfflineImportProvider:
    """Permite trabajar con la última importación guardada en caché."""

    def __init__(self, cache_dir):
        self.store = ImportPackageStore(cache_dir)

    def status(self) -> OfflineStatus:
        package = self.store.load()
        if package is None:
            return OfflineStatus(available=False)

        return OfflineStatus(
            available=True,
            source=package.source,
            teachers=len(package.teachers),
            courses=len(package.courses),
            subjects=len(package.subjects),
            rooms=len(package.rooms),
        )

    def load_cached_package(self) -> ImportPackage:
        package = self.store.load()
        if package is None:
            raise FileNotFoundError("No hay paquete EducaCyL en caché.")
        return package
