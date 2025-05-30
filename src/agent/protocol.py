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
