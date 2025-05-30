import io
import py7zr
import pytest
import tarfile
import zipfile
from pathlib import Path

from src.core.archive_handler import ArchiveHandler


def test_extract_password_protected_7z(tmp_path: Path):
    archive = tmp_path / "secret.7z"
    with py7zr.SevenZipFile(archive, "w", password="passwd") as z:
        z.writestr("secret.txt", "hidden")

    handler = ArchiveHandler()
    with pytest.raises(py7zr.exceptions.PasswordRequired):
        handler.extract_archive(archive, tmp_path / "out")


def test_extract_permission_denied(monkeypatch, tmp_path):
    archive = tmp_path / "demo.zip"
    with zipfile.ZipFile(archive, "w") as z:
        z.writestr("file.txt", "content")

    def deny(*args, **kwargs):
        raise PermissionError("denied")

    monkeypatch.setattr(zipfile.ZipFile, "extract", deny)
    handler = ArchiveHandler()
    with pytest.raises(PermissionError):
        handler.extract_archive(archive, tmp_path / "out")


def test_zip_directory_traversal(tmp_path: Path):
    archive = tmp_path / "bad.zip"
    with zipfile.ZipFile(archive, "w") as z:
        z.writestr("../evil.txt", "boom")

    handler = ArchiveHandler()
    with pytest.raises(ValueError):
        handler.extract_archive(archive, tmp_path / "out")


def test_tar_directory_traversal(tmp_path: Path):
    archive = tmp_path / "bad.tar"
    with tarfile.open(archive, "w") as t:
        info = tarfile.TarInfo("../evil.txt")
        data = b"boom"
        info.size = len(data)
        t.addfile(info, io.BytesIO(data))

    handler = ArchiveHandler()
    with pytest.raises(ValueError):
        handler.extract_archive(archive, tmp_path / "out")
