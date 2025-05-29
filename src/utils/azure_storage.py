from __future__ import annotations

from pathlib import Path
from typing import Iterable


class AzureStorageClient:
    """Placeholder Azure Blob Storage client for tests."""

    def upload_files(self, files: Iterable[Path]) -> None:  # pragma: no cover
        pass

    def cleanup_temp_blobs(self) -> None:  # pragma: no cover
        pass