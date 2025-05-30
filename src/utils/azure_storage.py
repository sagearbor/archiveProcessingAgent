from __future__ import annotations

from pathlib import Path
from typing import Iterable

try:
    from azure.storage.blob import BlobServiceClient
except Exception:  # pragma: no cover - optional dependency
    BlobServiceClient = None


class AzureStorageClient:
    """Simple wrapper around Azure Blob Storage for uploads and cleanup."""

    def __init__(self, account_name: str, account_key: str, container: str) -> None:
        if BlobServiceClient is None:  # pragma: no cover - offline testing
            self._client = None
            self._container = None
            return
        url = f"https://{account_name}.blob.core.windows.net"
        self._client = BlobServiceClient(account_url=url, credential=account_key)
        self._container = self._client.get_container_client(container)
        self.container = container

    def upload_files(self, files: Iterable[Path]) -> None:
        if self._container is None:  # pragma: no cover - offline testing
            return
        for path in files:
            with open(path, "rb") as fh:
                self._container.upload_blob(name=path.name, data=fh, overwrite=True)

    def cleanup_temp_blobs(self, prefix: str = "tmp/") -> None:
        if self._container is None:  # pragma: no cover - offline testing
            return
        for blob in self._container.list_blobs(name_starts_with=prefix):
            self._container.delete_blob(blob.name)
