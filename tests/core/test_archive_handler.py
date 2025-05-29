from pathlib import Path

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