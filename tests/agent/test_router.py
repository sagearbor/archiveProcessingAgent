from src.agent.registry import AgentRegistry
from src.agent.router import RequestRouter


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
