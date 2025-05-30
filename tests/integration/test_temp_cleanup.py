import zipfile
from pathlib import Path

from src.core.archive_handler import ArchiveHandler


def test_temp_extract_cleanup(tmp_path: Path):
    archive = tmp_path / "data.zip"
    with zipfile.ZipFile(archive, "w") as z:
        z.writestr("a.txt", "content")

    handler = ArchiveHandler()
    with handler.temp_extract(archive) as files:
        temp_dir = files[0].parent
        assert temp_dir.exists()
    # after context manager exits, directory should be removed
    assert not temp_dir.exists()
