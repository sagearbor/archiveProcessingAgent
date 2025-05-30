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


def test_relationship_identification_complex():
    summarizer = ContentSummarizer()
    data = {
        "relationships": {
            "a.csv": ["b.csv", "c.csv"],
            "b.csv": ["c.csv"],
            "folder/d.csv": [],
        }
    }
    rel = summarizer.identify_relationships(data)
    assert rel["a.csv"] == ["b.csv", "c.csv"]
    assert rel["b.csv"] == ["c.csv"]
    assert rel["folder/d.csv"] == []


def test_assess_summary_quality():
    summarizer = ContentSummarizer()
    good = {
        "total_files": 2,
        "category_counts": {},
        "context": "demo",
    }
    quality = summarizer.assess_summary_quality(good)
    assert quality["score"] == 1.0
    assert not quality["missing"]

    bad = {"total_files": 2}
    quality = summarizer.assess_summary_quality(bad)
    assert quality["score"] < 1.0
    assert "category_counts" in quality["missing"]

