from packages.educacyl.conflict_resolver import ConflictResolutionPolicy, ImportConflictResolver
from packages.educacyl.diff import ImportPackageDiffer
from packages.educacyl.models import ImportPackage, TeacherImport
from packages.educacyl.validator import ImportPackageValidator


def test_validator_detects_duplicate_codes():
    package = ImportPackage(
        teachers=(
            TeacherImport("P01", "Ana", "García"),
            TeacherImport("P01", "Luis", "Pérez"),
        )
    )

    report = ImportPackageValidator().validate(package)

    assert report.has_errors
    assert any("duplicado" in issue.message for issue in report.issues)


def test_conflict_resolution_plan_skips_deletes_by_default():
    old = ImportPackage(teachers=(TeacherImport("P01", "Ana", "García"),))
    new = ImportPackage(teachers=())

    diff = ImportPackageDiffer().diff(old, new)
    plan = ImportConflictResolver().build_plan(diff)

    assert plan.delete_count == 0
    assert plan.skipped_deletes == 1


def test_conflict_resolution_policy_can_apply_deletes():
    old = ImportPackage(teachers=(TeacherImport("P01", "Ana", "García"),))
    new = ImportPackage(teachers=())

    diff = ImportPackageDiffer().diff(old, new)
    plan = ImportConflictResolver().build_plan(diff, ConflictResolutionPolicy(apply_deleted=True))

    assert plan.delete_count == 1
    assert plan.skipped_deletes == 0
