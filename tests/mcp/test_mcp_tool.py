from pathlib import Path

from src.mcp.mcp_tool import extract_archive_tool

DATA_DIR = Path(__file__).resolve().parents[2] / "mock_data"


def test_extract_archive_basic(tmp_path):
    result = extract_archive_tool(str(DATA_DIR / "mock_archive.zip"))
    assert result["status"] == "success"
    paths = [Path(f["path"]).name for f in result["files"]]
    assert "file.txt" in paths


def test_file_not_found():
    res = extract_archive_tool("/nonexistent/archive.zip")
    assert res["status"] == "error"

