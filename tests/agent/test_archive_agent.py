from pathlib import Path

from src.agent.archive_agent import ArchiveAgent

DATA_DIR = Path(__file__).resolve().parents[2] / "mock_data"


def test_process_request_docx():
    agent = ArchiveAgent()
    result = agent.process_request(str(DATA_DIR / "mock_word.docx"), "extract text")
    assert "paragraphs" in result["content"]
    assert result["summary"]["total_files"] == 1


def test_context_tracking():
    agent = ArchiveAgent()
    agent.process_request(str(DATA_DIR / "mock_word.docx"), "summarize")
    agent.process_request(str(DATA_DIR / "mock_excel.xlsx"), "extract")
    assert len(agent.context) == 2
