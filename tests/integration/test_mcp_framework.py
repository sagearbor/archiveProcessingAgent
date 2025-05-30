from pathlib import Path
from src.mcp import extract_archive_tool, ToolRegistry

DATA_DIR = Path(__file__).resolve().parents[2] / "mock_data"


def test_mcp_tool_integration():
    registry = ToolRegistry()
    manifest = registry.load_manifest("src/mcp/manifest.json")
    registry.register_tool("extract_archive", extract_archive_tool, manifest=manifest)

    tools = registry.discover_tools()
    assert "extract_archive" in tools

    result = registry.get_tool("extract_archive")(str(DATA_DIR / "mock_archive.zip"))
    assert result["status"] == "success"
