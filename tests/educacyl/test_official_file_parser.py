from packages.educacyl.file_parser import OfficialFileParser
from packages.educacyl.template import OfficialImportTemplate


def test_parse_official_excel_template(tmp_path):
    path = tmp_path / "educacyl_import.xlsx"
    OfficialImportTemplate().create(path)

    package = OfficialFileParser().parse_file(path)

    assert len(package.teachers) == 1
    assert len(package.courses) == 1
    assert len(package.subjects) == 1
    assert len(package.rooms) == 1
    assert package.configuration.center_name == "CEIP Tierra de Pinares"
