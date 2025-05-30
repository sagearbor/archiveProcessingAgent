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


def create_handler(agent: ArchiveAgent):
    def handler(request: dict):
        req = AgentRequest.from_dict(request)
        content = agent.process_request(req.file_path, req.request_text)
        return AgentResponse(status="success", message="ok", data=content).to_dict()

    return handler


@pytest.mark.parametrize(
    "fname",
    [
        "mock_word.docx",
        "mock_excel.xlsx",
        "mock_powerpoint.pptx",
        "mock_powerbi.pbix",
        "mock_tableau.twbx",
        "mock_synapse.zip",
        "mock_archive.zip",
        "mock_source.tar.gz",
    ],
)
def test_full_pipeline_all_formats(fname):
    agent = ArchiveAgent()
    registry = AgentRegistry()
    router = RequestRouter(registry)
    registry.register_agent("archive", {"formats": ["*"]}, version="1.0", handler=create_handler(agent))

    request = AgentRequest(
        file_path=str(DATA_DIR / fname),
        request_text="summarize",
    ).to_dict()

    result = router.send_request(request, retries=1)
    assert result["status"] == "success"
    assert "summary" in result["data"]
    assert registry.get_agent_status("archive") == "online"
