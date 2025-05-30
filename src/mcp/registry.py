from __future__ import annotations

from pathlib import Path
from typing import Any, Callable, Dict, Optional
import json


class ToolRegistry:
    """Simple registry for MCP tools."""

    def __init__(self) -> None:
        self._tools: Dict[str, Dict[str, Any]] = {}

    def register_tool(
        self,
        name: str,
        handler: Callable[..., Dict[str, Any]],
        *,
        manifest: Dict[str, Any] | None = None,
    ) -> None:
        """Register a tool with optional manifest."""
        self._tools[name] = {"handler": handler, "manifest": manifest or {}}

    def load_manifest(self, manifest_path: str) -> Dict[str, Any]:
        """Load a JSON manifest from disk."""
        path = Path(manifest_path)
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)

    def discover_tools(self) -> Dict[str, Dict[str, Any]]:
        """Return information about all registered tools."""
        return {name: data["manifest"] for name, data in self._tools.items()}

    def get_tool(self, name: str) -> Callable[..., Dict[str, Any]]:
        """Return the registered handler for a tool."""
        if name not in self._tools:
            raise KeyError(name)
        return self._tools[name]["handler"]
