from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Iterable


class StorageClient(ABC):
    """Abstract storage interface for uploading and cleanup."""

    @abstractmethod
    def upload_files(self, files: Iterable[Path]) -> None:
        """Upload iterable of files to the storage backend."""
        raise NotImplementedError

    @abstractmethod
    def cleanup_temp_blobs(self, prefix: str = "tmp/") -> None:
        """Remove temporary files from the storage backend."""
        raise NotImplementedError
