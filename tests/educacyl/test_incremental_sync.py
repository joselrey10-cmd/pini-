from packages.educacyl.diff import ImportPackageDiffer
from packages.educacyl.models import ImportPackage, TeacherImport
from packages.educacyl.package_store import ImportPackageStore


def test_diff_detects_created_updated_deleted():
    old = ImportPackage(
        teachers=(
            TeacherImport("P01", "Ana", "García", "Primaria"),
            TeacherImport("P02", "Luis", "Pérez", "Inglés"),
        )
    )
    new = ImportPackage(
        teachers=(
            TeacherImport("P01", "Ana", "García", "Primaria"),
            TeacherImport("P03", "Marta", "López", "Música"),
        )
    )

    diff = ImportPackageDiffer().diff(old, new)

    assert len(diff.created) == 1
    assert len(diff.deleted) == 1
    assert diff.total_changes == 2


def test_package_store_roundtrip(tmp_path):
    store = ImportPackageStore(tmp_path)
    package = ImportPackage(teachers=(TeacherImport("P01", "Ana", "García"),), source="test")

    store.save(package)
    loaded = store.load()

    assert loaded is not None
    assert loaded.teachers[0].code == "P01"
    assert loaded.source == "test"
