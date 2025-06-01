from __future__ import annotations

import shutil
from pathlib import Path
from typing import Iterable

from .storage import StorageClient


class LocalStorageClient(StorageClient):
    """Store extracted files on the local filesystem."""

    def __init__(self, base_path: Path) -> None:
        self.base_path = base_path
        self.base_path.mkdir(parents=True, exist_ok=True)

    def upload_files(self, files: Iterable[Path]) -> None:
        for path in files:
            dest = self.base_path / path.name
            shutil.copy2(path, dest)

    def cleanup_temp_blobs(self, prefix: str = "tmp/") -> None:
        for file in self.base_path.glob(f"{prefix}*"):
            try:
                file.unlink()
            except Exception:
                pass
