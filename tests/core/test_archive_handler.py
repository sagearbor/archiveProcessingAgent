from pathlib import Path
import pytest

from src.core.archive_handler import ArchiveHandler

DATA_DIR = Path(__file__).resolve().parents[2] / "mock_data"


def test_detect_type_zip():
    handler = ArchiveHandler()
    assert handler.detect_archive_type(DATA_DIR / "mock_archive.zip") == "zip"


def test_list_contents_zip():
    handler = ArchiveHandler()
    contents = handler.list_contents(DATA_DIR / "mock_archive.zip")
    assert "file.txt" in contents


def test_extract_zip(tmp_path):
    handler = ArchiveHandler()
    files = handler.extract_archive(DATA_DIR / "mock_archive.zip", tmp_path)
    assert any(f.name == "file.txt" for f in files)


def test_extract_invalid_zip(tmp_path):
    handler = ArchiveHandler()
    corrupted = tmp_path / "bad.zip"
    corrupted.write_text("notzip")
    with pytest.raises(Exception):
        handler.extract_archive(corrupted, tmp_path)


def test_detect_type_unknown(tmp_path):
    handler = ArchiveHandler()
    unknown = tmp_path / "file.xyz"
    unknown.write_text("data")
    assert handler.detect_archive_type(unknown) is None
