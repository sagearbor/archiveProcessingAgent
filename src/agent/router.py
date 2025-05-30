"""Request routing and load balancing for A2A agents."""

from __future__ import annotations

from itertools import cycle
from typing import Any, Callable, Dict, Iterable, Optional

from .registry import AgentRegistry


class AgentCommunicationError(Exception):
    """Raised when all retries to contact an agent fail."""


class RequestRouter:
    """Simple round-robin request router using :class:`AgentRegistry`."""

    def __init__(self, registry: AgentRegistry) -> None:
        self.registry = registry
        self._agent_cycle: Optional[Iterable[str]] = None

    def _update_cycle(self) -> None:
        """Refresh the round-robin cycle when agents change."""
        agents = list(self.registry.list_agents().keys())
        self._agent_cycle = cycle(agents) if agents else None

    def register_agent(
        self,
        name: str,
        capabilities: Dict[str, Any],
        *,
        version: str | None = None,
        handler: Callable[[Dict[str, Any]], Any] | None = None,
    ) -> None:
        """Register an agent and update the routing cycle."""
        self.registry.register_agent(
            name, capabilities, version=version, handler=handler
        )
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

    def send_request(self, request: Dict[str, Any], *, retries: int = 1) -> Any:
        """Send request to agents with basic retry mechanism."""
        attempt = 0
        last_error: Exception | None = None
        tried: set[str] = set()
        while attempt <= retries:
            agent_name = self.route_request(request)
            if agent_name is None or agent_name in tried:
                break
            tried.add(agent_name)
            try:
                result = self.registry.call_agent(agent_name, request)
                self.registry.heartbeat(agent_name)
                return result
            except Exception as exc:  # pragma: no cover - simple retry
                last_error = exc
                self.registry.update_agent_status(agent_name, "error")
                attempt += 1
        if last_error:
            raise AgentCommunicationError("All retries failed") from last_error
        raise AgentCommunicationError("No agents available")
