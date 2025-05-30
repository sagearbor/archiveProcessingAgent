from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Dict, List

from src.core.archive_handler import ArchiveHandler



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

    handler = ArchiveHandler()
    archive_type = handler.detect_archive_type(path)
    if not archive_type:
        return {"status": "error", "message": "Unsupported archive type"}

    start = datetime.utcnow()
    try:
        extracted_files: List[Path] = handler.extract_archive(path)
    except Exception as exc:
        return {"status": "error", "message": str(exc)}

    files = [_file_info(p) for p in extracted_files[:max_files]]
    archive_info = {
        "type": archive_type,
        "size": path.stat().st_size,
        "file_count": len(extracted_files),
    }
    metadata = {
        "extraction_time": datetime.utcnow().isoformat(),
        "processing_duration": (datetime.utcnow() - start).total_seconds(),
        "warnings": [],
    }

    return {
        "status": "success",
        "message": "Archive extracted",
        "archive_info": archive_info,
        "files": files,
        "metadata": metadata if include_metadata else {},
    }
