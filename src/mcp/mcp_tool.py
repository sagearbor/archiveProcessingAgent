from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Dict, Iterable, List
import errno
import tarfile
import zipfile

import py7zr

from src.core.archive_handler import ArchiveHandler
from src.core.office_parser import OfficeParser
from src.core.relevance_engine import RelevanceEngine
from src.utils.config import load_config


ALLOWED_MODES = {"basic", "detailed", "content", "smart"}


def _file_info(path: Path) -> Dict[str, object]:
    stat = path.stat()
    return {
        "path": str(path),
        "size": stat.st_size,
        "type": path.suffix.lstrip("."),
        "modified": datetime.utcfromtimestamp(stat.st_mtime).isoformat(),
    }


def extract_archive_tool(
    file_path: str,
    extraction_mode: str = "basic",
    include_metadata: bool = True,
    max_files: int = 1000,
) -> Dict[str, object]:
    """Basic MCP tool for extracting archives."""

    path = Path(file_path)
    if not path.exists() or not path.is_file():
        return {"status": "error", "message": "File not found"}

    if extraction_mode not in ALLOWED_MODES:
        return {"status": "error", "message": "Invalid extraction mode"}

    cfg = load_config()
    if path.stat().st_size > cfg.max_file_size_mb * 1024 * 1024:
        return {"status": "error", "message": "File too large"}

    if max_files <= 0:
        return {"status": "error", "message": "max_files must be positive"}

    handler = ArchiveHandler()
    archive_type = handler.detect_archive_type(path)
    if not archive_type:
        return {"status": "error", "message": "Unsupported archive type"}

    start = datetime.now(UTC)
    try:
        extracted_files: List[Path] = handler.extract_archive(path)
    except PermissionError:
        return {
            "status": "error",
            "message": "Permission denied. Check file permissions and try again.",
        }
    except (
        zipfile.BadZipFile,
        tarfile.ReadError,
        py7zr.exceptions.ArchiveError,
    ) as exc:
        return {
            "status": "error",
            "message": "Corrupted archive file. Unable to extract.",
        }
    except OSError as exc:
        if exc.errno == errno.ENOSPC:
            return {
                "status": "error",
                "message": "Out of disk space during extraction. Free space and retry.",
            }
        return {"status": "error", "message": str(exc)}
    except Exception as exc:
        return {"status": "error", "message": str(exc)}

    if extraction_mode == "basic":
        files = [str(p) for p in extracted_files[:max_files]]
    else:
        files = [_file_info(p) for p in extracted_files[:max_files]]

    content_data: Dict[str, Iterable[str]] | None = None
    if extraction_mode in {"content", "smart"}:
        parser = OfficeParser()
        contents: Dict[str, Iterable[str]] = {}
        for p in extracted_files[:max_files]:
            if p.suffix.lower() == ".txt":
                contents[str(p)] = p.read_text(errors="ignore").splitlines()
            elif p.suffix.lower() == ".docx":
                contents[str(p)] = parser.parse_docx(p)["paragraphs"]
        if extraction_mode == "smart":
            engine = RelevanceEngine()
            keywords = engine.extract_keywords(" ")
            contents = {
                k: v
                for k, v in contents.items()
                if engine.match_content_to_intent("\n".join(v), keywords) > 0
            }
        content_data = contents
    archive_info = {
        "type": archive_type,
        "size": path.stat().st_size,
        "file_count": len(extracted_files),
    }
    metadata = {
        "extraction_time": datetime.now(UTC).isoformat(),
        "processing_duration": (datetime.now(UTC) - start).total_seconds(),
        "warnings": [],
    }

    return {
        "status": "success",
        "message": "Archive extracted",
        "archive_info": archive_info,
        "files": files,
        "metadata": metadata if include_metadata else {},
        "contents": content_data,
    }
