from pathlib import Path
from src.mcp.registry import ToolRegistry
from src.mcp.mcp_tool import extract_archive_tool


def test_register_and_discover(tmp_path):
    reg = ToolRegistry()
    manifest = {"name": "extract", "description": "test"}
    reg.register_tool("extract", extract_archive_tool, manifest=manifest)
    tools = reg.discover_tools()
    assert "extract" in tools
    assert tools["extract"]["description"] == "test"


def test_load_manifest_and_get_tool(tmp_path):
    reg = ToolRegistry()
    manifest_file = tmp_path / "manifest.json"
    manifest_file.write_text('{"name": "extract", "description": "ok"}')
    manifest = reg.load_manifest(manifest_file)
    reg.register_tool("extract", extract_archive_tool, manifest=manifest)
    tool = reg.get_tool("extract")
    assert tool is extract_archive_tool
