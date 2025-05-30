import pytest
from pathlib import Path

from src.agent import (
    ArchiveAgent,
    AgentRequest,
    AgentResponse,
    AgentRegistry,
    RequestRouter,
)

DATA_DIR = Path(__file__).resolve().parents[2] / "mock_data"


def create_handler():
    agent = ArchiveAgent()

    def handler(request: dict):
        req = AgentRequest.from_dict(request)
        content = agent.process_request(req.file_path, req.request_text)
        resp = AgentResponse(status="success", message="ok", data=content)
        return resp.to_dict()

    return handler


def test_router_with_mock_agents():
    registry = AgentRegistry()
    router = RequestRouter(registry)
    handler = create_handler()
    registry.register_agent("a1", {"formats": ["zip"]}, version="1.0", handler=handler)
    registry.register_agent("a2", {"formats": ["zip"]}, version="1.0", handler=handler)

    request = AgentRequest(
        file_path=str(DATA_DIR / "mock_archive.zip"),
        request_text="list files",
    ).to_dict()

    result = router.send_request(request, retries=1)
    assert result["status"] == "success"
    assert "files" in result["data"]["content"]
    assert registry.get_agent_status("a1") == "online"


def test_router_retry_on_error():
    registry = AgentRegistry()
    router = RequestRouter(registry)

    def fail_handler(_):
        raise RuntimeError("fail")

    registry.register_agent("fail", {}, version="1.0", handler=fail_handler)
    registry.register_agent("ok", {}, version="1.0", handler=create_handler())

    request = AgentRequest(
        file_path=str(DATA_DIR / "mock_archive.zip"),
        request_text="list",
    ).to_dict()

    result = router.send_request(request, retries=1)
    assert result["status"] == "success"
    assert registry.get_agent_status("fail") == "error"

