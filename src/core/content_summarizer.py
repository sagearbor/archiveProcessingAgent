from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence


class ContentSummarizer:
    """Generate summaries and inventories of extracted content."""

    def generate_executive_summary(
        self, content_data: Dict[str, Any], request_context: str
    ) -> Dict[str, Any]:
        """Return a simple summary based on provided content."""
        files: Sequence[str] = content_data.get("files", [])
        categories: Dict[str, Iterable[str]] = content_data.get("categories", {})
        return {
            "total_files": len(files),
            "category_counts": {k: len(list(v)) for k, v in categories.items()},
            "context": request_context,
        }

    def create_file_inventory(
        self, file_list: Sequence[Path], metadata: Dict[str, Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Return inventory information for each file."""
        inventory: List[Dict[str, Any]] = []
        for file in file_list:
            info = metadata.get(str(file), {})
            inventory.append(
                {
                    "path": str(file),
                    "size": info.get("size"),
                    "modified": info.get("modified"),
                    "type": file.suffix.lstrip("."),
                }
            )
        return inventory

    def describe_file_contents(self, file_path: Path, content_data: Any) -> str:
        """Return a short description of file contents."""
        length = len(str(content_data))
        return f"File {file_path.name} contains {length} characters"

    def identify_relationships(self, content_data: Dict[str, Any]) -> Dict[str, List[str]]:
        """Return relationship information if present."""
        return content_data.get("relationships", {})

    def assess_summary_quality(self, summary_data: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate summary completeness and return quality metrics."""
        required = ["total_files", "category_counts", "context"]
        missing = [field for field in required if field not in summary_data]
        score = 1.0 - (len(missing) / len(required))
        return {"score": round(score, 2), "missing": missing}

    def format_for_agent_consumption(self, summary_data: Dict[str, Any], output_format: str) -> str:
        """Format summary data for different agent types."""
        if output_format == "json":
            return json.dumps(summary_data)
        if output_format == "markdown":
            return "\n".join(f"- {k}: {v}" for k, v in summary_data.items())
        if output_format == "references":
            return "\n".join(summary_data.get("files", []))
        return str(summary_data)

