from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any, Callable, Dict, Optional


class AgentRegistry:
    """In-memory registry storing agent capabilities and status."""

    def __init__(self) -> None:
        self._agents: Dict[str, Dict[str, Any]] = {}
        self._last_heartbeat: Dict[str, datetime] = {}

    def register_agent(
        self,
        name: str,
        capabilities: Dict[str, Any],
        *,
        version: str | None = None,
        handler: Callable[[Dict[str, Any]], Any] | None = None,
        metadata: Dict[str, Any] | None = None,
    ) -> None:
        """Register an agent with optional handler, version, and metadata."""
        self._agents[name] = {
            "capabilities": capabilities,
            "version": version,
            "handler": handler,
            "status": "online",
            "metadata": metadata or {},
        }
        self._last_heartbeat[name] = datetime.now(UTC)

    def get_agent_capabilities(self, name: str) -> Dict[str, Any]:
        """Return capabilities for the specified agent."""
        info = self._agents.get(name)
        return info.get("capabilities", {}) if info else {}

    def list_agents(self) -> Dict[str, Dict[str, Any]]:
        """Return all registered agents and their capabilities."""
        return {
            name: data["capabilities"] for name, data in self._agents.items()
        }

    def update_agent_status(self, name: str, status: str) -> None:
        """Update the status of an agent (e.g., online/offline/error)."""
        if name in self._agents:
            self._agents[name]["status"] = status

    def get_agent_status(self, name: str) -> Optional[str]:
        """Return the status of an agent if registered."""
        return self._agents.get(name, {}).get("status")

    def heartbeat(self, name: str) -> None:
        """Record a heartbeat for the specified agent."""
        if name in self._agents:
            self._last_heartbeat[name] = datetime.now(UTC)
            if self.get_agent_status(name) != "online":
                self.update_agent_status(name, "online")

    def get_last_heartbeat(self, name: str) -> Optional[datetime]:
        """Return the timestamp of the last heartbeat."""
        return self._last_heartbeat.get(name)

    def check_health(self, name: str, *, threshold: int = 60) -> str:
        """Return current health status based on last heartbeat."""
        last = self._last_heartbeat.get(name)
        if last is None:
            return "unknown"
        if datetime.now(UTC) - last > timedelta(seconds=threshold):
            self.update_agent_status(name, "offline")
        return self.get_agent_status(name) or "unknown"

    def report_status(self) -> Dict[str, str]:
        """Return status for all agents."""
        return {
            name: self.get_agent_status(name) or "unknown"
            for name in self._agents
        }

    def call_agent(self, name: str, request: Dict[str, Any]) -> Any:
        """Call the registered handler for the agent if available."""
        handler = self._agents.get(name, {}).get("handler")
        if handler is None:
            raise ValueError(f"No handler registered for agent {name}")
        return handler(request)

    def get_agent_metadata(self, name: str) -> Dict[str, Any]:
        """Return metadata associated with an agent."""
        return self._agents.get(name, {}).get("metadata", {})

    def add_agent_documentation(self, name: str, documentation: str) -> None:
        """Attach documentation text to an agent."""
        if name in self._agents:
            self._agents[name].setdefault("docs", "")
            self._agents[name]["docs"] += documentation

    def get_agent_documentation(self, name: str) -> str:
        """Return documentation associated with an agent."""
        return self._agents.get(name, {}).get("docs", "")

    def is_version_compatible(
        self,
        name: str,
        *,
        minimum: str | None = None,
        maximum: str | None = None,
    ) -> bool:
        """Return ``True`` if the agent's version is within the given range."""
        version = self._agents.get(name, {}).get("version")
        if version is None:
            return False
        try:
            from packaging.version import Version

            ver = Version(version)
            if minimum and ver < Version(minimum):
                return False
            if maximum and ver > Version(maximum):
                return False
        except Exception:  # pragma: no cover - invalid version
            return False
        return True

    def find_compatible_agents(
        self, *, minimum: str | None = None, maximum: str | None = None
    ) -> list[str]:
        """Return list of agents compatible with the version range."""
        return [
            name
            for name in self._agents
            if self.is_version_compatible(
                name, minimum=minimum, maximum=maximum
            )
        ]
