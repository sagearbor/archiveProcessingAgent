import py7zr
import pytest
from pathlib import Path

from src.core.archive_handler import ArchiveHandler


def test_extract_password_protected_7z(tmp_path: Path):
    archive = tmp_path / "secret.7z"
    with py7zr.SevenZipFile(archive, "w", password="passwd") as z:
        z.writestr("secret.txt", "hidden")

    handler = ArchiveHandler()
    with pytest.raises(py7zr.exceptions.PasswordRequired):
        handler.extract_archive(archive, tmp_path / "out")
