from datetime import timedelta

from src.agent.registry import AgentRegistry


def test_register_and_get_capabilities():
    registry = AgentRegistry()
    registry.register_agent(
        "agent1", {"formats": ["zip", "tar"]}, version="1.0"
    )
    assert registry.get_agent_capabilities("agent1") == {
        "formats": ["zip", "tar"]
    }
    assert registry.get_agent_status("agent1") == "online"


def test_list_agents_and_status():
    registry = AgentRegistry()
    registry.register_agent("agent1", {"formats": ["zip"]})
    registry.register_agent("agent2", {"formats": ["docx"]})
    agents = registry.list_agents()
    assert agents["agent1"]["formats"] == ["zip"]
    assert agents["agent2"]["formats"] == ["docx"]
    registry.update_agent_status("agent1", "error")
    assert registry.get_agent_status("agent1") == "error"


def test_health_monitoring():
    registry = AgentRegistry()
    registry.register_agent("agent1", {})
    assert registry.check_health("agent1", threshold=1) == "online"
    registry._last_heartbeat["agent1"] -= timedelta(seconds=2)
    assert registry.check_health("agent1", threshold=1) == "offline"
    registry.heartbeat("agent1")
    assert registry.check_health("agent1", threshold=1) == "online"


def test_version_compatibility_and_metadata():
    registry = AgentRegistry()
    registry.register_agent(
        "agent1",
        {},
        version="1.2.0",
        metadata={"description": "test agent"},
    )
    assert registry.is_version_compatible("agent1", minimum="1.0")
    assert not registry.is_version_compatible("agent1", minimum="2.0")
    assert registry.get_agent_metadata("agent1") == {
        "description": "test agent"
    }
    registry.register_agent("agent2", {}, version="0.9")
    compatible = registry.find_compatible_agents(minimum="1.0")
    assert compatible == ["agent1"]


def test_documentation_storage():
    registry = AgentRegistry()
    registry.register_agent("a1", {})
    registry.add_agent_documentation("a1", "Docs 1. ")
    registry.add_agent_documentation("a1", "More docs")
    assert registry.get_agent_documentation("a1") == "Docs 1. More docs"
