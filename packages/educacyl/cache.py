import json
from datetime import datetime
from pathlib import Path


class EducaCyLCache:
    def __init__(self, cache_dir):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.metadata_path = self.cache_dir / "metadata.json"

    def write_metadata(self, source: str) -> None:
        self.metadata_path.write_text(
            json.dumps(
                {"source": source, "last_sync": datetime.now().isoformat(timespec="seconds")},
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

    def read_metadata(self) -> dict:
        if not self.metadata_path.exists():
            return {}
        return json.loads(self.metadata_path.read_text(encoding="utf-8"))

    def has_sync(self) -> bool:
        return bool(self.read_metadata().get("last_sync"))

    def clear(self) -> None:
        for path in self.cache_dir.glob("*"):
            if path.is_file():
                path.unlink()
