from __future__ import annotations

import os
import tarfile
import tempfile
import zipfile
from contextlib import contextmanager
from pathlib import Path
from typing import List, Optional

import py7zr

from src.utils.azure_storage import AzureStorageClient
from src.utils.config import AppConfig, load_config

try:
    import magic
except Exception:  # pragma: no cover - optional dependency
    magic = None


class ArchiveHandler:
    """Utility class for detecting and extracting archives."""

    SUPPORTED_TYPES = {
        ".zip": "zip",
        ".tar": "tar",
        ".tar.gz": "tar",
        ".tgz": "tar",
        ".7z": "7z",
    }

    def __init__(
        self,
        storage_client: AzureStorageClient | None = None,
        config: AppConfig | None = None,
    ) -> None:
        """Initialize handler with optional Azure storage and config."""
        self.storage_client = storage_client
        self.config = config or load_config()

    def _use_azure(self, file_path: Path) -> bool:
        """Return True if Azure storage should be used for this file."""
        if self.storage_client is None:
            return False
        if self.config.app_env == "production":
            return True
        size_limit = self.config.max_file_size_mb * 1024 * 1024
        return file_path.stat().st_size > size_limit

    def detect_archive_type(self, file_path: Path) -> Optional[str]:
        """Return archive type based on extension and magic bytes."""
        ext = (
            "".join(file_path.suffixes[-2:])
            if file_path.suffix == ".gz"
            else file_path.suffix
        )
        if ext in self.SUPPORTED_TYPES:
            return self.SUPPORTED_TYPES[ext]
        if magic is not None:
            try:
                mime = magic.from_file(str(file_path), mime=True)
                if "zip" in mime:
                    return "zip"
                if "tar" in mime:
                    return "tar"
                if "7z" in mime:
                    return "7z"
            except Exception:
                pass
        return None

    def extract_archive(
        self,
        file_path: Path,
        extract_to: Optional[Path] = None,
        max_members: int = 1000,
    ) -> List[Path]:
        """Extract the archive and return list of extracted file paths.

        Parameters
        ----------
        file_path: Path
            Archive to extract.
        extract_to: Optional[Path]
            Destination directory. Temporary directory created if not provided.
        max_members: int
            Maximum number of archive entries allowed to prevent zip bombs.
        """
        archive_type = self.detect_archive_type(file_path)
        if archive_type is None:
            raise ValueError("Unsupported archive type")

        use_azure = self._use_azure(file_path)

        if (
            file_path.stat().st_size
            > self.config.max_file_size_mb * 1024 * 1024
            and not use_azure
        ):
            raise ValueError("Archive exceeds configured size limit")

        target_dir = Path(tempfile.mkdtemp()) if extract_to is None else extract_to
        extracted: List[Path] = []

        if archive_type == "zip":
            try:
                zf = zipfile.ZipFile(file_path)
            except zipfile.BadZipFile as exc:
                raise ValueError("Corrupted archive") from exc
            with zf as z:
                members = z.namelist()
                if len(members) > max_members:
                    raise ValueError("Archive contains too many files")
                for member in members:
                    self._safe_extract(z, member, target_dir)
                    extracted.append(target_dir / member)
        elif archive_type == "tar":
            try:
                tf = tarfile.open(file_path)
            except tarfile.TarError as exc:
                raise ValueError("Corrupted archive") from exc
            with tf as t:
                members = t.getmembers()
                if len(members) > max_members:
                    raise ValueError("Archive contains too many files")
                for member in members:
                    self._safe_extract_tar(t, member, target_dir)
                    if member.isfile():
                        extracted.append(target_dir / member.name)
        elif archive_type == "7z":
            try:
                zf = py7zr.SevenZipFile(file_path)
            except py7zr.exceptions.Bad7zFile as exc:
                raise ValueError("Corrupted archive") from exc
            with zf as z:
                members = z.getnames()
                if len(members) > max_members:
                    raise ValueError("Archive contains too many files")
                z.extractall(target_dir)
                extracted.extend([p for p in target_dir.rglob("*") if p.is_file()])
        else:
            raise ValueError("Unsupported archive type")

        if use_azure:
            self.storage_client.upload_files(extracted)
            for f in extracted:
                try:
                    f.unlink()
                except Exception:
                    pass
        return extracted

    def list_contents(self, file_path: Path) -> List[str]:
        """Return list of contents without extraction."""
        archive_type = self.detect_archive_type(file_path)
        if archive_type == "zip":
            with zipfile.ZipFile(file_path) as z:
                return z.namelist()
        if archive_type == "tar":
            with tarfile.open(file_path) as t:
                return [m.name for m in t.getmembers()]
        if archive_type == "7z":
            with py7zr.SevenZipFile(file_path) as z:
                return z.getnames()
        raise ValueError("Unsupported archive type")

    @contextmanager
    def temp_extract(self, file_path: Path, max_members: int = 1000):
        """Context manager that extracts to a temporary directory and cleans up."""
        with tempfile.TemporaryDirectory() as tmpdir:
            files = self.extract_archive(file_path, Path(tmpdir), max_members=max_members)
            try:
                yield files
            finally:
                if self._use_azure(file_path) and self.storage_client:
                    self.storage_client.cleanup_temp_blobs()

    def _safe_extract(
        self, zipf: zipfile.ZipFile, member: str, target_dir: Path
    ) -> None:
        dest = target_dir / member
        if not str(dest.resolve()).startswith(str(target_dir.resolve())):
            raise ValueError("Attempted Path Traversal in Zip File")
        zipf.extract(member, path=target_dir)

    def _safe_extract_tar(
        self, tarf: tarfile.TarFile, member: tarfile.TarInfo, target_dir: Path
    ) -> None:
        dest = target_dir / member.name
        if not str(dest.resolve()).startswith(str(target_dir.resolve())):
            raise ValueError("Attempted Path Traversal in Tar File")
        tarf.extract(member, path=target_dir)
