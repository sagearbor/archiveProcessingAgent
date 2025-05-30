import time
from pathlib import Path
import zipfile

from src.core.archive_handler import ArchiveHandler

from src.agent import AgentRegistry, RequestRouter, ArchiveAgent, AgentRequest, AgentResponse

DATA_DIR = Path(__file__).resolve().parents[2] / "mock_data"


def make_handler(agent: ArchiveAgent):
    def handler(request: dict):
        req = AgentRequest.from_dict(request)
        content = agent.process_request(req.file_path, req.request_text)
        return AgentResponse(status="success", message="ok", data=content).to_dict()

    return handler


def test_router_performance_under_load():
    agent = ArchiveAgent()
    registry = AgentRegistry()
    router = RequestRouter(registry)
    registry.register_agent(
        "perf",
        {"formats": ["*"]},
        version="1.0",
        handler=make_handler(agent),
    )

    request = AgentRequest(
        file_path=str(DATA_DIR / "mock_archive.zip"),
        request_text="list files",
    ).to_dict()

    start = time.time()
    for i in range(20):
        result = router.send_request(request, retries=0)
        assert result["status"] == "success"
    duration = time.time() - start

    metrics = router.get_metrics()
    assert metrics["requests"] == 20
    assert metrics["successes"] == 20
    assert duration < 2.0


def test_extract_extremely_large_archive(tmp_path):
    handler = ArchiveHandler()
    large_zip = tmp_path / "large.zip"
    with zipfile.ZipFile(large_zip, "w", compression=zipfile.ZIP_DEFLATED) as z:
        big_chunk = b"a" * 1024 * 1024  # 1 MB of data
        for i in range(30):
            z.writestr(f"file_{i}.txt", big_chunk)

    start = time.time()
    files = handler.extract_archive(large_zip, tmp_path / "out")
    duration = time.time() - start

    assert len(files) == 30
    assert duration < 5.0
