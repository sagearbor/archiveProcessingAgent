from __future__ import annotations

from typing import Any, Callable, Dict, Optional


class AgentRegistry:
    """In-memory registry storing agent capabilities and status."""

    def __init__(self) -> None:
        self._agents: Dict[str, Dict[str, Any]] = {}

    def register_agent(
        self,
        name: str,
        capabilities: Dict[str, Any],
        *,
        version: str | None = None,
        handler: Callable[[Dict[str, Any]], Any] | None = None,
    ) -> None:
        """Register an agent with optional handler and version."""
        self._agents[name] = {
            "capabilities": capabilities,
            "version": version,
            "handler": handler,
            "status": "online",
        }

    def get_agent_capabilities(self, name: str) -> Dict[str, Any]:
        """Return capabilities for the specified agent."""
        info = self._agents.get(name)
        return info.get("capabilities", {}) if info else {}

    def list_agents(self) -> Dict[str, Dict[str, Any]]:
        """Return all registered agents and their capabilities."""
        return {name: data["capabilities"] for name, data in self._agents.items()}

    def update_agent_status(self, name: str, status: str) -> None:
        """Update the status of an agent (e.g., online/offline/error)."""
        if name in self._agents:
            self._agents[name]["status"] = status

    def get_agent_status(self, name: str) -> Optional[str]:
        """Return the status of an agent if registered."""
        return self._agents.get(name, {}).get("status")

    def call_agent(self, name: str, request: Dict[str, Any]) -> Any:
        """Call the registered handler for the agent if available."""
        handler = self._agents.get(name, {}).get("handler")
        if handler is None:
            raise ValueError(f"No handler registered for agent {name}")
        return handler(request)
