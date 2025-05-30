from pathlib import Path

from src.core.content_summarizer import ContentSummarizer


def test_generate_summary():
    summarizer = ContentSummarizer()
    data = {"files": ["a.txt", "b.txt"], "categories": {"docs": ["a.txt"], "code": ["b.txt"]}}
    summary = summarizer.generate_executive_summary(data, "test")
    assert summary["total_files"] == 2
    assert summary["category_counts"]["docs"] == 1


def test_create_file_inventory(tmp_path):
    summarizer = ContentSummarizer()
    f1 = tmp_path / "file1.txt"
    f1.write_text("hello")
    inventory = summarizer.create_file_inventory([f1], {str(f1): {"size": 5, "modified": "now"}})
    assert inventory[0]["path"] == str(f1)
    assert inventory[0]["size"] == 5


def test_format_for_agent_consumption():
    summarizer = ContentSummarizer()
    summary = {"total_files": 1}
    out = summarizer.format_for_agent_consumption(summary, "json")
    assert "total_files" in out

