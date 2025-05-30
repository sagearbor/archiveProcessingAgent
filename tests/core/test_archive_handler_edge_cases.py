import zipfile
import tarfile
from pathlib import Path
from src.core.archive_handler import ArchiveHandler


def test_extract_empty_zip(tmp_path):
    empty_zip = tmp_path / "empty.zip"
    with zipfile.ZipFile(empty_zip, "w"):
        pass
    handler = ArchiveHandler()
    extracted = handler.extract_archive(empty_zip, tmp_path / "out")
    assert extracted == []


def test_extract_special_characters(tmp_path):
    archive = tmp_path / "special.zip"
    special_name = "\u00FC\u00F1\u00ED\u00E7\u00F8d\u00E9.txt"
    with zipfile.ZipFile(archive, "w") as z:
        z.writestr(special_name, "data")
    handler = ArchiveHandler()
    extracted = handler.extract_archive(archive, tmp_path / "out")
    assert any(p.name == special_name for p in extracted)


def test_list_nested_archive(tmp_path):
    inner_zip = tmp_path / "inner.zip"
    with zipfile.ZipFile(inner_zip, "w") as z:
        z.writestr("a.txt", "data")
    outer_zip = tmp_path / "outer.zip"
    with zipfile.ZipFile(outer_zip, "w") as z:
        z.write(inner_zip, arcname="inner.zip")
    handler = ArchiveHandler()
    contents = handler.list_contents(outer_zip)
    assert "inner.zip" in contents
