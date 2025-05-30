from __future__ import annotations

import os
import tarfile
import tempfile
import zipfile
from pathlib import Path
from typing import List, Optional

import py7zr

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

        target_dir = Path(tempfile.mkdtemp()) if extract_to is None else extract_to
        extracted: List[Path] = []

        if archive_type == "zip":
            with zipfile.ZipFile(file_path) as z:
                members = z.namelist()
                if len(members) > max_members:
                    raise ValueError("Archive contains too many files")
                for member in members:
                    self._safe_extract(z, member, target_dir)
                    extracted.append(target_dir / member)
        elif archive_type == "tar":
            with tarfile.open(file_path) as t:
                members = t.getmembers()
                if len(members) > max_members:
                    raise ValueError("Archive contains too many files")
                for member in members:
                    self._safe_extract_tar(t, member, target_dir)
                    if member.isfile():
                        extracted.append(target_dir / member.name)
        elif archive_type == "7z":
            with py7zr.SevenZipFile(file_path) as z:
                members = z.getnames()
                if len(members) > max_members:
                    raise ValueError("Archive contains too many files")
                z.extractall(target_dir)
                extracted.extend([p for p in target_dir.rglob("*") if p.is_file()])
        else:
            raise ValueError("Unsupported archive type")
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
