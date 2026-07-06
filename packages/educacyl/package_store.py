import json
from pathlib import Path
from dataclasses import asdict

from .models import (
    CourseImport,
    ImportPackage,
    RoomImport,
    SchoolConfigurationImport,
    SubjectImport,
    TeacherImport,
)


class ImportPackageStore:
    def __init__(self, cache_dir: str | Path):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.package_path = self.cache_dir / "last_package.json"

    def save(self, package: ImportPackage) -> None:
        self.package_path.write_text(
            json.dumps(self._to_dict(package), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def load(self) -> ImportPackage | None:
        if not self.package_path.exists():
            return None
        data = json.loads(self.package_path.read_text(encoding="utf-8"))
        return self._from_dict(data)

    def _to_dict(self, package: ImportPackage) -> dict:
        return {
            "teachers": [asdict(item) for item in package.teachers],
            "courses": [asdict(item) for item in package.courses],
            "subjects": [asdict(item) for item in package.subjects],
            "rooms": [asdict(item) for item in package.rooms],
            "configuration": asdict(package.configuration) if package.configuration else None,
            "source": package.source,
            "metadata": package.metadata,
        }

    def _from_dict(self, data: dict) -> ImportPackage:
        configuration = data.get("configuration")
        return ImportPackage(
            teachers=tuple(TeacherImport(**item) for item in data.get("teachers", [])),
            courses=tuple(CourseImport(**item) for item in data.get("courses", [])),
            subjects=tuple(SubjectImport(**item) for item in data.get("subjects", [])),
            rooms=tuple(RoomImport(**item) for item in data.get("rooms", [])),
            configuration=SchoolConfigurationImport(**configuration) if configuration else None,
            source=data.get("source", "cache"),
            metadata=data.get("metadata", {}),
        )
