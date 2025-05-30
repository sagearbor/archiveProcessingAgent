"""Request routing and load balancing for A2A agents."""

from __future__ import annotations

from itertools import cycle
from typing import Any, Dict, Iterable, Optional

from .registry import AgentRegistry


class RequestRouter:
    """Simple round-robin request router using :class:`AgentRegistry`."""

    def __init__(self, registry: AgentRegistry) -> None:
        self.registry = registry
        self._agent_cycle: Optional[Iterable[str]] = None

    def _update_cycle(self) -> None:
        """Refresh the round-robin cycle when agents change."""
        agents = list(self.registry.list_agents().keys())
        self._agent_cycle = cycle(agents) if agents else None

    def register_agent(self, name: str, capabilities: Dict[str, Any]) -> None:
        """Register an agent and update the routing cycle."""
        self.registry.register_agent(name, capabilities)
        self._update_cycle()

    def get_next_agent(self) -> Optional[str]:
        """Return the next agent in the round-robin cycle."""
        if self._agent_cycle is None:
            self._update_cycle()
        if self._agent_cycle is None:
            return None
        return next(self._agent_cycle)

    def route_request(self, request: Dict[str, Any]) -> Optional[str]:
        """Select an agent to handle the request.

        Parameters
        ----------
        request : Dict[str, Any]
            Parsed request data. Currently unused but reserved for future
            filtering logic.

        Returns
        -------
        Optional[str]
            Name of the selected agent or ``None`` if no agents are registered.
        """

        return self.get_next_agent()
