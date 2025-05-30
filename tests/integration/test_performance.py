import time
from pathlib import Path
import zipfile
import tracemalloc
from concurrent.futures import ThreadPoolExecutor
import pytest
import cProfile
import pstats

from src.core.archive_handler import ArchiveHandler

from src.agent import (
    AgentRegistry,
    RequestRouter,
    ArchiveAgent,
    AgentRequest,
    AgentResponse,
)

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


def test_extract_no_disk_space(monkeypatch, tmp_path):
    handler = ArchiveHandler()
    archive = tmp_path / "small.zip"
    with zipfile.ZipFile(archive, "w") as z:
        z.writestr("file.txt", "data")

    def no_space(*args, **kwargs):
        raise OSError(28, "No space left on device")

    monkeypatch.setattr(zipfile.ZipFile, "extract", no_space)
    with pytest.raises(OSError):
        handler.extract_archive(archive, tmp_path / "out")


@pytest.mark.parametrize("file_count", [5, 15, 25])
def test_benchmark_extraction_speed_various_sizes(tmp_path, file_count):
    handler = ArchiveHandler()
    archive = tmp_path / f"bench_{file_count}.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as z:
        chunk = b"a" * 1024 * 1024  # 1 MB per file
        for i in range(file_count):
            z.writestr(f"file_{i}.txt", chunk)

    start = time.time()
    files = handler.extract_archive(archive, tmp_path / "out")
    duration = time.time() - start

    assert len(files) == file_count
    assert duration < file_count * 0.1 + 2


def test_memory_usage_during_extraction(tmp_path):
    handler = ArchiveHandler()
    archive = tmp_path / "memory.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as z:
        chunk = b"b" * 1024 * 1024  # 1 MB
        for i in range(10):
            z.writestr(f"file_{i}.txt", chunk)

    tracemalloc.start()
    handler.extract_archive(archive, tmp_path / "out")
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    assert peak < 50 * 1024 * 1024


@pytest.mark.parametrize(
    "fname,request_text",
    [
        ("mock_archive.zip", "list files"),
        ("mock_word.docx", "extract text"),
        ("mock_excel.xlsx", "summarize"),
    ],
)
def test_response_times_for_request_types(fname, request_text):
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
        file_path=str(DATA_DIR / fname),
        request_text=request_text,
    ).to_dict()

    start = time.time()
    result = router.send_request(request, retries=0)
    duration = time.time() - start

    assert result["status"] == "success"
    assert duration < 1.0


def test_router_concurrent_requests():
    agent = ArchiveAgent()
    registry = AgentRegistry()
    router = RequestRouter(registry)
    registry.register_agent(
        "concurrent",
        {"formats": ["*"]},
        version="1.0",
        handler=make_handler(agent),
    )

    request = AgentRequest(
        file_path=str(DATA_DIR / "mock_archive.zip"),
        request_text="list files",
    ).to_dict()

    def send():
        return router.send_request(request, retries=0)

    with ThreadPoolExecutor(max_workers=5) as exe:
        results = list(exe.map(lambda _: send(), range(10)))

    for res in results:
        assert res["status"] == "success"

    metrics = router.get_metrics()
    assert metrics["requests"] == 10
    assert metrics["successes"] == 10


def test_cpu_usage_profile(tmp_path):
    handler = ArchiveHandler()
    archive = tmp_path / "cpu.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for i in range(20):
            z.writestr(f"file_{i}.txt", "data" * 1000)

    start = time.process_time()
    handler.extract_archive(archive, tmp_path / "out")
    cpu_time = time.process_time() - start

    assert cpu_time < 1.0
