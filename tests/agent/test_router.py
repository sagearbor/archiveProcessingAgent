import pytest
from datetime import timedelta

from src.agent.registry import AgentRegistry
from src.agent.router import (
    AgentCommunicationError,
    RequestRouter,
    RateLimitExceededError,
)


def test_round_robin_routing():
    registry = AgentRegistry()
    router = RequestRouter(registry)
    router.register_agent("agent1", {})
    router.register_agent("agent2", {})

    order = [router.route_request({}) for _ in range(4)]
    assert order == ["agent1", "agent2", "agent1", "agent2"]


def test_no_agents():
    registry = AgentRegistry()
    router = RequestRouter(registry)
    assert router.route_request({}) is None


def test_send_request_with_retry():
    registry = AgentRegistry()

    def fail_handler(_):
        raise RuntimeError("fail")

    def success_handler(req):
        return {"ok": True, "agent": req.get("id")}

    router = RequestRouter(registry)
    router.register_agent("bad", {}, handler=fail_handler)
    router.register_agent("good", {}, handler=success_handler)

    result = router.send_request({"id": 1}, retries=1)
    assert result == {"ok": True, "agent": 1}
    assert registry.get_agent_status("bad") == "error"


def test_send_request_all_fail():
    registry = AgentRegistry()

    def fail(_):
        raise RuntimeError("fail")

    router = RequestRouter(registry)
    router.register_agent("a1", {}, handler=fail)
    router.register_agent("a2", {}, handler=fail)

    with pytest.raises(AgentCommunicationError):
        router.send_request({}, retries=1)


def test_router_heartbeat():
    registry = AgentRegistry()

    def ok(_):
        return "ok"

    router = RequestRouter(registry)
    router.register_agent("a1", {}, handler=ok)
    assert registry.get_last_heartbeat("a1") is not None
    registry._last_heartbeat["a1"] -= timedelta(seconds=2)
    assert registry.check_health("a1", threshold=1) == "offline"
    router.send_request({}, retries=0)
    assert registry.check_health("a1", threshold=1) == "online"


def test_audit_logging():
    registry = AgentRegistry()

    def ok(req):
        return {"id": req.get("id")}

    router = RequestRouter(registry)
    router.register_agent("a1", {}, handler=ok)
    router.send_request({"id": 123}, retries=0)
    log = router.get_audit_log()
    assert len(log) == 1
    entry = log[0]
    assert entry["agent"] == "a1"
    assert entry["success"] is True
    assert entry["request"]["id"] == 123


def test_rate_limiting_and_metrics():
    registry = AgentRegistry()

    def ok(_):
        return "ok"

    router = RequestRouter(registry, requests_per_minute=1)
    router.register_agent("a1", {}, handler=ok)
    router.send_request({}, retries=0)
    with pytest.raises(RateLimitExceededError):
        router.send_request({}, retries=0)
    metrics = router.get_metrics()
    assert metrics["requests"] == 2
    assert metrics["successes"] == 1
    assert metrics["failures"] == 1
    traces = router.get_traces()
    assert len(traces) == 2
