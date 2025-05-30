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


def test_extract_tool_invalid_max_files(tmp_path):
    archive = tmp_path / "simple.zip"
    with zipfile.ZipFile(archive, "w") as z:
        z.writestr("a.txt", "1")
    from src.mcp.mcp_tool import extract_archive_tool

    result = extract_archive_tool(str(archive), max_files=0)
    assert result["status"] == "error"


def test_request_interpreter_sanitization():
    from src.agent.request_interpreter import RequestInterpreter

    text = "<script>alert('x')</script> extract data; DROP TABLE users;"
    interp = RequestInterpreter()
    res = interp.analyze_request_intent(text)
    assert res["intent"] == "extract"
    for kw in res["keywords"]:
        assert all(ch.isalnum() or ch == "_" for ch in kw)


def test_extract_tool_special_char_filename(tmp_path):
    archive = tmp_path / "weird;name.zip"
    with zipfile.ZipFile(archive, "w") as z:
        z.writestr("file.txt", "data")
    from src.mcp.mcp_tool import extract_archive_tool

    result = extract_archive_tool(str(archive))
    assert result["status"] == "success"
    assert any(
        (Path(f).name if isinstance(f, str) else Path(f["path"]).name) == "file.txt"
        for f in result["files"]
    )
