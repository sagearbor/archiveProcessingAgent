from __future__ import annotations

import json
from typing import Any, Dict, List


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
        if target_agent_type == "executive":
            return self.format_as_executive_summary(content_data)
        return str(content_data)

    def format_as_json(self, content_data: Dict[str, Any]) -> str:
        return json.dumps(content_data)

    def format_as_markdown(self, content_data: Dict[str, Any]) -> str:
        lines = [f"- {k}: {v}" for k, v in content_data.items()]
        return "\n".join(lines)

    def format_as_references(self, content_data: Dict[str, Any]) -> str:
        files = content_data.get("files", [])
        return "\n".join(str(f) for f in files)

    def format_as_executive_summary(
        self, content_data: Dict[str, Any], executive_level: str = "manager"
    ) -> str:
        """Return a short executive style summary."""
        summary = content_data.get("summary", "")
        key_points = content_data.get("key_points", [])
        lines = [f"# Executive Summary ({executive_level.title()})"]
        if summary:
            lines.append(summary)
        if key_points:
            lines.append("## Key Points")
            lines.extend(f"- {p}" for p in key_points)
        return "\n".join(lines)

    def detect_agent_preferences(
        self, agent_context: Dict[str, Any], request_history: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Infer preferred response format from history and context."""
        formats = [h.get("format") for h in request_history if h.get("format")]
        if formats:
            preferred = max(set(formats), key=formats.count)
        else:
            preferred = agent_context.get("default_format", "markdown")
        return {"preferred_format": preferred}

    def customize_response_depth(
        self, content_data: Dict[str, Any], complexity_preference: str = "standard"
    ) -> Dict[str, Any]:
        """Adjust the amount of detail included in the response."""
        if complexity_preference == "minimal":
            return {"summary": content_data.get("summary")}
        if complexity_preference == "detailed":
            return content_data
        filtered = dict(content_data)
        filtered.pop("raw", None)
        return filtered

    def validate_response_quality(
        self, formatted_response: str, original_request: str
    ) -> Dict[str, Any]:
        """Check if response appears to address the original request."""
        request_terms = original_request.lower().split()
        missing = [t for t in request_terms if t not in formatted_response.lower()]
        return {"complete": not missing, "missing_terms": missing}
