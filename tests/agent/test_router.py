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
