from pathlib import Path
import os
import zipfile

from src.utils.local_storage import LocalStorageClient
from src.core.archive_handler import ArchiveHandler


def test_local_upload_and_cleanup(tmp_path: Path):
    store = tmp_path / "store"
    client = LocalStorageClient(store)
    file1 = tmp_path / "a.txt"
    file1.write_text("data")
    file2 = tmp_path / "b.txt"
    file2.write_text("more")

    client.upload_files([file1, file2])
    assert (store / "a.txt").exists()
    assert (store / "b.txt").exists()

    (store / "tmp_file.txt").write_text("tmp")
    client.cleanup_temp_blobs(prefix="tmp")
    assert not (store / "tmp_file.txt").exists()


def test_extract_uses_local_storage(tmp_path: Path):
    os.environ["STORAGE_PROVIDER"] = "local"
    archive = tmp_path / "demo.zip"
    with zipfile.ZipFile(archive, "w") as z:
        z.writestr("file.txt", "content")

    store = tmp_path / "store"
    client = LocalStorageClient(store)
    handler = ArchiveHandler(storage_client=client)
    handler.extract_archive(archive)
    assert (store / "file.txt").exists()
