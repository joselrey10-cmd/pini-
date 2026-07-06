from dataclasses import dataclass

from .diff import ImportDiff


@dataclass(frozen=True)
class ConflictResolutionPolicy:
    apply_created: bool = True
    apply_updated: bool = True
    apply_deleted: bool = False


@dataclass(frozen=True)
class ConflictResolutionPlan:
    create_count: int
    update_count: int
    delete_count: int
    skipped_deletes: int

    @property
    def total_actions(self) -> int:
        return self.create_count + self.update_count + self.delete_count


class ImportConflictResolver:
    def build_plan(self, diff: ImportDiff, policy: ConflictResolutionPolicy | None = None) -> ConflictResolutionPlan:
        policy = policy or ConflictResolutionPolicy()

        create_count = len(diff.created) if policy.apply_created else 0
        update_count = len(diff.updated) if policy.apply_updated else 0
        delete_count = len(diff.deleted) if policy.apply_deleted else 0
        skipped_deletes = 0 if policy.apply_deleted else len(diff.deleted)

        return ConflictResolutionPlan(
            create_count=create_count,
            update_count=update_count,
            delete_count=delete_count,
            skipped_deletes=skipped_deletes,
        )
