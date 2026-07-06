import json
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path


@dataclass(frozen=True)
class SyncHistoryRecord:
    id: str
    source: str
    provider: str
    created_at: str
    teachers: int = 0
    courses: int = 0
    subjects: int = 0
    rooms: int = 0
    created: int = 0
    updated: int = 0
    deleted: int = 0
    warnings: tuple[str, ...] = ()


class SyncHistoryStore:
    def __init__(self, cache_dir):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.history_path = self.cache_dir / "sync_history.json"

    def add(self, record: SyncHistoryRecord) -> None:
        records = list(self.list_records())
        records.append(record)
        self.history_path.write_text(
            json.dumps([self._to_dict(item) for item in records], ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def list_records(self) -> tuple[SyncHistoryRecord, ...]:
        if not self.history_path.exists():
            return ()
        raw = json.loads(self.history_path.read_text(encoding="utf-8"))
        return tuple(self._from_dict(item) for item in raw)

    def clear(self) -> None:
        if self.history_path.exists():
            self.history_path.unlink()

    def build_record(self, sync_result) -> SyncHistoryRecord:
        diff = sync_result.diff
        return SyncHistoryRecord(
            id=datetime.now().strftime("%Y%m%d%H%M%S"),
            source=sync_result.package.source,
            provider=sync_result.session.provider,
            created_at=datetime.now().isoformat(timespec="seconds"),
            teachers=sync_result.import_result.teachers,
            courses=sync_result.import_result.courses,
            subjects=sync_result.import_result.subjects,
            rooms=sync_result.import_result.rooms,
            created=len(diff.created) if diff else 0,
            updated=len(diff.updated) if diff else 0,
            deleted=len(diff.deleted) if diff else 0,
            warnings=tuple(sync_result.import_result.warnings),
        )

    def _to_dict(self, record: SyncHistoryRecord) -> dict:
        data = asdict(record)
        data["warnings"] = list(record.warnings)
        return data

    def _from_dict(self, data: dict) -> SyncHistoryRecord:
        data = dict(data)
        data["warnings"] = tuple(data.get("warnings", ()))
        return SyncHistoryRecord(**data)
