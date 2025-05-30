from __future__ import annotations

from typing import Any, Dict


class AgentRegistry:
    """Simple in-memory registry for agent capabilities."""

    def __init__(self) -> None:
        self._agents: Dict[str, Dict[str, Any]] = {}

    def register_agent(self, name: str, capabilities: Dict[str, Any]) -> None:
        """Register an agent and its capabilities."""
        self._agents[name] = capabilities

    def get_agent_capabilities(self, name: str) -> Dict[str, Any]:
        """Return capabilities for the specified agent."""
        return self._agents.get(name, {})

    def list_agents(self) -> Dict[str, Dict[str, Any]]:
        """Return all registered agents and their capabilities."""
        return dict(self._agents)
