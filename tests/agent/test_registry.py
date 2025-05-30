from src.agent.registry import AgentRegistry


def test_register_and_get_capabilities():
    registry = AgentRegistry()
    registry.register_agent("agent1", {"formats": ["zip", "tar"]})
    assert registry.get_agent_capabilities("agent1") == {"formats": ["zip", "tar"]}


def test_list_agents():
    registry = AgentRegistry()
    registry.register_agent("agent1", {"formats": ["zip"]})
    registry.register_agent("agent2", {"formats": ["docx"]})
    agents = registry.list_agents()
    assert agents["agent1"]["formats"] == ["zip"]
    assert agents["agent2"]["formats"] == ["docx"]
