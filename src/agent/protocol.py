from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class AgentRequest:
    """Standardized request structure for A2A communication."""

    file_path: str
    request_text: str
    response_format: str = "markdown"
    agent: str = "unknown"
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Return the request data as a dictionary."""
        return {
            "file_path": self.file_path,
            "request_text": self.request_text,
            "response_format": self.response_format,
            "agent": self.agent,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AgentRequest":
        """Create and validate an :class:`AgentRequest` from a dictionary."""
        obj = cls(
            file_path=data.get("file_path", ""),
            request_text=data.get("request_text", ""),
            response_format=data.get("response_format", "markdown"),
            agent=data.get("agent", "unknown"),
            metadata=data.get("metadata", {}),
        )
        obj.validate()
        return obj

    def validate(self) -> None:
        """Validate required fields and supported formats."""
        if not self.file_path or not isinstance(self.file_path, str):
            raise ValueError("file_path is required")
        if not self.request_text or not isinstance(self.request_text, str):
            raise ValueError("request_text is required")
        if self.response_format not in {"markdown", "json", "references", "executive"}:
            raise ValueError("invalid response_format")


@dataclass
class AgentResponse:
    """Standardized response structure for A2A communication."""

    status: str
    message: str
    data: Any
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Return the response data as a dictionary."""
        return {
            "status": self.status,
            "message": self.message,
            "data": self.data,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AgentResponse":
        """Create and validate an :class:`AgentResponse` from a dictionary."""
        obj = cls(
            status=data.get("status", ""),
            message=data.get("message", ""),
            data=data.get("data"),
            metadata=data.get("metadata", {}),
        )
        obj.validate()
        return obj

    def validate(self) -> None:
        """Validate response structure."""
        if self.status not in {"success", "error"}:
            raise ValueError("status must be 'success' or 'error'")
