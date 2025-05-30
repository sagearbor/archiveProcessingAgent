from __future__ import annotations

import json
from typing import Any, Dict


class ResponseFormatter:
    """Format agent responses for different consumption patterns."""

    def format_response(
        self,
        content_data: Dict[str, Any],
        request_context: str,
        target_agent_type: str = "generic",
    ) -> str:
        if target_agent_type == "json":
            return self.format_as_json(content_data)
        if target_agent_type == "markdown":
            return self.format_as_markdown(content_data)
        if target_agent_type == "references":
            return self.format_as_references(content_data)
        return str(content_data)

    def format_as_json(self, content_data: Dict[str, Any]) -> str:
        return json.dumps(content_data)

    def format_as_markdown(self, content_data: Dict[str, Any]) -> str:
        lines = [f"- {k}: {v}" for k, v in content_data.items()]
        return "\n".join(lines)

    def format_as_references(self, content_data: Dict[str, Any]) -> str:
        files = content_data.get("files", [])
        return "\n".join(str(f) for f in files)
