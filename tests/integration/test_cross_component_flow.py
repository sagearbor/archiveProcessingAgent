import zipfile
from pathlib import Path

from src.agent import ArchiveAgent
from src.core.archive_handler import ArchiveHandler
from src.core.relevance_engine import RelevanceEngine
from src.core.content_summarizer import ContentSummarizer

DATA_DIR = Path(__file__).resolve().parents[2] / "mock_data"


def test_cross_component_archive_flow(tmp_path):
    handler = ArchiveHandler()
    extracted = handler.extract_archive(DATA_DIR / "mock_archive.zip", tmp_path / "out")
    engine = RelevanceEngine()
    categories = engine.categorize_content([str(p) for p in extracted], {})
    summarizer = ContentSummarizer()
    summary = summarizer.generate_executive_summary(
        {"files": [str(p) for p in extracted], "categories": categories},
        "summarize contents",
    )
    assert summary["total_files"] == len(extracted)
    assert summary["category_counts"]
    assert categories


def test_end_to_end_nested_archive(tmp_path):
    inner = tmp_path / "inner.zip"
    with zipfile.ZipFile(inner, "w") as z:
        z.write(DATA_DIR / "mock_word.docx", arcname="doc.docx")

    outer = tmp_path / "outer.zip"
    with zipfile.ZipFile(outer, "w") as z:
        z.write(inner, arcname="inner.zip")

    agent = ArchiveAgent()
    result = agent.process_request(str(outer), "list files")
    assert result["content"]["files"] == ["inner.zip"]
    assert result["summary"]["total_files"] == 1
