import types
from pathlib import Path

from src.utils.azure_storage import AzureStorageClient


class FakeContainer:
    def __init__(self):
        self.uploaded = []
        self.deleted = []

    def upload_blob(self, name, data, overwrite=False):
        self.uploaded.append(name)

    def list_blobs(self, name_starts_with=None):
        return [types.SimpleNamespace(name="tmp/file1.txt"), types.SimpleNamespace(name="tmp/file2.txt")]

    def delete_blob(self, name):
        self.deleted.append(name)


class FakeService:
    def __init__(self):
        self.container = FakeContainer()

    def get_container_client(self, name):
        return self.container


def test_upload_and_cleanup(monkeypatch, tmp_path: Path):
    fake = FakeService()
    monkeypatch.setattr("src.utils.azure_storage.BlobServiceClient", lambda account_url, credential: fake)

    client = AzureStorageClient("acct", "key", "container")
    file1 = tmp_path / "a.txt"
    file1.write_text("data")
    file2 = tmp_path / "b.txt"
    file2.write_text("more")

    client.upload_files([file1, file2])
    assert fake.container.uploaded == ["a.txt", "b.txt"]

    client.cleanup_temp_blobs(prefix="tmp/")
    assert fake.container.deleted == ["tmp/file1.txt", "tmp/file2.txt"]
