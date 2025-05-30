"""Request routing and load balancing for A2A agents."""

from __future__ import annotations

from itertools import cycle
from datetime import UTC, datetime, timedelta
from typing import Any, Callable, Dict, Iterable, Optional

from .registry import AgentRegistry


class AgentCommunicationError(Exception):
    """Raised when all retries to contact an agent fail."""


class RateLimitExceededError(Exception):
    """Raised when the request rate limit is exceeded."""


class RequestRouter:
    """Simple round-robin request router using :class:`AgentRegistry`."""

    def __init__(
        self, registry: AgentRegistry, *, requests_per_minute: int = 60
    ) -> None:
        self.registry = registry
        self._agent_cycle: Optional[Iterable[str]] = None
        self._audit_log: list[Dict[str, Any]] = []
        self._request_times: list[datetime] = []
        self.requests_per_minute = requests_per_minute
        self._metrics: Dict[str, int] = {
            "requests": 0,
            "successes": 0,
            "failures": 0,
        }
        self._traces: list[Dict[str, Any]] = []

    def _update_cycle(self) -> None:
        """Refresh the round-robin cycle when agents change."""
        agents = list(self.registry.list_agents().keys())
        self._agent_cycle = cycle(agents) if agents else None

    def _enforce_rate_limit(self) -> None:
        """Raise :class:`RateLimitExceededError` if request rate exceeded."""
        now = datetime.now(UTC)
        window_start = now - timedelta(minutes=1)
        self._request_times = [
            t for t in self._request_times if t > window_start
        ]
        if len(self._request_times) >= self.requests_per_minute:
            raise RateLimitExceededError("request rate limit exceeded")
        self._request_times.append(now)

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

    def send_request(
        self, request: Dict[str, Any], *, retries: int = 1
    ) -> Any:
        """Send request to agents with basic retry mechanism."""
        self._metrics["requests"] += 1
        trace: Dict[str, Any] = {
            "start": datetime.now(UTC).isoformat(),
            "request": request,
        }
        try:
            self._enforce_rate_limit()
        except RateLimitExceededError:
            trace.update(
                {
                    "end": datetime.now(UTC).isoformat(),
                    "duration": 0.0,
                    "success": False,
                    "error": "rate_limit",
                }
            )
            if trace.get("start") and trace.get("end"):
                start = datetime.fromisoformat(trace["start"])
                end = datetime.fromisoformat(trace["end"])
                trace["duration"] = (end - start).total_seconds()
            self._traces.append(trace)
            self._metrics["failures"] += 1
            raise
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
                self._metrics["successes"] += 1
                self._audit_log.append(
                    {
                        "agent": agent_name,
                        "timestamp": datetime.now(UTC).isoformat(),
                        "request": request,
                        "success": True,
                    }
                )
                trace.update(
                    {
                        "end": datetime.now(UTC).isoformat(),
                        "duration": 0.0,
                        "agent": agent_name,
                        "success": True,
                    }
                )
                if trace.get("start") and trace.get("end"):
                    start = datetime.fromisoformat(trace["start"])
                    end = datetime.fromisoformat(trace["end"])
                    trace["duration"] = (end - start).total_seconds()
                self._traces.append(trace)
                return result
            except Exception as exc:  # pragma: no cover - simple retry
                last_error = exc
                self.registry.update_agent_status(agent_name, "error")
                self._metrics["failures"] += 1
                self._audit_log.append(
                    {
                        "agent": agent_name,
                        "timestamp": datetime.now(UTC).isoformat(),
                        "request": request,
                        "success": False,
                        "error": str(exc),
                    }
                )
                attempt += 1
        trace.update(
            {
                "end": datetime.now(UTC).isoformat(),
                "duration": 0.0,
                "success": False,
            }
        )
        if trace.get("start") and trace.get("end"):
            start = datetime.fromisoformat(trace["start"])
            end = datetime.fromisoformat(trace["end"])
            trace["duration"] = (end - start).total_seconds()
        self._traces.append(trace)
        if last_error:
            raise AgentCommunicationError("All retries failed") from last_error
        raise AgentCommunicationError("No agents available")

    def get_audit_log(self, limit: int | None = None) -> list[Dict[str, Any]]:
        """Return recent audit log entries."""
        if limit is None or limit >= len(self._audit_log):
            return list(self._audit_log)
        return self._audit_log[-limit:]

    def get_metrics(self) -> Dict[str, int]:
        """Return basic request metrics."""
        return dict(self._metrics)

    def get_traces(self, limit: int | None = None) -> list[Dict[str, Any]]:
        """Return recent request traces."""
        if limit is None or limit >= len(self._traces):
            return list(self._traces)
        return self._traces[-limit:]
