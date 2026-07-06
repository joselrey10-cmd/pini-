from dataclasses import dataclass, field
from typing import Any

from .models import ImportPackage


@dataclass(frozen=True)
class DiffItem:
    entity: str
    code: str
    change_type: str
    before: dict[str, Any] | None = None
    after: dict[str, Any] | None = None


@dataclass(frozen=True)
class ImportDiff:
    created: tuple[DiffItem, ...] = ()
    updated: tuple[DiffItem, ...] = ()
    deleted: tuple[DiffItem, ...] = ()

    @property
    def has_changes(self) -> bool:
        return bool(self.created or self.updated or self.deleted)

    @property
    def total_changes(self) -> int:
        return len(self.created) + len(self.updated) + len(self.deleted)


class ImportPackageDiffer:
    def diff(self, old: ImportPackage, new: ImportPackage) -> ImportDiff:
        created = []
        updated = []
        deleted = []

        for entity, old_items, new_items in [
            ("teacher", old.teachers, new.teachers),
            ("course", old.courses, new.courses),
            ("subject", old.subjects, new.subjects),
            ("room", old.rooms, new.rooms),
        ]:
            entity_diff = self._diff_items(entity, old_items, new_items)
            created.extend(entity_diff.created)
            updated.extend(entity_diff.updated)
            deleted.extend(entity_diff.deleted)

        return ImportDiff(
            created=tuple(created),
            updated=tuple(updated),
            deleted=tuple(deleted),
        )

    def _diff_items(self, entity: str, old_items, new_items) -> ImportDiff:
        old_map = {item.code: item for item in old_items}
        new_map = {item.code: item for item in new_items}

        created = []
        updated = []
        deleted = []

        for code, item in new_map.items():
            if code not in old_map:
                created.append(DiffItem(entity, code, "created", None, item.__dict__))
            elif old_map[code] != item:
                updated.append(DiffItem(entity, code, "updated", old_map[code].__dict__, item.__dict__))

        for code, item in old_map.items():
            if code not in new_map:
                deleted.append(DiffItem(entity, code, "deleted", item.__dict__, None))

        return ImportDiff(
            created=tuple(created),
            updated=tuple(updated),
            deleted=tuple(deleted),
        )
