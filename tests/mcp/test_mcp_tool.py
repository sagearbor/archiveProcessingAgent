from pathlib import Path
import pytest

from src.mcp.mcp_tool import extract_archive_tool

DATA_DIR = Path(__file__).resolve().parents[2] / "mock_data"


def test_extract_archive_basic(tmp_path):
    result = extract_archive_tool(str(DATA_DIR / "mock_archive.zip"))
    assert result["status"] == "success"
    paths = [
        Path(f).name if isinstance(f, str) else Path(f["path"]).name
        for f in result["files"]
    ]
    assert "file.txt" in paths


def test_file_not_found():
    res = extract_archive_tool("/nonexistent/archive.zip")
    assert res["status"] == "error"


def test_extract_detailed_mode():
    result = extract_archive_tool(
        str(DATA_DIR / "mock_archive.zip"), extraction_mode="detailed"
    )
    assert isinstance(result["files"][0], dict)


def test_invalid_mode():
    res = extract_archive_tool(
        str(DATA_DIR / "mock_archive.zip"), extraction_mode="invalid"
    )
    assert res["status"] == "error"


def test_corrupted_archive(tmp_path):
    bad_file = tmp_path / "bad.zip"
    bad_file.write_text("not an archive")
    res = extract_archive_tool(str(bad_file))
    assert res["status"] == "error"


def test_output_structure():
    res = extract_archive_tool(str(DATA_DIR / "mock_archive.zip"))
    assert set(res.keys()) >= {"status", "message", "archive_info", "files", "metadata"}


@pytest.mark.parametrize(
    "fname",
    [
        "mock_archive.zip",
        "mock_source.tar.gz",
        "mock_synapse.zip",
    ],
)
def test_all_mock_archives(fname):
    res = extract_archive_tool(str(DATA_DIR / fname))
    assert res["status"] == "success"
